
code_list_hard = []

                    "300062.SZ",
                    "300072.SZ",
                    "000563.SZ",
                    "600126.SS",
                    "601398.SS",
                    "600805.SS",
                ]

def get_code_list_from_file():
    with open("hehe_ss.txt") as ss_file:
        code_list_string = ss_file.read()
        raw_code_list = code_list_string.split()
        ss_code_list = [code +".SS" for code in raw_code_list]

    with open("hehe_sz.txt") as sz_file:
        code_list_string = sz_file.read()
        raw_code_list = code_list_string.split()
        sz_code_list = [code+".SZ" for code in raw_code_list]
    

    code_list = code_list_hard + sz_code_list + ss_code_list
    return code_list



def get_code_list_from_hard_code():
    return code_list_hard

def get_code_list():
    return get_code_list_from_file()
    
