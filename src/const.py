"""
Static file of the integration driver.

:copyright: (c) 2025 Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

from datetime import timedelta

__version__ = "1.0.3"

from ucapi.ui import Buttons, DeviceButtonMapping, UiPage

PROJECT_URL = "https://github.com/AkA57/liveboxtvuhd/"
ISSUE_URL = f"{PROJECT_URL}issues"

NAME = "liveboxtvuhd"
STARTUP = f"""
-------------------------------------------------------------------
{NAME}
Version: {__version__}
This is a custom integration.
If you have any issues with this you need to open an issue here:
{ISSUE_URL}
-------------------------------------------------------------------
"""


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
    "GUIDE": 365,
}

REMOTE_BUTTONS_MAPPING: [DeviceButtonMapping] = [
    {"button": Buttons.BACK, "short_press": {"cmd_id": "BACK"}},
    {"button": Buttons.HOME, "short_press": {"cmd_id": "MENU"}},
    {"button": Buttons.CHANNEL_DOWN, "short_press": {"cmd_id": "CH-"}},
    {"button": Buttons.CHANNEL_UP, "short_press": {"cmd_id": "CH+"}},
    {"button": Buttons.DPAD_UP, "short_press": {"cmd_id": "UP"}},
    {"button": Buttons.DPAD_DOWN, "short_press": {"cmd_id": "DOWN"}},
    {"button": Buttons.DPAD_LEFT, "short_press": {"cmd_id": "LEFT"}},
    {"button": Buttons.DPAD_RIGHT, "short_press": {"cmd_id": "RIGHT"}},
    {"button": Buttons.DPAD_MIDDLE, "short_press": {"cmd_id": "OK"}},
    {"button": Buttons.PLAY, "short_press": {"cmd_id": "BACK"}},
    {"button": Buttons.PREV, "short_press": {"cmd_id": "FBWD"}},
    {"button": Buttons.NEXT, "short_press": {"cmd_id": "FFWD"}},
    {"button": Buttons.VOLUME_UP, "short_press": {"cmd_id": "VOL+"}},
    {"button": Buttons.VOLUME_DOWN, "short_press": {"cmd_id": "VOL-"}},
    {"button": Buttons.MUTE, "short_press": {"cmd_id": "MUTE"}},
]

REMOTE_UI_PAGES: [UiPage] = [
    {
        "page_id": "Orange commands",
        "name": "Orange commands",
        "grid": {"width": 4, "height": 6},
        "items": [
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "POWER", "repeat": 1}},
                "icon": "uc:power-on",
                "location": {"x": 0, "y": 0},
                "size": {"height": 1, "width": 1},
                "type": "icon",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "MENU", "repeat": 1}},
                "icon": "uc:home",
                "location": {"x": 1, "y": 0},
                "size": {"height": 1, "width": 1},
                "type": "icon",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "OK", "repeat": 1}},
                "icon": "uc:info",
                "location": {"x": 2, "y": 0},
                "size": {"height": 1, "width": 1},
                "type": "icon",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "REC", "repeat": 1}},
                "icon": "uc:rec",
                "location": {"x": 3, "y": 0},
                "size": {"height": 1, "width": 1},
                "type": "icon",
            },
        ],
    },
    {
        "page_id": "Orange numbers",
        "name": "Orange numbers",
        "grid": {"height": 4, "width": 3},
        "items": [
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "1", "repeat": 1}},
                "location": {"x": 0, "y": 0},
                "size": {"height": 1, "width": 1},
                "text": "1",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "2", "repeat": 1}},
                "location": {"x": 1, "y": 0},
                "size": {"height": 1, "width": 1},
                "text": "2",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "3", "repeat": 1}},
                "location": {"x": 2, "y": 0},
                "size": {"height": 1, "width": 1},
                "text": "3",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "4", "repeat": 1}},
                "location": {"x": 0, "y": 1},
                "size": {"height": 1, "width": 1},
                "text": "4",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "5", "repeat": 1}},
                "location": {"x": 1, "y": 1},
                "size": {"height": 1, "width": 1},
                "text": "5",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "6", "repeat": 1}},
                "location": {"x": 2, "y": 1},
                "size": {"height": 1, "width": 1},
                "text": "6",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "7", "repeat": 1}},
                "location": {"x": 0, "y": 2},
                "size": {"height": 1, "width": 1},
                "text": "7",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "8", "repeat": 1}},
                "location": {"x": 1, "y": 2},
                "size": {"height": 1, "width": 1},
                "text": "8",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "9", "repeat": 1}},
                "location": {"x": 2, "y": 2},
                "size": {"height": 1, "width": 1},
                "text": "9",
                "type": "text",
            },
            {
                "command": {"cmd_id": "remote.send", "params": {"command": "0", "repeat": 1}},
                "location": {"x": 1, "y": 3},
                "size": {"height": 1, "width": 1},
                "text": "0",
                "type": "text",
            },
        ],
    },
]
