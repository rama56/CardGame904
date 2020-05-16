history = []
beliefs = []
cks = []

hn = []


def reset_history_new():
    global hn
    hn = None


def add_to_new_history(h):
    global hn
    if hn:
        hn.append(h)
    else:
        hn = [h]


def peek_history_new():
    global hn
    if hn:
        return hn[-1]
    else:
        return None


def pop_history_new():
    global hn
    if hn:
        last_element = hn[-1]
        hn = hn[:-1]
        return last_element
    else:
        return None


def get_first_of_history():
    global hn
    if hn:
        return hn[0]
    else:
        return None
