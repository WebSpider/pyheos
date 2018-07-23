from pyheos import HEOSException, get_message_parts
import sys


def get_groups(heosobj, command, data):
    """CLI 4.3.1"""

    from datetime import datetime

    heosobj.save_groups(data, datetime.now())


def get_group_info(heosobj, command, data):
    """CLI 4.3.2"""

    from datetime import datetime

    old_groups = heosobj._groups
    new_groups = {}
    if old_groups:
        new_info_gid = data['gid']

        for group in old_groups:
            if group['gid'] == new_info_gid:
                new_groups.update(data)
            else:
                new_groups.update(group)
    else:
        new_groups.update(data)

    heosobj.save_groups(new_groups, datetime.now())


def set_group(heosobj, command, data):
    """CLI 4.3.3"""

    from datetime import datetime

    parts = get_message_parts(data, ['pid', 'gid', 'name'])
    player_list = parts['pid']
    new_group = parts['gid']
    new_group_name = parts['name']

    old_groups = heosobj._groups

    new_groups = {}

    for group in old_groups:
        new_groups.update(group)
        if group['gid'] == new_group:
            new_groups.update({'gid': new_group,
                               'pid': player_list,
                               'name': new_group_name})

    heosobj.save_groups(new_groups, datetime.now())


def get_group_volume(heosobj, command, data):
    """CLI 4.3.4"""

    from datetime import datetime

    parts = get_message_parts(data, ['gid', 'level'])
    group_id = parts['gid']
    volumelevel = parts['level']

    old_groups = heosobj._groups
    new_groups = {}

    for group in old_groups:
        new_groups.update(group)
        if group['gid'] == group_id:
            new_groups.update({'gid': group_id,
                               'level': volumelevel})

    heosobj.save_groups(new_groups, datetime.now())


def set_group_volume(heosobj, command, data):
    """CLI 4.3.5"""

    get_group_volume(heosobj, command, data)


def volume_up(heosobj, command, data):
    """CLI 4.3.6"""

    from datetime import datetime

    parts = get_message_parts(data, ['gid', 'step'])
    group_id = parts['gid']
    step_up = parts['step']

    old_groups = heosobj._groups
    new_groups = {}

    for group in old_groups:
        new_groups.update(group)
        if group['gid'] == group_id:
            new_groups.update({'gid': group_id,
                               'step': step_up})

    heosobj.save_groups(new_groups, datetime.now())

def volume_down(heosobj, command, data):
    """CLI 4.3.7"""

    from datetime import datetime

    parts = get_message_parts(data, ['gid', 'step'])
    group_id = parts['gid']
    step_down = parts['step']

    old_groups = heosobj._groups
    new_groups = {}

    for group in old_groups:
        new_groups.update(group)
        if group['gid'] == group_id:
            new_groups.update({'gid': group_id,
                               'step': step_down})

    heosobj.save_groups(new_groups, datetime.now())


def get_mute(heosobj, command, data):
    """CLI 4.3.8"""

    from datetime import datetime

    parts = get_message_parts(data, ['gid', 'state'])
    state = parts['state']
    group_id = parts['gid']

    old_groups = heosobj._groups
    new_groups = {}

    for group in old_groups:
        new_groups.update(group)
        if group['gid'] == group_id:
            new_groups.update({'gid': group_id,
                               'state': state})

    heosobj.save_groups(new_groups, datetime.now())
