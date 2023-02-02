from rest_framework import filters

from django.db.models.query import QuerySet


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

    def custome_sorting(self, queryset, ordering):
        if "price_for_kilo" or "-price_for_kilo" in ordering:
            if len(ordering) == 1:
                if "-" in ordering[0]:
                    sort_queryset = sorted(
                        queryset,
                        key=lambda x: getattr(x, ordering[0][1:]),
                        reverse=True,
                    )
                else:
                    sort_queryset = sorted(
                        queryset, key=lambda x: getattr(x, ordering[0])
                    )
                return sort_queryset
            else:
                mid = len(ordering) // 2
                my_first_sort = self.custome_sorting(queryset, ordering=ordering[:mid])
                print(my_first_sort, ordering[:mid])
                my_second_sort = self.custome_sorting(
                    my_first_sort, ordering=ordering[mid:]
                )
                print(my_second_sort, ordering[mid:])
                return my_second_sort
        else:
            return queryset

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        if ordering:
            _queryset = self.custome_sorting(queryset, ordering)
            if queryset == []:
                return queryset
            elif isinstance(_queryset, QuerySet):
                return queryset.order_by(*ordering)
            return _queryset
        return queryset
