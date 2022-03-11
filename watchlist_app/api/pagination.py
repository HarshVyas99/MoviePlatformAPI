from rest_framework.pagination import PageNumberPagination

class WatchListPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'result'
    max_page_size = 5
    