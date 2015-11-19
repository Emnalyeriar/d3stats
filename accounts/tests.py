from django.utils import timezone
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Account, AccountHistory


class AccountTests(APITestCase):
    """
    Test cases for Account app.
    """

    def test_create_new_account(self):
        """
        Ensure we create new account instance when it is searched for the first
        time,
        """
        url = reverse(
            'account-details',
            kwargs={'region': 'eu', 'battle_tag': 'Emnalyeriar-2594'}
        )
        response = self.client.get(url, format='json')
        account = Account.objects.get()
        account_history = AccountHistory.objects.get()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Account.objects.count(), 1)
        self.assertEqual(AccountHistory.objects.count(), 1)
        self.assertEqual(account.battle_tag, 'Emnalyeriar#2594')
        self.assertEqual(str(account), 'Emnalyeriar#2594')
        self.assertEqual(
            str(account_history),
            timezone.now().date().strftime('%Y-%m-%d')
        )

    def test_not_found_account(self):
        """
        Ensure we get 404 when looking for account that doesn't exist.
        """
        url = reverse('account-details',
                      kwargs={'region': 'eu', 'battle_tag': 'aaa-0000'})
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(Account.objects.count(), 0)
