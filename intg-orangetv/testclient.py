import asyncio
import calendar
import datetime
import importlib
import json
import socket
from collections import OrderedDict

import logging

import aiohttp
import netifaces
import requests
from ssdp import aio, messages, network
import socket
from rich import print, print_json

_LOGGER = logging.getLogger(__name__)

EPG_URL = "https://rp-ott-mediation-tv.woopic.com/api-gw/live/v3/applications/STB4PC/programs"
EPG_USER_AGENT = "Opera/9.80 (Linux i686; U; fr) Presto/2.10.287 Version/12.00 ; SC/IHD92 STB"

# module = importlib.import_module("intg-orangetv.client")
# print(module)
# exit(0)
# LiveboxTvUhdClient = getattr(module, "LiveboxTvUhdClient")
from client import LiveboxTvUhdClient

class MyProtocol(aio.SimpleServiceDiscoveryProtocol):

    def response_received(self, response, addr):
        print(response, addr)

    def request_received(self, request, addr):
        print(request, addr)

async def get_epg():
    session = aiohttp.ClientSession(headers={"User-Agent": EPG_USER_AGENT},
                                    raise_for_status=True)
    async with session.get(EPG_URL, params={}) as r:
        results = await r.json()
        f = open("epg.json", "w")
        f.write(json.dumps(results))
        # print(results)
    await session.close()

def rq_livebox(hostname, port, operation, params=None):
    url = "http://{}:{}/remoteControl/cmd".format(hostname, port)
    get_params = OrderedDict({"operation": operation})
    _LOGGER.debug("Request Livebox operation %s", operation)
    if params:
        get_params.update(params)
    try:
        r = requests.get(url, params=get_params, timeout=5)
        r.raise_for_status()
        # _LOGGER.debug("Livebox response: %s", r.json())
        return r.json()
    except requests.exceptions.RequestException as err:
        _standby_state = "1"
        _LOGGER.error(err)
    except requests.exceptions.HTTPError as errh:
        _LOGGER.error(errh)
    except requests.exceptions.ConnectionError as errc:
         _LOGGER.error(errc)
    except requests.exceptions.Timeout as errt:
         _LOGGER.error(errt)

# loop = asyncio.get_event_loop()
# connect = loop.create_datagram_endpoint(MyProtocol, family=socket.AF_INET)
# transport, protocol = loop.run_until_complete(connect)
#
# notify = messages.SSDPRequest('NOTIFY')
# notify.sendto(transport, (network.MULTICAST_ADDRESS_IPV4, network.PORT))
#
# try:
#     loop.run_forever()
# except KeyboardInterrupt:
#     pass
#
# transport.close()
# loop.close()

async def device_status_poller(device: LiveboxTvUhdClient, interval: float = 10.0) -> None:
    """Receiver data poller."""
    while True:
        try:
            await device.update()
            print(f"Orange : {device.channel_id} {device.channel_name} {device.state} {device.show_title}")
            # print("Episode : "+str(device.show_episode))
        except (KeyError, ValueError):
            pass
        await asyncio.sleep(interval)
async def main():
    logging.basicConfig(level=logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    # ch.setFormatter(formatter)
    _LOGGER.addHandler(ch)
    # d = datetime.datetime.utcnow()
    # _show_position = calendar.timegm(d.utctimetuple())
    # print(_show_position)
    # exit(0)
    client = LiveboxTvUhdClient("192.168.1.49", "8080")
    await client.connect()
    # await device_status_poller(client, 5)
    data = rq_livebox("192.168.1.49", "8080", "10")
    print_json(data=data)

    # await client.set_channel_by_name("FRANCE 2")

    # epg_data = await client.rq_epg([])
    # f = open("epg.json", "w")
    # f.write(str(epg_data))
    # f.close()
    await client.disconnect()

    # await get_epg()
    # logging.getLogger("webos_client").setLevel(logging.DEBUG)

# toto = [i[4][0] for i in socket.getaddrinfo(socket.gethostname(), None)]
# print(*toto, sep=",")
#
# ips = []
# for interface in netifaces.interfaces():
#     addresses = netifaces.ifaddresses(interface)
#     for address in addresses.get(netifaces.AF_INET, []):
#         ips.append(address["addr"])
# print(*toto, sep=",")

if __name__ == "__main__":
    asyncio.run(main())
