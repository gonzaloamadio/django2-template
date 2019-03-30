"""
    Django drf custom pagination
"""
from collections import OrderedDict

from rest_framework import pagination as drf_pagination
from rest_framework.response import Response


class CustomPagination(drf_pagination.LimitOffsetPagination):
    """Custom pagination class for Django DRF"""

    def __init__(self, *args, **kwargs):
        """Initialize class"""
        self.count = None
        return super(CustomPagination, self).__init__(*args, **kwargs)

    def get_limit(self, request):
        """get limit from request"""
        if self.limit_query_param:
            try:
                return drf_pagination._positive_int(
                    request.query_params[self.limit_query_param]
                )
            except (KeyError, ValueError):
                pass
        return self.default_limit

    def paginate_queryset(self, queryset, request, view=None):
        """
        Overwrite https://github.com/tomchristie/django-rest-framework/blob/
                          master/rest_framework/pagination.py#L347
        to display all results if limit == 0.
        """

        self.limit = self.get_limit(request)
        if self.limit == 0:
            self.request = request
            rows = list(queryset)
            self.count = len(rows)
            return rows

        return super(CustomPagination, self).paginate_queryset(queryset, request, view)

    def get_next_link(self):
        """get next pagination link"""
        if self.limit == 0:
            return None
        return super(CustomPagination, self).get_next_link()

    def get_previous_link(self):
        """get pagination previous link"""
        if self.limit == 0:
            return None
        return super(CustomPagination, self).get_previous_link()

    def get_paginated_response(self, data, extra_meta={}):  # noqa: B006
        """return pagination Response object"""
        if not self.count:
            self.count = len(data)
        document = self._make_response_document(data, extra_meta)
        return Response(document)

    def _make_response_document(self, data, extra_meta={}):  # noqa: B006
        """Create object to return"""
        meta = OrderedDict(
            (
                (
                    'request',
                    self.request.build_absolute_uri(self.request.get_full_path()),
                ),
                ('num_found', self.count),
                ('num_sent', len(data)),
                ('prev', self.get_previous_link()),
                ('next', self.get_next_link()),
            )
        )
        meta.update(extra_meta)
        document = OrderedDict((('meta', meta), ('data', data)))
        return document


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
