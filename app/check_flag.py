flag_completed = False

def set_completion_flag():
    global flag_completed
    flag_completed = True

def set_completion_flag_false():
    global flag_completed
    flag_completed = False

def check_completion_flag():
    return flag_completed