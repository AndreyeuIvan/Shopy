from rest_framework import filters
from rest_framework.settings import api_settings

from django.utils.translation import gettext_lazy as _


class CustomeOrderingFilter(filters.OrderingFilter):
    """
    def filter_queryset(self, request, queryset, view):
        import pdb;pdb.set_trace()
        ordering = self.get_ordering(request, queryset, view)

        if ordering:
            return queryset.order_by(*ordering)

        return queryset
    """

    ordering_param = api_settings.ORDERING_PARAM
    ordering_fields = None
    ordering_title = _("Ordering")
    ordering_description = _("Which field to use when ordering the results.")
    template = "rest_framework/filters/ordering.html"

    def get_ordering(self, request, queryset, view):

        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        # import pdb;pdb.set_trace()
        print("get_order")
        params = request.query_params.get(self.ordering_param)
        if params in ("price_for_kilo", "-price_for_kilo"):
            return params
        elif params:
            # import pdb;pdb.set_trace()
            fields = [param.strip() for param in params.split(",")]
            ordering = self.remove_invalid_fields(queryset, fields, view, request)
            if ordering:
                return ordering

    def filter_queryset(self, request, queryset, view):
        print("filter_q")
        print(request, queryset, view)
        # import pdb;pdb.set_trace() # Переписать request
        ordering = self.get_ordering(request, queryset, view)
        if ordering == "price_for_kilo":
            queryset = sorted(queryset, key=lambda x: x.price_for_kilo)
        elif ordering == "-price_for_kilo":
            queryset = sorted(queryset, key=lambda x: x.price_for_kilo, reverse=True)
        elif ordering:
            return queryset.order_by(*ordering)

        return queryset
