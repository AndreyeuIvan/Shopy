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

    def custome_sorting(self, queryset, ordering):
        if "price_for_kilo" in ordering:
            
            print([x.id for x in queryset])
            sort_queryset = sorted(queryset, key=lambda x: x.price_for_kilo)
            list_of_ids = [item.id for item in sort_queryset]
            print(list_of_ids)
            new_queryset = queryset.filter(id__in=list_of_ids)
            import pdb;pdb.set_trace()
            ordering.remove('price_for_kilo')
        elif "-price_for_kilo" in ordering:
            sort_queryset = sorted(queryset, key=lambda x: x.price_for_kilo, reverse=True)
            list_of_ids = [item.id for item in sort_queryset]
            queryset = queryset.filter(pk__in=list_of_ids)
            ordering.remove('-price_for_kilo')
        return queryset
    
    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        print(queryset)
        if ordering:
            #import pdb;pdb.set_trace()
            queryset = self.custome_sorting(queryset, ordering)
            print(queryset)
            if queryset == []:
                return queryset
            return queryset.order_by(*ordering)
        return queryset
