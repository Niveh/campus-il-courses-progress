# Protocol Constants

CMD_FIELD_LENGTH = 16  # Exact length of cmd field (in bytes)
LENGTH_FIELD_LENGTH = 4   # Exact length of length field (in bytes)
# Max size of data field according to protocol
MAX_DATA_LENGTH = 10**LENGTH_FIELD_LENGTH-1
MSG_HEADER_LENGTH = CMD_FIELD_LENGTH + 1 + LENGTH_FIELD_LENGTH + \
    1  # Exact size of header (CMD+LENGTH fields)
MAX_MSG_LENGTH = MSG_HEADER_LENGTH + MAX_DATA_LENGTH  # Max size of total message
DELIMITER = "|"  # Delimiter character in protocol
DATA_DELIMITER = "#"  # Delimiter in the data part of the message

# Protocol Messages
# In this dictionary we will have all the client and server command names

PROTOCOL_CLIENT = {
    "login_msg": "LOGIN",
    "logout_msg": "LOGOUT"
}  # .. Add more commands if needed


PROTOCOL_SERVER = {
    "login_ok_msg": "LOGIN_OK",
    "login_failed_msg": "ERROR"
}  # ..  Add more commands if needed


# Other constants

ERROR_RETURN = None  # What is returned in case of an error


def build_message(cmd, data):
    """
    Gets command name (str) and data field (str) and creates a valid protocol message
    Returns: str, or None if error occured
    """
    if len(cmd) > CMD_FIELD_LENGTH or len(data) > MAX_DATA_LENGTH:
        return ERROR_RETURN

    full_msg = DELIMITER.join([cmd.ljust(16), str(len(data)).zfill(4), data])
    return full_msg


def parse_message(data):
    """
    Parses protocol message and returns command name and data field
    Returns: cmd (str), data (str). If some error occured, returns None, None
    """
    data = data.split(DELIMITER)
    if len(data) != 3 or len(data[1]) != 4 or len(data[0]) != 16:
        return ERROR_RETURN, ERROR_RETURN

    if "".join(list(filter(str.isnumeric, data[1]))) != data[1]:
        return ERROR_RETURN, ERROR_RETURN

    msg_len = int(data[1])
    if msg_len != len(data[2]):
        return ERROR_RETURN, ERROR_RETURN

    return data[0].replace(" ", ""), data[2]


def split_data(msg, expected_fields):
    """
    Helper method. gets a string and number of expected fields in it. Splits the string 
    using protocol's data field delimiter (|#) and validates that there are correct number of fields.
    Returns: list of fields if all ok. If some error occured, returns None
    """
    fields = msg.split(DATA_DELIMITER)
    return fields if len(fields) == expected_fields else ERROR_RETURN


def join_data(msg_fields):
    """
    Helper method. Gets a list, joins all of it's fields to one string divided by the data delimiter. 
    Returns: string that looks like cell1#cell2#cell3
    """
    return DATA_DELIMITER.join(msg_fields)
