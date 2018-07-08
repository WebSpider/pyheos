def get_players(command, data):
    """CLI 4.2.1"""

    from datetime import datetime

    return { 'players': data,
             '_refresh_players': datetime.now()
             }


def get_player_info(instance, command, data):
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

    return { 'players': new_player_info,
             '_refresh_players': datetime.now()
             }