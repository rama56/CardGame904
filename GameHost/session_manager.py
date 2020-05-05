history = []
beliefs = []
cks = []


def add_to_beliefs(belief, ck):
    global beliefs, cks
    if beliefs:
        beliefs.append(belief)
        cks.append(ck)
    else:
        beliefs = [belief]
        cks = [ck]


def get_beliefs():
    global beliefs, cks
    if beliefs:
        return beliefs, cks
    else:
        return None, None


def reset_beliefs():
    global beliefs, cks
    beliefs = None
    cks = None


def pop_beliefs():
    global beliefs, cks
    if beliefs:
        last_bel = beliefs[-1]
        last_ck = cks[-1]
        beliefs = beliefs[:-1]
        cks = cks[:-1]
        return last_bel, last_ck
    return None, None


def add_to_history(element):
    global history
    if history:
        history.append(element)
    else:
        history = [element]


def get_history():
    global history
    if history:
        return history
    else:
        return None


def reset_history():
    global history
    history = None


def pop_history():
    global history
    if history:
        last_element = history[-1]
        history = history[:-1]
        return last_element
    return None
