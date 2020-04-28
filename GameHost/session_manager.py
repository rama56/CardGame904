history = []
beliefs = []


def add_to_beliefs(element):
    global beliefs
    if beliefs:
        beliefs.append(element)
    else:
        beliefs = [element]


def get_beliefs():
    global beliefs
    if beliefs:
        return beliefs
    else:
        return None


def reset_beliefs():
    global beliefs
    beliefs = None


def pop_beliefs():
    global beliefs
    if beliefs:
        last_element = beliefs[-1]
        beliefs = beliefs[:-1]
        return last_element
    return None


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
