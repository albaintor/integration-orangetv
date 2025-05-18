#!/usr/bin/env python
# coding: utf-8
"""
This module implements the Orange TV communication of the Remote Two integration driver.

:copyright: (c) Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""
# pylint: skip-file
import asyncio
import logging
import sys

from rich import print_json

from client import LiveboxTvUhdClient
from config import DeviceInstance
from const import OPERATION_INFORMATION

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
_LOOP = asyncio.new_event_loop()
asyncio.set_event_loop(_LOOP)


async def main():
    _LOG.debug("Start connection")
    client = LiveboxTvUhdClient(
        device_config=DeviceInstance(
            id="deviceid", name="LiveboxUHD", address="192.168.1.129", port=8080, country="france", always_on=False
        )
    )
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
