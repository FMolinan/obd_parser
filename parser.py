def parse_message(raw_message):
    """
    Receives a single message and returns a parsed dict with OBD fields and contents
    raw_message: string with a valid payload format (refer to documentation)
    returns: dictionary containing the different fields of the payload and the default elements or a 
    dict containing an error message
    """
    if message_is_valid(raw_message):
        return message_to_dict(raw_message)
    else:
        return {"error": "invalid message"}

def parse_messages(raw_message_list):
    """
    Receives a list of messages and returns a list containing dicts with OBD fields and contents
    raw_message_list: list containing only strings with a valid payload format (refer to documentation)
    returns: a list containing dicts with the different fields of the payload and the default elements,
    ONLY valid messages will be returned
    """
    message_list = [parse_message(m) for m in raw_message_list]
    return [m for m in message_list if 'error' not in m] # return only valid messages


def message_is_valid(message):
    if type(message) != str:
        return
    # for a message to be valid, it must start with * an end with # chars
    if message[0:3] != '*TS' or message[-1] != '#':
        return
    return True

def message_to_dict(raw_message):
    message_list = raw_message[3:-1].rstrip().split(',')
    # The first three elements ALWAYS are protocol version,  device ID (15 char) and packet time
    payload = {
        "protocol": message_list.pop(0),
        "device_id": message_list.pop(0),
        "timestamp": message_list.pop(0)
    }
    for field in message_list:
        # all the other elements should have a ':' to divide by data field and ';' to concatenate data
        data_field = field.split(':')
        payload[data_field[0]] = data_field[1].split(';') if len(data_field[1].split(';')) > 1 else data_field[1]
    return payload
