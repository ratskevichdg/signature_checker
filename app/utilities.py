def find_query_parameter(query_parameter, request_body, parameter_name):
    if query_parameter is None:
        return str(request_body[parameter_name])
    return query_parameter
