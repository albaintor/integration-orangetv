#!/usr/bin/env python
# coding: utf-8
"""
This module implements the Orange TV communication of the Remote Two integration driver.

:copyright: (c) Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""
# pylint: skip-file
# flake8: noqa
import asyncio
import logging
import sys
from typing import Any

from rich import print_json

from client import LiveboxTvUhdClient, Events
from config import DeviceInstance
from const import OPERATION_INFORMATION


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
_LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(_LOOP)

#192.168.1.123
#192.168.0.8

#OLD 192.168.1.35

async def on_device_update(device_id: str, update: dict[str, Any] | None) -> None:
    print_json(data=update)

async def main():
    _LOG.debug("Start connection")
    client = LiveboxTvUhdClient(
        device_config=DeviceInstance(#192.168.1.129 192.168.1.132
            id="deviceid", name="LiveboxUHD", address="192.168.0.8", port=8080, country="france", always_on=False
        )
    )
    client.events.on(Events.UPDATE, on_device_update)
    await client.connect()
    for i in range(100):
        # _LOG.debug("INFO %s %s", client.media_state, client.attributes)
        # print_json(data=client.media_state)
        print_json(data=client.attributes)
        _datalivebox = await client.rq_livebox(OPERATION_INFORMATION)
        print_json(data=_datalivebox)
        # await client.set_channel_by_name("M6 4K")
        # await client.set_channel_by_name("NICKELODEON JUNIOR")
        await asyncio.sleep(10)


if __name__ == "__main__":
    _LOG = logging.getLogger(__name__)
    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    logging.basicConfig(handlers=[ch])
    logging.getLogger("client").setLevel(logging.DEBUG)
    logging.getLogger("test_connection").setLevel(logging.DEBUG)
    _LOOP.run_until_complete(main())
    _LOOP.run_forever()
