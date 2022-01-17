# from memory_profiler import profile
#
# from loguru import logger
#
#
# @profile
# def find_query_parameter(query_parameter, request_body, parameter_name):
#     """
#     Find a query parameter value from request body if no exists in query.
#
#     Args:
#         query_parameter ([type]): Query parameter.
#         request_body ([type]): Request body.
#         parameter_name ([type]): Parameter name.
#
#     Returns:
#         [str]: Query parameter from Request body
#     """
#     if query_parameter is None:
#         logger.warning(f"Request without query parameter")
#         return str(request_body[parameter_name])
#     return query_parameter
