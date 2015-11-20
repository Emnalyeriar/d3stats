# from datetime import timedelta
from django.db import connection
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, APIClient, APIRequestFactory, force_authenticate
from .models import Account, AccountHistory
from .views import AccountView


class AccountTests(APITestCase):
    """
    Test cases for Accounts app.
    """
    EXAMPLE_ACCOUNTS = ({
        'region': 'eu',
        'battle_tag': 'Emnalyeriar-2594'}, {
        'region': 'us',
        'battle_tag': 'Sanctum-1158'}, {
        'region': 'kr',
        'battle_tag': '특수부대-3188'}, {
        'region': 'tw',
        'battle_tag': '死亡戰刃-3700'
    })
    NONEXISTENT_ACCOUNT = {
        'region': 'eu',
        'battle_tag': 'aaa-0000'
    }
    LEAGUES = ['sc', 'hc', 'sc-s', 'hc-s']

    def setUp(self):
        """
        Fetch some example data from Bnet.
        """
        self.responses = []
        for account in self.EXAMPLE_ACCOUNTS:
            url = reverse('account-details',
                          kwargs=account)
            self.responses.append(self.client.get(url, format='json'))

    def test_create_new_account(self):
        """
        Ensure we create new account instance when it is searched for the first
        time,
        """
        for response in self.responses:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
        account = Account.objects.filter(
            battle_tag=self.EXAMPLE_ACCOUNTS[0]['battle_tag'])
        account_history = AccountHistory.objects.filter(account=account)

        battle_tag = self.EXAMPLE_ACCOUNTS[0]['battle_tag']

        self.assertEqual(account.count(), 1)
        self.assertEqual(account_history.count(), 1)
        self.assertEqual(account[0].battle_tag, battle_tag)
        self.assertEqual(str(account[0]), battle_tag)
        self.assertEqual(
            str(account_history[0]),
            battle_tag + ' | ' + timezone.now().date().strftime('%Y-%m-%d')
        )

    def test_list_all_accounts_for_admin(self):
        """
        Ensure only admin can list all accounts.
        """
        factory = APIRequestFactory()
        admin = User.objects.create(username='admin')
        admin.is_staff = True
        admin.save()
        view = AccountView.as_view()
        request = factory.get('api/accounts/')
        force_authenticate(request, user=admin)
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), len(self.EXAMPLE_ACCOUNTS))

    def test_list_all_accounts_for_user(self):
        """
        Ensure users cannot view all accounts
        """
        url = reverse('accounts-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_not_found_account(self):
        """
        Ensure we get 404 when looking for account that doesn't exist.
        """
        url = reverse('account-details',
                      kwargs=self.NONEXISTENT_ACCOUNT)
        response = self.client.get(url, format='json')
        account = Account.objects.filter(
            battle_tag=self.NONEXISTENT_ACCOUNT['battle_tag'])

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(account.count(), 0)

    def test_recently_updated_accounts(self):
        """
        Ensure updated accounts are seen in the recently updated view.
        """
        response = self.client.get(reverse('recent'))
        self.assertEqual(len(response.data), len(self.EXAMPLE_ACCOUNTS))
        self.assertEqual(Account.objects.count(), len(self.EXAMPLE_ACCOUNTS))

    def test_leaderboards(self):
        """
        Ensure leaderboards for all regions and leagues display correctly.
        """
        for league in self.LEAGUES:
            url = reverse('leaderboards',
                          kwargs={'region': 'all', 'league': league})
            response = self.client.get(url, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 4)
            for account in self.EXAMPLE_ACCOUNTS:
                url = reverse(
                    'leaderboards',
                    kwargs={'region': account['region'], 'league': league}
                )
                response = self.client.get(url, format='json')
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(len(response.data['results']), 1)

    def test_update_account_data(self):
        """
        Ensure account data is updated if account was played since last
        update.
        """
        cursor = connection.cursor()
        last_updated_query = """
            UPDATE accounts_account
            SET last_updated='2000-11-18 19:52:51.060350'
            WHERE battle_tag='{battle_tag}'
        """.format(**self.EXAMPLE_ACCOUNTS[0])
        last_played_query = """
            UPDATE accounts_account
            SET last_played='2000-11-18'
            WHERE battle_tag='{battle_tag}'
        """.format(**self.EXAMPLE_ACCOUNTS[0])
        cursor.execute(last_updated_query)
        cursor.execute(last_played_query)

        url = reverse('account-details', kwargs=self.EXAMPLE_ACCOUNTS[0])
        response = self.client.get(url, format='json')
        account = Account.objects.get(
            battle_tag=self.EXAMPLE_ACCOUNTS[0]['battle_tag'])

        self.assertEqual(
            response.data['last_played'],
            account.last_played.strftime('%Y-%m-%d')
        )
