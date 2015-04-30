from horizon import tables


class FilterAction(tables.FilterAction):

    """simple filter action for search in all available columns
    """

    def filter(self, table, data, filter_string):
        q = filter_string.lower()

        def comp(obj):
            if obj.lower() == q:
                return True
            # dict
            if isinstance(obj, dict):
                for key, value in obj.iteritems():
                    if q in str(obj.get(key, "")).lower():
                        return True
            return False

        return filter(comp, data)
