def split_list_into_equal_parts(lst, sz=8):
    """
    Replaces some query parameters to None

    Args:
        lst (list): list with lists of request body and query parameters
        sz (int, optional): number of lists to split. Defaults to 8.
    """
    splitted_lists = [lst[i:i + sz] for i in range(0, len(lst), sz)]
    # without query parameters
    for splitted_list in splitted_lists:
        # signature_only
        splitted_list[0][1] = None
        splitted_list[0][2] = None
        splitted_list[0][3] = None

        # session_id_only
        splitted_list[1][1] = None
        splitted_list[1][2] = None

        # account_id_only
        splitted_list[2][1] = None
        splitted_list[2][3] = None

        # session_id_and_account_id
        splitted_list[3][1] = None

        # app_id
        splitted_list[4][2] = None
        splitted_list[4][3] = None

        # app_id_and_session_id
        splitted_list[5][2] = None

        # app_id_and_account_id
        splitted_list[6][3] = None
