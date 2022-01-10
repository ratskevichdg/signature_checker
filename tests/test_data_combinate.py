def split_list_into_equal_parts(lst, sz=8):
    splited_lists = [lst[i:i+sz] for i in range(0, len(lst), sz)]
    # without query parameters
    for splited_list in splited_lists:
        # signature_only
        splited_list[0][1] = None
        splited_list[0][2] = None
        splited_list[0][3] = None

        # session_id_only
        splited_list[1][1] = None
        splited_list[1][2] = None

        # account_id_only
        splited_list[2][1] = None
        splited_list[2][3] = None

        # session_id_and_account_id
        splited_list[3][1] = None

        # app_id
        splited_list[4][2] = None
        splited_list[4][3] = None

        # app_id_and_session_id
        splited_list[5][2] = None

        # app_id_and_account_id
        splited_list[6][3] = None
