# Constant variables go here

# Supported music services
SERVICE_PANDORA = 1
SERVICE_RHAPSODY = 2
SERVICE_TUNEIN = 3
SERVICE_SPOTIFY = 4
SERVICE_DEEZER = 5
SERVICE_NAPSTER = 6
SERVICE_IHEARTRADIO = 7
SERVICE_SIRIUSXM = 8
SERVICE_SOUNDCLOUD = 9
SERVICE_TIDAL = 10
SERVICE_FUTURE = 11
SERVICE_RDIO = 12
SERVICE_AMAZON = 13
SERVICE_FUTURE_2 = 14
SERVICE_MOODMIX = 15
SERVICE_JUKE = 16
SERVICE_FUTURE_3 = 17
SERVICE_QQ = 18

# Music sources
SOURCE_LOCALUSB = 1024
SOURCE_HEOS_PLAYLIST = 1025
SOURCE_HEOS_HISTORY = 1026
SOURCE_HEOS_AUX = 1027
SOURCE_HEOS_FAVORITES = 1028

# HEOS Defaults
HEOS_PORT = 1255
HEOS_ST_NAME = 'urn:schemas-denon-com:device:ACT-Denon:1'

# UPNP Defaults
SSDP_HOST = '239.255.255.250'
SSDP_PORT = 1900

# Credentials
HEOS_USERNAME = 'dummy'
HEOS_PASSWORD = 'denon'

# Commands
COMMAND_REGISTRY = {
    'CMD_REGISTER_CHANGE_EVENTS': 'system/register_for_change_events',
    'CMD_HEOS_ACCOUNT_CHECK': 'system/check_account',
    'CMD_HEOS_ACCOUNT_SIGNIN': 'system/sign_in',
    'CMD_HEOS_ACCOUNT_SIGNOUT': 'system/sign_out',
    'CMD_HEOS_HEARTBEAT': 'system/heart_beat',
    'CMD_HEOS_REBOOT': 'system/reboot',
    'CMD_PRETTIFY_JSON': 'system/prettfy_json_response',
    'CMD_GET_PLAYERS': 'player/get_players',
    'CMD_GET_PLAYER_INFO': 'player/get_player_info',
    'CMD_GET_PLAY_STATE': 'player/get_play_state',
    'CMD_SET_PLAY_STATE': 'player/set_play_state',
    'CMD_GET_NOW_PLAYING': 'player/get_now_playing_media',
    'CMD_GET_VOLUME': 'player/get_volume',
    'CMD_SET_VOLUME': 'player/set_volume',
    'CMD_VOLUME_UP': 'player/volume_up',
    'CMD_VOLUME_DOWN': 'player/volume_down',
    'CMD_GET_MUTE': 'player/get_mute',
    'CMD_SET_MUTE': 'player/set_mute',
    'CMD_TOGGLE_MUTE': 'player/toggle_mute',
    'CMD_GET_PLAY_MODE': 'player/get_play_mode',
    'CMD_SET_PLAY_MODE': 'player/set_play_mode',
    'CMD_GET_QUEUE': 'player/get_queue',
    'CMD_PLAY_QUEUE_ITEM': 'player/play_queue',
    'CMD_REMOVE_FROM_QUEUE': 'player/remove_from_queue',
    'CMD_SAVE_QUEUE_AS_PLAYLIST': 'player/save_queue',
    'CMD_CLEAR_QUEUE': 'player/clear_queue',
    'CMD_MOVE_TO_QUEUE': 'player/move_queue_item',
    'CMD_PLAY_NEXT': 'player/play_next',
    'CMD_PLAY_PREV': 'player/play_previous',
    'CMD_SET_QUICKSELECT': 'player/set_quickselect',
    'CMD_PLAY_QUICKSELECT': 'player/play_quickselect',
    'CMD_GET_QUICKSELECTS': 'player/get_quickselects',
    'CMD_CHECK_FW_UPDATE': 'player/check_update',
    'CMD_GET_GROUPS': 'player/get_groups',
    'CMD_GET_GROUP_INFO': 'group/get_group_info',
    'CMD_SET_GROUP': 'group/set_group',
    'CMD_GET_GROUP_VOLUME': 'group/get_volume',
    'CMD_SET_GROUP_VOLUME': 'group/set_volume',
    'CMD_GROUP_VOLUME_UP': 'group/volume_up',
    'CMD_GROUP_VOLUME_DOWN': 'group/volume_down',
    'CMD_GET_GROUP_MUTE': 'group/get_mute',
    'CMD_SET_GROUP_MUTE': 'group/set_mute',
    'CMD_TOGGLE_GROUP_MUTE': 'group/toggle_mute',
    'CMD_'
}
