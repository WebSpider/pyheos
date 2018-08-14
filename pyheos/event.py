from pyheos import HEOSException, get_message_parts, update_players
from .constants import HEOS_USERNAME, HEOS_PASSWORD


def sources_changed(heosobj, command, data):
    """CLI 5.1"""

    if command == 'event/sources_changed':
        heosobj.send_command(command='browse/get_music_sources')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command),errid=501)


def players_changed(heosobj, command, data):
    """CLI 5.2"""

    if command == 'event/players_changed':
        heosobj.send_command(command='player/get_players')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=502)


def group_changed(heosobj, command, data):
    """CLI 5.3"""

    if command == 'event/groups_changed':
        heosobj.send_command(command='group/get_groups')
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=503)


def player_state_changed(heosobj, command, data):
    """CLI 5.4"""

    if command == 'event/player_state_changed':
        pid = get_message_parts(data, ['pid'])[0]

        heosobj.send_command(command='player/get_player_info?pid={}'.format(pid))
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), errid=504)


def player_now_playing_changed(heosobj, command, data):
    """CLI 5.5"""

    if command == 'event/player_now_playing_changed':
        pid = get_message_parts(data, ['pid'])[0]

        heosobj.send_command(command='player/get_player_info?pid={}'.format(pid))
    else:
        raise HEOSException(message='{} is an unknown command'.format(command), error=505)


def player_now_playing_progress(heosobj, command, data):
    """CLI 5.6"""

    if command == 'event/player_now_playing_progress':

        all_player_info = heosobj.players
        new_pid = data['pid']

        new_player_info = {}
        for player in all_player_info:
            if player['pid'] == new_pid:
                new_player_info.update(data)
            else:
                new_player_info.update(player)

        from datetime import datetime

        try:
            setattr(heosobj, '_players', new_player_info)
            setattr(heosobj, '_refresh_players', datetime.now())
        except:
            e = sys.exc_info()
            raise HEOSException(message=e[1] + ": " + e[2])

def player_playback_error(heosobj, command, data):
    """CLI 5.7"""

    if command == 'event/player_playback_error':

        update_players(heosobj, data)


def player_queue_changed(heosobj, command, data):
    """CLI 5.8"""

    if command == 'event/player_queue_changed':

        # Get player info
        # Get queue info
        pass


def player_volume_changed(heosobj, command, data):
    """CLI 5.9"""

    if command == 'event/player_volume_changed':

        update_players(heosobj, data)


def player_repeat_mode_changed(heosobj, command, data):
    """CLI 5.10"""

    if command == 'event/repeat_mode_changed':

        update_players(heosobj, data)


def player_shuffle_mode_changed(heosobj, command, data):
    """CLI 5.11"""

    if command == 'event/shuffle_mode_changed':

        update_players(heosobj, data)


def group_volume_changed(heosobj, command, data):
    """CLI 5.12"""

    if command == 'event/group_volume_changed':

        update_groups(heosobj, data)


def user_changed(heosobj, command, data):
    """CLI 5.13"""

    if command == 'event/user_changed':

        if signed_out in data:

            heosobj.heos_username = ''
            heosobj.account_status = 'signed_out'
            heosobj.sign_in(username=HEOS_USERNAME, password=HEOS_PASSWORD)

        elif signed_in in data:

            heosobj.heos_username = data['un']
            heosobj.account_status = 'signed_in'
