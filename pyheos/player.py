from pyheos import HEOSException, get_message_parts, update_players
import sys


def get_players(heosobj, command, data):
    """CLI 4.2.1"""

    from datetime import datetime

    try:
        setattr(heosobj, '_players', data)
        setattr(heosobj, '_refresh_players', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def get_player_info(heosobj, command, data):
    """CLI 4.2.2"""

    update_players(heosobj, data)

def get_play_state(heosobj, command, data):
    """CLI 4.2.3"""

    parts = get_message_parts(data, ['pid', 'state'])

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'state' in parts.keys():
        state = parts['state']
    else:
        raise HEOSException(message='Response does not contain state, aborting')

    if state not in ['play', 'pause', 'stop']:
        raise HEOSException(message='Invalid play state received: {}'.format(state))

    try:
        attrname = "_play_states['" + pid + "']"
        setattr(heosobj, attrname, state)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def set_play_state(heosobj, command, data):
    """CLI 4.2.4"""

    get_play_state(heosobj, command, data)


def get_now_playing_media(heosobj, command, data):
    """CLI 4.2.5"""

    # TODO We need to get passed message, payload AND options to handle this
    pass


def get_volume(heosobj, command, data):
    """CLI 4.2.6"""

    parts = get_message_parts(data, ['pid', 'level'])

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'level' in parts.keys():
        vol_level = parts['level']
    else:
        raise HEOSException(message='Response does not contain volume level, aborting')

    try:
        attrname = "_player_volumes['" + pid + "']"
        setattr(heosobj, attrname, vol_level)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def set_volume(heosobj, command, data):
    """CLI 4.2.7"""

    get_volume(heosobj, command, data)


def volume_up(heosobj, command, data):
    """CLI 4.2.8"""

    parts = get_message_parts(data, ['pid', 'step'])

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'step' in parts.keys():
        step_level = parts['step']
    else:
        raise HEOSException(message='Response does not contain volume level, aborting')

    #TODO: Should we store this somewhere? And for which use? Or should we just get_volume?


def volume_down(heosobj, command, data):
    """CLI 4.2.9"""

    volume_up(heosobj, command, data)


def get_mute(heosobj, command, data):
    """CLI 4.2.10"""

    parts = get_message_parts(data, ['pid', 'state'])

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'state' in parts.keys():
        state = parts['state']
    else:
        raise HEOSException(message='Response does not contain state, aborting')

    if state not in ['on', 'off']:
        raise HEOSException(message='Illegal state received: {}'.format(state))

    try:
        attrname = "_player_mute['" + pid + "']"
        setattr(heosobj, attrname, state)
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def set_mute(heosobj, command, data):
    """CLI 4.2.11"""

    get_mute(heosobj, command, data)


def toggle_mute(heosobj, command, data):
    """CLI 4.2.12"""

    get_mute(heosobj, command, data)


def get_play_mode(heosobj, command, data):
    """CLI 4.2.13"""

    parts = get_message_parts(data, ['pid', 'repeat', 'shuffle'])

    if 'pid' in parts.keys():
        pid = parts['pid']
    else:
        raise HEOSException(message='Response does not contain PID, aborting')

    if 'repeat' in parts.keys():
        repeat_status = parts['repeat']
    else:
        raise HEOSException(message='Response does not contain repeat, aborting')

    if 'shuffle' in parts.keys():
        shuffle_status = parts['shuffle']
    else:
        raise HEOSException(message='Response does not contain shuffle, aborting')

    if repeat_status not in ['on', 'off']:
        raise HEOSException(message='Illegal repeat state received: {}'.format(repeat_status))

    if shuffle_status not in ['']:
        raise HEOSException(message='Illegal shuffle state received: {}'.format(shuffle_status))


def set_play_mode(heosobj, command, data):
    """CLI 4.2.14"""

    get_play_mode(heosobj, command, data)


def get_queue(heosobj, command, data):
    """CLI 4.2.15"""

    setattr(heosobj, "_queue", data)


def play_queue(heosobj, command, data):
    """CLI 4.2.16"""

    pass


def remove_from_queue(heosobj, command, data):
    """CLI 4.2.17"""

    pass


def save_queue(heosobj, command, data):
    """CLI 4.2.18"""

    pass


def clear_queue(heosobj, command, data):
    """CLI 4.2.19"""

    setattr(heosobj, "_queue", [])


def move_queue(heosobj, command, data):
    """CLI 4.2.20"""

    pass


def play_next(heosobj, command, data):
    """CLI 4.2.21"""

    pass


def play_previous(heosobj, command, data):
    """CLI 4.2.22"""

    pass


def set_quickselect(heosobj, command, data):
    """CLI 4.2.23"""

    pass


def play_quickselect(heosobj, command, data):
    """CLI 4.2.24"""

    pass


def get_quickselects(heosobj, command, data):
    """CLI 4.2.25"""

    setattr(heosobj, "_quickselects", data)


def check_update(heosobj, command, data):
    """CLI 4.2.26"""

    update_status = data['update']
    setattr(heosobj, "_update_status", update_status)
