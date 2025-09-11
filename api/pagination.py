from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class SimpleResultsPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "page": self.page.number,
                "page_size": self.page.paginator.per_page,
                "total_records": self.page.paginator.count,
                "records": data,
            }
        )
