from datetime import timedelta

__version__ = "1.0.4"

from enum import IntEnum

import ucapi

PROJECT_URL = "https://github.com/AkA57/liveboxtvuhd/"
ISSUE_URL = "{}issues".format(PROJECT_URL)

NAME = "liveboxtvuhd"
STARTUP = """
-------------------------------------------------------------------
{}
Version: {}
This is a custom integration.
If you have any issues with this you need to open an issue here:
{}
-------------------------------------------------------------------
""".format(
    NAME, __version__, ISSUE_URL
)


class States(IntEnum):
    """State of a connected devoce."""

    UNKNOWN = 0
    UNAVAILABLE = 1
    OFF = 2
    ON = 3
    PLAYING = 4
    PAUSED = 5


# Mapping of a device state to a media-player entity state
MEDIA_PLAYER_STATE_MAPPING: dict[States, ucapi.media_player.States] = {
    States.ON: ucapi.media_player.States.ON,
    States.OFF: ucapi.media_player.States.OFF,
    States.PAUSED: ucapi.media_player.States.PAUSED,
    States.PLAYING: ucapi.media_player.States.PLAYING,
    States.UNAVAILABLE: ucapi.media_player.States.UNAVAILABLE,
    States.UNKNOWN: ucapi.media_player.States.UNKNOWN,
}

SCAN_INTERVAL = timedelta(seconds=10)
MIN_TIME_BETWEEN_SCANS = SCAN_INTERVAL
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=1)
DEFAULT_NAME = "liveboxtvuhd"
DEFAULT_PORT = 8080
CONF_COUNTRY = "country"
DEFAULT_COUNTRY = "france"


# Livebox operation
OPERATION_INFORMATION = "10"
OPERATION_CHANNEL_CHANGE = "09"
OPERATION_KEYPRESS = "01"

KEYS = {
    "POWER": 116,
    "0": 512,
    "1": 513,
    "2": 514,
    "3": 515,
    "4": 516,
    "5": 517,
    "6": 518,
    "7": 519,
    "8": 520,
    "9": 521,
    "CH+": 402,
    "CH-": 403,
    "VOL+": 115,
    "VOL-": 114,
    "MUTE": 113,
    "UP": 103,
    "DOWN": 108,
    "LEFT": 105,
    "RIGHT": 106,
    "OK": 352,
    "BACK": 158,
    "MENU": 139,
    "PLAY/PAUSE": 164,
    "FBWD": 168,
    "FFWD": 159,
    "REC": 167,
    "VOD": 393,
}
