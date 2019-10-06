import datetime
import random
import string


def random_string(string_length=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(string_length))


def from_date_to_str(date: datetime) -> str:
    if date is None:
        return ''
    return date.strftime("%d-%b-%Y %H:%M:%S.%f")


def extract_search_query_parameters(query):
    page = 0
    rows_per_page = 10
    order_direction = 'asc'
    order_column = 'createdOn'
    filter_keyword = None

    if 'rows_per_page' in query:
        rows_per_page = int(query['rows_per_page'])
    if 'page' in query:
        page = int(query['page'])
    if 'order_column' in query:
        order_column = query['order_column']
    if 'order_direction' in query:
        order_direction = query['order_direction']
    if 'filter_keyword' in query:
        filter_keyword = query['filter_keyword']

    print("=========")
    print(f"rows_per_page: {rows_per_page}; "
          f"filter_keyword: {filter_keyword}; "
          f"order_direction: {order_direction}; "
          f"order_column: {order_column}")

    return {
        "page": page,
        "rows_per_page": rows_per_page,
        "order_direction": order_direction,
        "order_column": order_column,
        "filter_keyword": filter_keyword
    }
