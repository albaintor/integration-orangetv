#!/usr/bin/env python
# coding: utf-8
import asyncio
import datetime
from collections import OrderedDict
import json
import logging
from enum import IntEnum

import requests
import calendar

import ucapi.media_player
from dateutil.tz import tz
from fuzzywuzzy import process
from pyee import AsyncIOEventEmitter
from ucapi.media_player import MediaType, Attributes

# from .const import CHANNELS
from const import KEYS, States, MEDIA_PLAYER_STATE_MAPPING
from const import (
    OPERATION_INFORMATION,
    OPERATION_CHANNEL_CHANGE,
    OPERATION_KEYPRESS,
    # EPG_URL,
    # EPG_USER_AGENT,
)

_LOGGER = logging.getLogger(__name__)


class Events(IntEnum):
    """Internal driver events."""

    CONNECTED = 0
    ERROR = 1
    UPDATE = 2
    IP_ADDRESS_CHANGED = 3
    DISCONNECTED = 4


class LiveboxTvUhdClient(object):
    def __init__(self, hostname, port=8080, country="france", timeout=3, refresh_frequency=60, device_id=None):
        from datetime import timedelta

        if device_id is None:
            self.id = hostname
        else:
            self.id = device_id
        self.hostname = hostname
        self.port = port
        self.country = country
        # import const for country
        if self.country == "france":
            from const_france import CHANNELS, EPG_URL, EPG_USER_AGENT, TIMEZONE
        elif self.country == "poland":
            from const_poland import CHANNELS, EPG_URL, EPG_USER_AGENT, TIMEZONE
        self.channels = CHANNELS
        self.epg_url = EPG_URL
        self.epg_user_agent = EPG_USER_AGENT
        self.timeout = timeout
        self.refresh_frequency = timedelta(seconds=refresh_frequency)
        # data from livebox
        self._display_con_err = True
        self._name = None
        self._standby_state = "1"
        self._channel_id = None
        self._osd_context = None
        self._wol_support = None
        self._media_state = None
        self._media_type = None
        self._show_series_title = None
        self._show_season = None
        self._show_episode = None
        # data from woopic.com
        self._channel_name = None
        self._show_title = None
        self._show_definition = None
        self._show_img = None
        self._show_start_dt = 0
        self._show_duration = 0
        self._show_position = 0
        self._last_channel_id = None
        self._cache_channel_img = {}
        self._state = States.UNKNOWN
        loop = asyncio.get_event_loop()
        self.events = AsyncIOEventEmitter(loop or asyncio.get_running_loop())
        self._timezone = tz.gettz(TIMEZONE)

    def refresh_state(self):
        """Refresh the current media state."""
        state = self.media_state
        if state == "PLAY":
            self._state = States.PLAYING
        elif state == "PAUSE":
            self._state = States.PAUSED
        else:
            self._state = States.ON if self.is_on else States.OFF

    def connect(self):
        self.update()
        self.events.emit(Events.CONNECTED, self.id)

    def _find_epg_entry(self, data) -> any:
        if data is None:
            return None
        now = datetime.datetime.now(self._timezone)
        for entry in data:
            show_start_dt = entry["diffusionDate"]
            show_duration = entry["duration"]
            show_start = datetime.datetime.fromtimestamp(show_start_dt, self._timezone)
            show_end = show_start + datetime.timedelta(0, show_duration)
            if show_start <= now < show_end:
                return entry
        return data[0]

    def update(self):
        _LOGGER.debug("Refresh Orange API data")

        update_data = {}
        current_state = self.state
        self._osd_context = None
        self._channel_id = None
        self._media_state = None
        _datalivebox = self.rq_livebox(OPERATION_INFORMATION)
        _data = None
        if _datalivebox:
            self._display_con_err = False
            _data = _datalivebox["result"]["data"]

        if _data:
            standby_state = _data["activeStandbyState"]
            if standby_state != self._standby_state:
                self._standby_state = standby_state

            if "playedMediaState" in _data:
                media_state = _data["playedMediaState"]
                if media_state != self._media_state:
                    self._media_state = media_state

            self._osd_context = _data["osdContext"]
            self._wol_support = _data["wolSupport"]

            if "playedMediaId" in _data:
                self._channel_id = _data["playedMediaId"]
            self.refresh_state()
        else:
            if self._standby_state != "1":
                self._standby_state = "1"
                self.refresh_state()

        # If a channel is displayed
        if self._channel_id and self.get_channel_from_epg_id(self._channel_id):

            current_title = self.show_title
            current_img = self.show_img
            current_position = self.show_position
            current_duration = self.show_duration
            current_channel = self.channel_name

            # We should update all information only if channel or show change
            if self._channel_id != self._last_channel_id or self._show_position > self._show_duration:
                self._last_channel_id = self._channel_id
                self._channel_name = self.get_channel_from_epg_id(self._channel_id)["name"]

                # Reset everything
                self._show_series_title = None
                self._show_season = None
                self._show_episode = None
                self._show_title = None
                self._show_img = None
                self._show_position = 0
                self._show_start_dt = 0

                # Get EPG information
                _data2 = self.rq_epg(self._channel_id)
                if self.country == "france":
                    if _data2 != None and _data2[self._channel_id]:
                        # Show title depending of programType and current time
                        entry = self._find_epg_entry(_data2[self._channel_id])

                        if entry["programType"] == "EPISODE":
                            self._media_type = MediaType.VIDEO
                            self._show_series_title = entry["title"]
                            self._show_season = entry["season"]["number"]
                            if hasattr(entry, "episodeNumber"):
                                self._show_episode = entry["episodeNumber"]
                            else:
                                self._show_episode = 0
                            self._show_title = entry["season"]["serie"]["title"]
                        else:
                            self._media_type = MediaType.TVSHOW
                            self._show_title = entry["title"]

                        self._show_definition = entry["definition"]
                        self._show_start_dt = entry["diffusionDate"]
                        self._show_duration = entry["duration"]
                        if entry["covers"] and len(entry["covers"]) > 1:
                            self._show_img = entry["covers"][1]["url"]
                        elif entry["covers"] and len(entry["covers"]) > 0:
                            self._show_img = entry["covers"][0]["url"]

                elif self.country == "poland":
                    if _data2 != None:
                        for epg in (_data2).get("epg", None):
                            if self._channel_id in epg.get("channelExternalId", None):
                                schedules = epg.get("schedule", None)
                                for sch in schedules:
                                    d = datetime.datetime.utcnow()
                                    if (
                                        sch.get("startDate", None)
                                        <= calendar.timegm(d.utctimetuple())
                                        <= sch.get("endDate", None)
                                    ):
                                        self._show_start_dt = sch.get("startDate", None)
                                        self._show_duration = sch.get("endDate", None) - sch.get("startDate", None)

                                        if sch.get("isSeries", False) == True:
                                            self._media_type = MediaType.VIDEO
                                            self._show_series_title = sch.get("name", None)
                                            self._show_episode = sch.get("episodeNumber", None)
                                            # self._show_title = sch.get("name", None)
                                        else:
                                            self._media_type = MediaType.TVSHOW
                                            self._show_title = sch.get("name", None)

                                        if sch.get("imagePath", None) != None:
                                            self._show_img = "https://tvgo.orange.pl{}".format(
                                                sch.get("imagePath", None)
                                            )

                                        break

                                        # update position if we have show information

            if self._show_start_dt > 0:
                d = datetime.datetime.utcnow()
                self._show_position = calendar.timegm(d.utctimetuple()) - self._show_start_dt

            if current_state != self.state:
                update_data[Attributes.STATE] = MEDIA_PLAYER_STATE_MAPPING.get(self.state, ucapi.media_player.States.UNKNOWN)
            if current_title != self.show_title:
                update_data[Attributes.MEDIA_TITLE] = self.show_title
                update_data[Attributes.MEDIA_TYPE] = self.media_type
            if current_img != self.show_img:
                update_data[Attributes.MEDIA_IMAGE_URL] = self.show_img
                update_data[Attributes.MEDIA_TYPE] = self.media_type
            if current_position != self.show_position:
                update_data[Attributes.MEDIA_POSITION] = self.show_position
            if current_duration != self.show_duration:
                update_data[Attributes.MEDIA_DURATION] = self.show_duration
            if current_channel != self.channel_name:
                update_data[Attributes.SOURCE] = self.channel_name

            if update_data:
                self.events.emit(
                    Events.UPDATE,
                    self.id,
                    update_data
                )


        else:
            # Unknow or no channel displayed. Should be HOMEPAGE, NETFLIX, WHATEVER...
            self._channel_id = -1
            self._last_channel_id = self._channel_id
            self._media_type = MediaType.TVSHOW
            if self._osd_context:
                self._channel_name = self._osd_context.upper()
            self._show_title = None
            self._show_season = None
            self._show_episode = None
            self._show_title = None
            self._show_definition = None
            self._show_img = None
            self._show_start_dt = 0
            self._show_duration = 0
            self._show_position = 0
            if current_state != self.state:
                update_data[Attributes.STATE] = MEDIA_PLAYER_STATE_MAPPING.get(self.state, ucapi.media_player.States.UNKNOWN)
                self.events.emit(
                    Events.UPDATE,
                    self.id,
                    {
                        Attributes.SOURCE: "",
                        Attributes.MEDIA_IMAGE_URL: "",
                        Attributes.MEDIA_TITLE: "",
                        Attributes.MEDIA_POSITION: 0,
                        Attributes.MEDIA_DURATION: 0,
                        Attributes.MEDIA_TYPE: MediaType.TVSHOW,
                        Attributes.STATE: self.state,
                    },
                )
        return _data

    @property
    def state(self):
        return self._state

    @property
    def name(self):
        return self._name

    @property
    def standby_state(self):
        return self._standby_state == "0"

    @property
    def channel_id(self):
        return self._channel_id

    @property
    def osd_context(self):
        return self._osd_context

    @property
    def media_state(self):
        return self._media_state

    @property
    def media_type(self):
        return self._media_type

    @property
    def show_series_title(self):
        return self._show_series_title

    @property
    def show_season(self):
        return self._show_season

    @property
    def show_episode(self):
        return self._show_episode

    @property
    def wol_support(self):
        return self._wol_support == "0"

    @property
    def channel_name(self):
        return self._channel_name

    @channel_name.setter
    def channel_name(self, value):
        self.set_channel_by_name(value)

    @property
    def channel_names(self):
        channel_names = []
        for channel in self.channels:
            channel_names.append(channel.get("name"))
        return channel_names

    @property
    def show_title(self):
        return self._show_title

    @property
    def show_definition(self):
        return self._show_definition

    @property
    def show_img(self):
        return self._show_img

    @property
    def show_start_dt(self):
        return self._show_start_dt

    @property
    def show_duration(self):
        return self._show_duration

    @property
    def show_position(self):
        return self._show_position

    @property
    def is_on(self):
        return self.standby_state

    @property
    def info(self):
        return self.update()

    # TODO
    @staticmethod
    def discover():
        pass

    def get_channels(self):
        return self.channels

    async def async_turn_on(self):
        if not self.standby_state:
            self.press_key(key=KEYS["POWER"])
            await asyncio.sleep(2)
            self.press_key(key=KEYS["OK"])

    def turn_on(self):
        if not self.standby_state:
            asyncio.create_task(self.async_turn_on())

    def turn_off(self):
        if self.standby_state:
            return self.press_key(key=KEYS["POWER"])

    def __get_key_name(self, key_id):
        for key_name, k_id in KEYS.items():
            if k_id == key_id:
                return key_name

    def press_key(self, key, mode=0):
        """
        modes:
            0 -> simple press
            1 -> long press
            2 -> release after long press
        """
        if isinstance(key, str):
            assert key in KEYS, "No such key: {}".format(key)
            key = KEYS[key]
        _LOGGER.debug("Press key %s", self.__get_key_name(key))
        return self.rq_livebox(OPERATION_KEYPRESS, OrderedDict([("key", key), ("mode", mode)]))

    def volume_up(self):
        return self.press_key(key=KEYS["VOL+"])

    def volume_down(self):
        return self.press_key(key=KEYS["VOL-"])

    def mute(self):
        return self.press_key(key=KEYS["MUTE"])

    def channel_up(self):
        return self.press_key(key=KEYS["CH+"])

    def channel_down(self):
        return self.press_key(key=KEYS["CH-"])

    def play_pause(self):
        return self.press_key(key=KEYS["PLAY/PAUSE"])

    def play(self):
        if self.media_state == "PAUSE":
            return self.play_pause()
        _LOGGER.debug("Media is already playing.")

    def pause(self):
        if self.media_state == "PLAY":
            return self.play_pause()
        _LOGGER.debug("Media is already paused.")

    def get_channel_names(self, json_output=False):
        channels = [x["name"] for x in self.channels]
        return json.dumps(channels) if json_output else channels

    def get_channel_info(self, channel):
        # If the channel start with '#' search by channel number
        channel_index = None
        if channel.startswith("#"):
            channel_index = channel.split("#")[1]
        # Look for an exact match first
        for chan in self.channels:
            if channel_index:
                if chan["index"] == channel_index:
                    return chan
            else:
                if chan["name"].lower() == channel.lower():
                    return chan
        # Try fuzzy matching it that did not give any result
        chan = process.extractOne(channel, self.channels)[0]
        return chan

    def get_channel_id_from_name(self, channel):
        return self.get_channel_info(channel)["epg_id"]

    def get_channel_from_epg_id(self, epg_id):
        res = [c for c in self.channels if c["epg_id"] == epg_id]
        return res[0] if res else None

    def set_channel_by_id(self, epg_id):
        # The EPG ID needs to be 10 chars long, padded with '*' chars
        epg_id_str = str(epg_id).rjust(10, "*")
        _LOGGER.debug("Tune to channel %s, epg_id %s", self.get_channel_from_epg_id(epg_id)["name"], epg_id_str)
        return self.rq_livebox(OPERATION_CHANNEL_CHANGE, OrderedDict([("epg_id", epg_id_str), ("uui", "1")]))

    def set_channel_by_name(self, channel):
        epg_id = self.get_channel_id_from_name(channel)
        return self.set_channel_by_id(epg_id)

    def rq_livebox(self, operation, params=None):
        url = "http://{}:{}/remoteControl/cmd".format(self.hostname, self.port)
        get_params = OrderedDict({"operation": operation})
        _LOGGER.debug("Request Livebox operation %s", operation)
        if params:
            get_params.update(params)
        try:
            r = requests.get(url, params=get_params, timeout=self.timeout)
            r.raise_for_status()
            _LOGGER.debug("Livebox response: %s", r.json())
            return r.json()
        except requests.exceptions.RequestException as err:
            self._standby_state = "1"
            if self._display_con_err:
                self._display_con_err = False
                _LOGGER.error(err)
        except requests.exceptions.HTTPError as errh:
            self._standby_state = "1"
            if self._display_con_err:
                self._display_con_err = False
                _LOGGER.error(errh)
        except requests.exceptions.ConnectionError as errc:
            self._standby_state = "1"
            if self._display_con_err:
                self._display_con_err = False
                _LOGGER.error(errc)
        except requests.exceptions.Timeout as errt:
            self._standby_state = "1"
            if self._display_con_err:
                self._display_con_err = False
                _LOGGER.error(errt)

    def rq_epg(self, channel_id):
        if self.country == "france":
            get_params = OrderedDict({"groupBy": "channel", "period": "current", "epgIds": channel_id, "mco": "OFR"})
        elif self.country == "poland":
            get_params = OrderedDict({"hhTech": "", "deviceCat": "otg"})
        _LOGGER.debug("Request EPG channel id %s", channel_id)
        try:
            headers = {"User-Agent": self.epg_user_agent}
            r = requests.get(self.epg_url, headers=headers, params=get_params, timeout=self.timeout)
            r.raise_for_status()
            _LOGGER.debug("EPG response: %s", r.json())
            return r.json()
        except requests.exceptions.RequestException as err:
            _LOGGER.error("EPG response: %s", err)
            pass
        except requests.exceptions.HTTPError as errh:
            _LOGGER.error("EPG response: %s", errh)
            pass
        except requests.exceptions.ConnectionError as errc:
            _LOGGER.error("EPG response: %s", errc)
            pass
        except requests.exceptions.Timeout as errt:
            _LOGGER.error("EPG response: %s", errt)
            pass
