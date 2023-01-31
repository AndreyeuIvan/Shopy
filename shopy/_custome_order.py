from rest_framework import filters


class CustomeOrderingFilter(filters.OrderingFilter):
    def remove_invalid_fields(self, queryset, fields, view, request):

        valid_fields = [
            item[0]
            for item in self.get_valid_fields(queryset, view, {"request": request})
        ]

        def term_valid(term):
            if term or term[1:] == "price_for_kilo":
                return True
            elif term.startswith("-"):
                term = term[1:]
            return term in valid_fields

        return [term for term in fields if term_valid(term)]

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            if "price_for_kilo" in ordering:
                queryset = sorted(queryset, key=lambda x: x.price_for_kilo)
                return queryset
            elif "-price_for_kilo" in ordering:
                queryset = sorted(queryset, key=lambda x: x.price_for_kilo, reverse=True)
                return queryset
            return queryset.order_by(*ordering)
        return queryset
