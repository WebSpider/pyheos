def register_for_change_events(command, data):
    """CLI 4.1.1"""
    value = data.split('=')[1]
    return {command: value}


def check_account(command, data):
    """CLI 4.1.2"""
    status = data.split('&')

    account_status = status[0]
    account_details = ""
    username = ""

    if len(status) > 1:
        account_details = status[1]

    if account_details and account_status == "signed_in":
        username = account_details.split('=')[1]

    return {
                command: account_status,
                'heos_username': username
           }


def sign_in(command, data):
    """CLI 4.1.3"""
    return check_account(command, data)


def sign_out(command, data):
    """CLI 4.1.4"""
    return check_account(command, data)


def heart_beat(command, data):
    """CLI 4.1.5"""
    from datetime import datetime
    return {'last_heartbeat': datetime.now()}


def reboot(command, data):
    """CLI 4.1.6"""
    return


def prettify_json_response(command, data):
    """CLI 4.1.7"""
    return register_for_change_events(command, data)

