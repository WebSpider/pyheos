def get_players(heosobj, command, data):
    """CLI 4.2.1"""

    from datetime import datetime

    try:
        setattr(heosobj, 'players', data)
        setattr(heosobj, '_refresh_players', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


def get_player_info(heosobj, command, data):
    """CLI 4.2.2"""

    all_player_info = instance.players
    new_pid = data['pid']

    new_player_info = {}
    for player in all_player_info:
        if player['pid'] == new_pid:
            new_player_info.update(data)
        else
            new_player_info.update(player)

    from datetime import datetime

    try:
        setattr(heosobj, 'players', new_player_info)
        setattr(heosobj, '_refresh_players', datetime.now())
    except:
        e = sys.exc_info()
        raise HEOSException(message=e[1] + ": " + e[2])


