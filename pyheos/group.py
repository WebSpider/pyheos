from pyheos import HEOSException, get_message_parts
import sys


def get_groups(heosobj, command, data):
    """CLI 4.3.1"""

    from datetime import datetime

    setattr(heosobj, "_groups", data)
    setattr(heosobj, "_refresh_groups", datetime.now())


def get_group_info(heosobj, command, data):
    """CLI 4.3.2"""

    from datetime import datetime

    old_groups = heosobj._groups
    if old_groups:
        new_groups = {}
        new_info_gid = data['gid']

        for group in old_groups:
            if group['gid'] == new_info_gid:
                new_groups.update(data)
            else:
                new_groups.update(group)
    else:
        new_groups.update(data)

    setattr(heosobj, "_groups", new_groups)
    setattr(heosobj, "_refresh_groups", datetime.now())


def set_group(heosobj, commnd, data):
    """CLI 4.3.3"""

    parts = get_message_parts(data, ['gid'])

