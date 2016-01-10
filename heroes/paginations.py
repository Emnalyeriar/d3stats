from rest_framework.pagination import PageNumberPagination


class LeaderboardsPagination(PageNumberPagination):
    """
    Pagination class for leaderboards - adjusted page size
    """
    page_size = 5
