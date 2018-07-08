import sys
from pyheos import HEOSException

def register_for_change_events(heosobj, command, data):
    """CLI 4.1.1"""
    value = data.split('=')[1]
    try:
        attrname = '_' + command
        setattr(heosobj, attrname, value)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def check_account(heosobj, command, data):
    """CLI 4.1.2"""
    status = data.split('&')

    account_status = status[0]
    account_details = ""
    username = ""

    if len(status) > 1:
        account_details = status[1]

    if account_details and account_status == "signed_in":
        username = account_details.split('=')[1]

    try:
        setattr(heosobj, '_account_status', account_status)
        setattr(heosobj, '_heos_username', username)

    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def sign_in(heosobj, command, data):
    """CLI 4.1.3"""
    check_account(heosobj, command, data)


def sign_out(heosobj, command, data):
    """CLI 4.1.4"""
    check_account(heosobj, command, data)


def heart_beat(heosobj, command, data):
    """CLI 4.1.5"""
    from datetime import datetime
    try:
        setattr(heosobj, '_last_heartbeat', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def reboot(heosobj, command, data):
    """CLI 4.1.6"""
    pass


def prettify_json_response(heosobj, command, data):
    """CLI 4.1.7"""
    register_for_change_events(heosobj, command, data)

