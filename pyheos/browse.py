from pyheos import get_message_parts, HEOSException

VALID_SOURCE_TYPES = ['music_service', 'heos_service', 'heos_server', 'dlna_server']


def get_music_sources(heosobj, command, data):
    """CLI 4.4.1"""

    sources = data
    filtered_sources = []

    for source in sources:
        if source.type in VALID_SOURCE_TYPES:
            filtered_sources.append(source)
        else:
            raise HEOSException(message='{} is not a valid source type ({})'.format(source.type, source.name),errid=441)


    heosobj._sources = list(filtered_sources)

    return filtered_sources


def get_source_info(heosobj, command, data):
    """CLI 4.4.2"""

    newsource = data
    oldsources = heosobj._sources
    processed_sources = []

    if newsource.type in VALID_SOURCE_TYPES:
        for src in oldsources:
            if src.sid == newsource.sid:
                processed_sources.append(newsource)
            else:
                processed_sources.append(src)
    else:
        raise HEOSException(message='{} is not a valid source type ({})'.format(newsource.type, newsource.name),errid=442)

    heosobj._sources = list(processed_sources)

    return newsource


def browse_source(heosobj, command, data):
    """CLI 4.4.3"""

    raise NotImplementedError


def browse_container(heosobj, command, data):
    """CLI 4.4.4"""

    raise NotImplementedError


def get_search_criteria(heosobj, command, data):
    """CLI 4.4.5"""

    return data


def search(heosobj, command, data):
    """CLI 4.4.6"""

    raise NotImplementedError


def play_stream(heosobj, command, data):
    """CLI 4.4.7"""

    parts = get_message_parts(data, ['pid', 'sid', 'cid', 'mid', 'name'])

    heosobj._cur_play_state = parts

    return parts


def play_preset(heosobj, command, data):
    """CLI 4.4.8"""

    parts = get_message_parts(data, ['pid', 'preset'])

    heosobj._cur_play_state = parts

    return parts


def play_input(heosobj, command, data):
    """CLI 4.4.9"""

    parts = get_message_parts(data, ['sid', 'pid', 'mid', 'spid', 'input'])

    heosobj._cur_play_state = parts

    return parts


def play_url(heosobj, command, data):
    """CLI 4.4.10"""

    parts = get_message_parts(data, ['pid', 'url'])

    heosobj._cur_play_state = parts

    return parts


def add_cnt_to_queue(heosobj, command, data):
    """CLI 4.4.11"""

    parts = get_message_parts(data, ['sid', 'cid', 'aid', 'pid'])

    heosobj._cur_play_state = parts

    return parts


def add_track_to_queue(heosobj, command, data):
    """CLI 4.4.12"""

    parts = get_message_parts(data, ['sid', 'cid', 'mid', 'aid', 'pid'])

    heosobj._cur_play_state = parts

    return parts


def get_playlists(heosobj, command, data):
    """CLI 4.4.13"""

    pass


def rename_playlist(heodobj, command, data):
    """CLI 4.4.14"""

    parts = get_message_parts(data, ['sid', 'cid', 'name'])

    return parts


def delete_playlist(heosobj, command, data):
    """CLI 4.4.15"""

    parts = get_message_parts(data, ['sid', 'cid'])

    return parts


def get_heos_history(heosobj, command, data):
    """CLI 4.4.16"""

    pass


def retrieve_metedata(heosobj, command, data):
    """CLI 4.4.17"""

    raise NotImplementedError


def get_service_options(heosobj, command, data):
    """CLI 4.4.18"""

    pass


def set_service_option(heosobj, command, data):
    """CLI 4.4.19"""

    raise NotImplementedError
