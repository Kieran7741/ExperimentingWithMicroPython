
import ujson


def get_credentials(fname="credentials.json"):
    """
    Load values from json file
    :param fname: Target credential file
    :return: Dict containing contents of json file
    """
    with open(fname) as f:
        return ujson.loads(f.read())


