"""
Media-player entity functions.

:copyright: (c) 2023 by Unfolded Circle ApS.
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

import logging
from typing import Any

import ucapi.media_player
from ucapi import EntityTypes, Sensor
from ucapi.media_player import States as MediaStates
from ucapi.sensor import Attributes, DeviceClasses, Options, States

import client
from config import OrangeConfigDevice, OrangeEntity, create_entity_id
from const import OrangeSensors

_LOG = logging.getLogger(__name__)

SENSOR_STATE_MAPPING = {
    MediaStates.OFF: States.UNAVAILABLE,
    MediaStates.ON: States.ON,
    MediaStates.STANDBY: States.ON,
    MediaStates.PLAYING: States.ON,
    MediaStates.PAUSED: States.ON,
    MediaStates.UNAVAILABLE: States.UNAVAILABLE,
    MediaStates.UNKNOWN: States.UNKNOWN,
}


# pylint: disable=R0917
class OrangeSensor(OrangeEntity, Sensor):
    """Representation of a Kodi Sensor entity."""

    def __init__(
        self,
        entity_id: str,
        name: str | dict[str, str],
        config_device: OrangeConfigDevice,
        device: client.OrangeTVClient,
        options: dict[Options, Any] | None = None,
        device_class: DeviceClasses = DeviceClasses.CUSTOM,
    ) -> None:
        """Initialize the class."""
        # pylint: disable = R0801
        self._device: client.OrangeTVClient = device
        features = []
        attributes = dict[Any, Any]()
        self._config_device = config_device
        self._state: States = States.UNAVAILABLE
        super().__init__(entity_id, name, features, attributes, device_class=device_class, options=options)

    @property
    def deviceid(self) -> str:
        """Return the device identifier."""
        return self._device.id

    def update_attributes(self, update: dict[str, Any] | None = None) -> dict[str, Any]:
        """Return the updated attributes of current sensor entity."""
        raise NotImplementedError()


class OrangeSensorChannel(OrangeSensor):
    """Current channel sensor entity."""

    ENTITY_NAME = "sensor_channel"

    def __init__(self, config_device: OrangeConfigDevice, device: client.OrangeTVClient):
        """Initialize the class."""
        entity_id = f"{create_entity_id(config_device.id, EntityTypes.SENSOR)}.{OrangeSensorChannel.ENTITY_NAME}"
        # TODO : dict instead of name to report language names
        self._device = device
        self._config_device = config_device
        super().__init__(
            entity_id,
            {"en": f"{config_device.get_device_part()}Channel", "fr": f"{config_device.get_device_part()}Chaîne"},
            config_device,
            device,
        )

    def update_attributes(self, update: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """Return updated sensor value from full update if provided or sensor value if no udpate is provided."""
        attributes: dict[str, Any] = {}
        if update:
            if ucapi.media_player.Attributes.STATE in update:
                attributes[Attributes.STATE] = SENSOR_STATE_MAPPING.get(update[ucapi.media_player.Attributes.STATE])
            if OrangeSensors.SENSOR_CHANNEL in update:
                attributes[Attributes.VALUE] = update[OrangeSensors.SENSOR_CHANNEL]
            return attributes
        return {
            Attributes.VALUE: self._device.channel_name,
            Attributes.STATE: SENSOR_STATE_MAPPING.get(self._device.state),
        }


class OrangeSensorMediaTitle(OrangeSensor):
    """Current media title sensor entity."""

    ENTITY_NAME = "sensor_media_title"

    def __init__(self, config_device: OrangeConfigDevice, device: client.OrangeTVClient):
        """Initialize the class."""
        entity_id = f"{create_entity_id(config_device.id, EntityTypes.SENSOR)}.{OrangeSensorMediaTitle.ENTITY_NAME}"
        # TODO : dict instead of name to report language names
        self._device = device
        self._config_device = config_device
        super().__init__(
            entity_id,
            {
                "en": f"{config_device.get_device_part()}Media title",
                "fr": f"{config_device.get_device_part()}Programme",
            },
            config_device,
            device,
        )

    def update_attributes(self, update: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """Return updated sensor value from full update if provided or sensor value if no udpate is provided."""
        attributes: dict[str, Any] = {}
        if update:
            if ucapi.media_player.Attributes.STATE in update:
                attributes[Attributes.STATE] = SENSOR_STATE_MAPPING.get(update[ucapi.media_player.Attributes.STATE])
            if OrangeSensors.SENSOR_MEDIA_TITLE in update:
                attributes[Attributes.VALUE] = update[OrangeSensors.SENSOR_MEDIA_TITLE]
            return attributes
        return {
            Attributes.VALUE: self._device.show_title,
            Attributes.STATE: SENSOR_STATE_MAPPING.get(self._device.state),
        }


class OrangeSensorMediaEpisode(OrangeSensor):
    """Current media episode sensor entity."""

    ENTITY_NAME = "sensor_media_episode"

    def __init__(self, config_device: OrangeConfigDevice, device: client.OrangeTVClient):
        """Initialize the class."""
        entity_id = f"{create_entity_id(config_device.id, EntityTypes.SENSOR)}.{OrangeSensorMediaEpisode.ENTITY_NAME}"
        # TODO : dict instead of name to report language names
        self._device = device
        self._config_device = config_device
        super().__init__(
            entity_id,
            {"en": f"{config_device.get_device_part()}Episode", "fr": f"{config_device.get_device_part()}Episode"},
            config_device,
            device,
        )

    def update_attributes(self, update: dict[str, Any] | None = None) -> dict[str, Any] | None:
        """Return updated sensor value from full update if provided or sensor value if no udpate is provided."""
        attributes: dict[str, Any] = {}
        if update:
            if ucapi.media_player.Attributes.STATE in update:
                attributes[Attributes.STATE] = SENSOR_STATE_MAPPING.get(update[ucapi.media_player.Attributes.STATE])
            if OrangeSensors.SENSOR_MEDIA_EPISODE in update:
                attributes[Attributes.VALUE] = update[OrangeSensors.SENSOR_MEDIA_EPISODE]
            return attributes
        return {
            Attributes.VALUE: self._device.show_episode,
            Attributes.STATE: SENSOR_STATE_MAPPING.get(self._device.state),
        }
