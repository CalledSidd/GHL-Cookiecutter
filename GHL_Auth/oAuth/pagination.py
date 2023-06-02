from rest_framework.pagination import PageNumberPagination

class ContactsPagination(PageNumberPagination):
    page_size = 1