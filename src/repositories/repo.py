from flask_sqlalchemy.pagination import Pagination


class Repo:
    @staticmethod
    def _filter_equals(column, values):
        if isinstance(values, (list, set, tuple)):
            return column.in_(values)
        else:
            return column == values

    @staticmethod
    def _filter_not_equals(column, values):
        if isinstance(values, (list, set, tuple)):
            return column.not_in(values)
        else:
            return column != values

    @staticmethod
    def _do_pagination(query, page, per_page) -> Pagination:
        return query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def _filter_time_interval(column, start=None, end=None):
        conditions = list()
        if start is not None:
            conditions.append(start <= column)
        if end is not None:
            conditions.append(column <= end)
        return conditions
