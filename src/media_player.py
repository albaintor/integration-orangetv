"""
Media-player entity functions.

:copyright: (c) 2025 Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

import logging
from typing import Any

from ucapi import EntityTypes, MediaPlayer, StatusCodes
from ucapi.media_player import (
    Attributes,
    Commands,
    DeviceClasses,
    Features,
    MediaType,
)

from client import OrangeTVClient
from config import OrangeConfigDevice, OrangeEntity, create_entity_id

_LOG = logging.getLogger(__name__)


class OrangeMediaPlayer(MediaPlayer, OrangeEntity):
    """Representation of a Sony Media Player entity."""

    # pylint: disable=R0915,R0903
    def __init__(self, config_device: OrangeConfigDevice, device: OrangeTVClient):
        """Initialize the class."""
        self._device = device

        entity_id = create_entity_id(config_device.id, EntityTypes.MEDIA_PLAYER)
        features = [
            Features.ON_OFF,
            Features.TOGGLE,
            Features.VOLUME_UP_DOWN,
            Features.MUTE_TOGGLE,
            Features.SELECT_SOURCE,
            Features.MEDIA_TITLE,
            Features.MEDIA_IMAGE_URL,
            Features.MEDIA_TYPE,
            Features.PLAY_PAUSE,
            Features.DPAD,
            Features.SETTINGS,
            Features.STOP,
            Features.FAST_FORWARD,
            Features.REWIND,
            Features.RECORD,
            Features.MENU,
            Features.NUMPAD,
            Features.CHANNEL_SWITCHER,
            Features.MEDIA_POSITION,
            Features.MEDIA_DURATION,
        ]
        # pylint: disable=R0801
        attributes = {
            Attributes.STATE: device.state,
            Attributes.SOURCE: device.channel_name if device.channel_name else "",
            Attributes.SOURCE_LIST: device.channel_names,
            Attributes.MEDIA_IMAGE_URL: device.show_img if device.show_img else "",
            Attributes.MEDIA_TITLE: device.show_title if device.show_title else "",
            Attributes.MEDIA_ARTIST: device.channel_episode if device.channel_episode else "",
            Attributes.MEDIA_POSITION: device.show_position,
            Attributes.MEDIA_DURATION: device.show_duration,
            Attributes.MEDIA_TYPE: device.media_type if device.media_type else MediaType.TVSHOW,
        }

        super().__init__(
            entity_id,
            config_device.name,
            features,
            attributes,
            device_class=DeviceClasses.SET_TOP_BOX,
        )

    @property
    def deviceid(self) -> str:
        """Return the device identifier."""
        return self._device.id

    async def command(self, cmd_id: str, params: dict[str, Any] | None = None, *, websocket: Any) -> StatusCodes:
        """
        Media-player entity command handler.

        Called by the integration-API if a command is sent to a configured media-player entity.

        :param cmd_id: command
        :param params: optional command parameters
        :param websocket: optional websocket connection. Allows for directed event
                          callbacks instead of broadcasts.
        :return: status code of the command request
        """
        # pylint: disable = R0915
        _LOG.info("Got %s command request: %s %s", self.id, cmd_id, params)

        if self._device is None:
            _LOG.warning("No device instance for entity: %s", self.id)
            return StatusCodes.SERVICE_UNAVAILABLE

        if cmd_id == Commands.VOLUME_UP:
            res = await self._device.volume_up()
        elif cmd_id == Commands.VOLUME_DOWN:
            res = await self._device.volume_down()
        elif cmd_id == Commands.MUTE_TOGGLE:
            res = await self._device.mute()
        elif cmd_id == Commands.ON:
            await self._device.turn_on()
            return StatusCodes.OK
        elif cmd_id == Commands.OFF:
            await self._device.turn_off()
            return StatusCodes.OK
        elif cmd_id == Commands.TOGGLE:
            await self._device.press_key("POWER")
            return StatusCodes.OK
        elif cmd_id == Commands.SELECT_SOURCE:
            res = await self._device.set_channel_by_name(params.get("source"))
        elif cmd_id == Commands.CHANNEL_UP:
            res = await self._device.channel_up()
        elif cmd_id == Commands.CHANNEL_DOWN:
            res = await self._device.channel_down()
        elif cmd_id == Commands.PLAY_PAUSE:
            res = await self._device.play_pause()
        elif cmd_id == Commands.FAST_FORWARD:
            res = await self._device.press_key("FFWD")
        elif cmd_id == Commands.REWIND:
            res = await self._device.press_key("FBWD")
        elif cmd_id == Commands.RECORD:
            res = await self._device.press_key("REC")
        elif cmd_id == Commands.CURSOR_UP:
            res = await self._device.press_key("UP")
        elif cmd_id == Commands.CURSOR_DOWN:
            res = await self._device.press_key("DOWN")
        elif cmd_id == Commands.CURSOR_LEFT:
            res = await self._device.press_key("LEFT")
        elif cmd_id == Commands.CURSOR_RIGHT:
            res = await self._device.press_key("RIGHT")
        elif cmd_id == Commands.CURSOR_ENTER:
            res = await self._device.press_key("OK")
        elif cmd_id == Commands.BACK:
            res = await self._device.press_key("BACK")
        elif cmd_id == Commands.MENU:
            res = await self._device.press_key("MENU")
        elif cmd_id == Commands.MY_RECORDINGS:
            res = await self._device.press_key("VOD")
        elif cmd_id == Commands.DIGIT_0:
            res = await self._device.press_key("0")
        elif cmd_id == Commands.DIGIT_1:
            res = await self._device.press_key("1")
        elif cmd_id == Commands.DIGIT_2:
            res = await self._device.press_key("2")
        elif cmd_id == Commands.DIGIT_3:
            res = await self._device.press_key("3")
        elif cmd_id == Commands.DIGIT_4:
            res = await self._device.press_key("4")
        elif cmd_id == Commands.DIGIT_5:
            res = await self._device.press_key("5")
        elif cmd_id == Commands.DIGIT_6:
            res = await self._device.press_key("6")
        elif cmd_id == Commands.DIGIT_7:
            res = await self._device.press_key("7")
        elif cmd_id == Commands.DIGIT_8:
            res = await self._device.press_key("8")
        elif cmd_id == Commands.DIGIT_9:
            res = await self._device.press_key("9")
        else:
            return StatusCodes.NOT_IMPLEMENTED
        return res
