from rest_framework.pagination import PageNumberPagination


class LeaderboardsPagination(PageNumberPagination):
    page_size = 5
