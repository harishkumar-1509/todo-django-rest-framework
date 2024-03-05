from rest_framework.pagination import PageNumberPagination

class TodoTaskListPagination(PageNumberPagination):
    # Define no of objs per page
    page_size = 5
    # Customize the query param
    # Here instead of urls/?page=1 we are setting the param to url/?t=1
    page_query_param = 't'
    # Get the page size from the client instead of handling in the code i.e url/?size=7
    page_size_query_param = 'size'
    # To restric the above custome page size by the user, we can use the below implementation
    max_page_size = 10
    # By default if the client wants to visit the last page then, url/?t=last
    last_page_strings = ('last',)
    