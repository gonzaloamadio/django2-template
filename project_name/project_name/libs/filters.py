""" DRF filters library """

import django_filters


class MultipleCharFilter(django_filters.CharFilter):
    """
    Allows multiple options in a comma separated list for Char fields.
    Example:
        - field=value       # filter by a single value
        - field=val1,val2   # Filter by val1 OR val2  (Django's 'in' lookup)
    """

    def filter(self, qs, value):
        if not value:
            return qs
        values = value.split(',')
        if len(values) > 1:
            self.lookup_expr = 'in'
        else:
            values = values[0]
        return super(MultipleCharFilter, self).filter(qs, values)


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
