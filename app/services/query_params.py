from .base import BaseService
import enum
from starlette.datastructures import URL, QueryParams

class QueryParamsService(BaseService):

    def transform_request_query_params(self, request_url):
        url = URL(str(request_url).replace("+", "%2B"))
        return QueryParams(url.query)

    def transform_query_params(self, params):
        params = self.transform_default_query_params(params)
        params = self.transform_filter_query_params(params)
        params = self.transform_search_query_params(params)
        return self.transform_null_query_values(params)

    def transform_default_query_params(self, params):
        params.sort = self.get_sort_value(params)
        params.order = params.get_order_value(params.order)
        params.paginate = params.get_paginate_value(params.paginate)
        params.page = params.get_page_value(params.page)
        return params

    def transform_filter_query_params(self, params):
        return self.get_filter_query_values(
            params, params.get_filter_fields())

    def transform_search_query_params(self, params):
        value = params.search if params.search != "" and params.search != None else None
        params.search = {
            "fields": params.get_search_fields(),
            "value": value
        }
        return params

    def transform_null_query_values(self, params):
        params = dict(params)
        for key in params:
            params[key] = self.get_null_query_value(params[key])
        return params

    def get_null_query_value(self, value):
        if value is None or value == "":
            return None
        return value

    def get_sort_value(self, params):
        field = params.get_sort_field(params.sort)
        use_main_model = field not in params.get_other_table_attribute()
        return {
            "use_main_model": use_main_model,
            "model": self.get_other_table_filter_attribute(use_main_model, params, field),
            "field": field
        }

    def get_filter_query_values(self, params, fields):
        for field in fields:
            values = getattr(params, field)
            if values != "" and values != None:
                use_main_model = field not in params.get_other_table_attribute()
                setattr(params, field, {
                    "use_main_model": use_main_model,
                    "model": self.get_other_table_filter_attribute(use_main_model, params, field),
                    "values": self.get_filter_values(params, field, values.split("+"))
                    })
        return params

    def get_filter_values(self, params, field, values):
        if field in params.get_enum_fields():
            filter_values = self.get_enum_values(params, field, values)
        else:
            filter_values = [value.replace('%20', ' ') for value in values if self.check_valid_filter_value(params, field, value)]
        return filter_values if len(filter_values) > 0 else None

    def check_valid_filter_value(self, params, field, value):
        if field in params.get_numeric_fields():
            return value.isnumeric()
        if field in params.get_boolean_fields():
            return value.lower() in ['1', '0', 'false', 'true']
        return True

    def get_enum_values(self, params, field, values):
        enum_values = [params.get_enum_fields()[field](value) for value in values if value in params.get_enum_fields()[field].list()]
        return enum_values

    def get_other_table_filter_attribute(self, use_main_model, params, field):
        return params.get_other_table_attribute()[field] if not use_main_model else None
