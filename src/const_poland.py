"""
Static file of the integration driver for Poland STB.

:copyright: (c) 2025 Albaintor
:license: Mozilla Public License Version 2.0, see LICENSE for more details.
"""

# EPG
EPG_URL = "https://tvgo.orange.pl/gpapi/epg/epg"
EPG_USER_AGENT = "Opera/9.80 (Linux i686; U; fr) Presto/2.10.287 Version/12.00 ; SC/IHD92 STB"
# pylint: disable = C0301
# channel list: https://tvgo.orange.pl/gpapi/live/channel-list?hhTech=iptv&deviceCat=otg
# channel logo: https://tvgo.orange.pl/gpapi/resource/image/L1ZPRC9EMkE1NUMwNUJDMEY4NTAwMDUyMDFDOEI4ODNCQUE1RTg0MjI4OEEyLnBuZw== # noqa: E501
# epg: https://tvgo.orange.pl/gpapi/epg/epg?hhTech=&deviceCat=otg&chosen-day=1642287660 # noqa: E501
# image: https://tvgo.orange.pl/mnapi/epgimages/akpah3154182.jpg

TIMEZONE = "Poland"

CHANNELS = [
    {"index": "-1", "epg_id": "-1", "name": "N/A"},
    {"index": "0", "epg_id": "0", "name": "Mozajka"},
    {"index": "1", "epg_id": "14135", "name": "TVP 1 HD"},
    {"index": "2", "epg_id": "14999", "name": "TVP 2 HD"},
    {"index": "3", "epg_id": "14171", "name": "TVN HD"},
    {"index": "4", "epg_id": "14177", "name": "TVN 7 HD"},
    {"index": "5", "epg_id": "14137", "name": "Polsat HD"},
    {"index": "6", "epg_id": "14301", "name": "TV4 HD"},
    {"index": "7", "epg_id": "15019", "name": "TVPuls HD"},
    {"index": "8", "epg_id": "14199", "name": "TVPuls 2 HD"},
    {"index": "9", "epg_id": "14185", "name": "TTV HD"},
    {"index": "10", "epg_id": "14015", "name": "TVP Polonia"},
    {"index": "11", "epg_id": "14294", "name": "Super Polsat HD"},
    {"index": "13", "epg_id": "14173", "name": "TV6 HD"},
    {"index": "18", "epg_id": "14250", "name": "Comedy Central HD"},
    {"index": "19", "epg_id": "14175", "name": "Paramount Channel HD"},
    {"index": "20", "epg_id": "14097", "name": "Polsat Comedy Central Extra HD"},
    {"index": "22", "epg_id": "14190", "name": "TVN24 HD"},
    {"index": "23", "epg_id": "14290", "name": "TVN24 Biznes i Świat HD"},
    {"index": "24", "epg_id": "14014", "name": "TVP Info HD"},
    {"index": "25", "epg_id": "14215", "name": "TVP3 Regionalna"},
    {"index": "28", "epg_id": "14249", "name": "TV Republika"},
    {"index": "29", "epg_id": "14233", "name": "Polsat News HD"},
    {"index": "31", "epg_id": "14004", "name": "Polsat News 2"},
    {"index": "32", "epg_id": "14323", "name": "wPolsce 4K UltraHD"},
    {"index": "33", "epg_id": "14287", "name": "Nowa TVH D"},
    {"index": "34", "epg_id": "14289", "name": "Metro TV HD"},
    {"index": "35", "epg_id": "14288", "name": "WP"},
    {"index": "36", "epg_id": "14286", "name": "Zoom TV"},
    {"index": "40", "epg_id": "14176", "name": "TVN Style HD"},
    {"index": "41", "epg_id": "14072", "name": "TLC HD"},
    {"index": "42", "epg_id": "15021", "name": "HGTV Home&Garden HD"},
    {"index": "43", "epg_id": "14293", "name": "FoodNetwork HD"},
    {"index": "44", "epg_id": "15033", "name": "Discovery Life HD"},
    {"index": "45", "epg_id": "14118", "name": "ID HD"},
    {"index": "48", "epg_id": "14178", "name": "TVN Turbo HD"},
    {"index": "49", "epg_id": "14155", "name": "Discovery Channel HD"},
    {"index": "50", "epg_id": "14222", "name": "FoodNetwork HD"},
    {"index": "58", "epg_id": "14262", "name": "NTL Radomsko HD"},
    {"index": "222", "epg_id": "14258", "name": "TVN Fabuła HD"},
    {"index": "223", "epg_id": "14130", "name": "TVP Seriale"},
    {"index": "224", "epg_id": "14016", "name": "TVP Kultura"},
    {"index": "225", "epg_id": "14237", "name": "Stopklatka TV HD"},
    {"index": "226", "epg_id": "15014", "name": "Kino Polska HD"},
    {"index": "227", "epg_id": "14250", "name": "Comedy Central HD"},
    {"index": "228", "epg_id": "14281", "name": "13 Ulica HD"},
    {"index": "229", "epg_id": "14175", "name": "Paramount Channel HD"},
    {"index": "230", "epg_id": "14097", "name": "Polsat Comedy Central Extra HD"},
    {"index": "233", "epg_id": "14132", "name": "KinoTV HD"},
    {"index": "234", "epg_id": "14164", "name": "AMC HD"},
    {"index": "235", "epg_id": "14219", "name": "TNT HD"},
    {"index": "236", "epg_id": "14138", "name": "FOX HD"},
    {"index": "239", "epg_id": "14172", "name": "AXN HD"},
    {"index": "253", "epg_id": "14229", "name": "Polsat Seriale"},
    {"index": "254", "epg_id": "14139", "name": "Polsat 2 HD"},
    {"index": "337", "epg_id": "14193", "name": "TVP Rozrywka"},
    {"index": "338", "epg_id": "14072", "name": "TLC HD"},
    {"index": "341", "epg_id": "14293", "name": "FoodNetwork HD"},
    {"index": "346", "epg_id": "14251", "name": "Lifetime HD"},
    {"index": "347", "epg_id": "14160", "name": "Polsat Play HD"},
    {"index": "348", "epg_id": "14161", "name": "Polsat Cafe HD"},
    {"index": "352", "epg_id": "14308", "name": "TBN Polska"},
    {"index": "355", "epg_id": "14180", "name": "TVR HD"},
    {"index": "444", "epg_id": "15032", "name": "National Geographic"},
    {"index": "445", "epg_id": "14134", "name": "TVP Historia"},
    {"index": "446", "epg_id": "14240", "name": "FokusTV HD"},
    {"index": "447", "epg_id": "14212", "name": "Planete+ HD"},
    {"index": "448", "epg_id": "14155", "name": "Discovery Channel HD"},
    {"index": "449", "epg_id": "14118", "name": "ID HD"},
    {"index": "451", "epg_id": "15033", "name": "Discovery Life HD"},
    {"index": "455", "epg_id": "14156", "name": "National Geographic HD"},
    {"index": "458", "epg_id": "14300", "name": "Polsat Doku HD"},
    {"index": "461", "epg_id": "14196", "name": "History HD"},
    {"index": "467", "epg_id": "14222", "name": "Travel Channel HD"},
    {"index": "555", "epg_id": "14242", "name": "TVP ABC"},
    {"index": "556", "epg_id": "14208", "name": "MiniMini+ HD"},
    {"index": "557", "epg_id": "14123", "name": "Disney Junior"},
    {"index": "558", "epg_id": "14187", "name": "NickJr."},
    {"index": "566", "epg_id": "14117", "name": "Nickelodeon"},
    {"index": "567", "epg_id": "15044", "name": "Disney Channel HD"},
    {"index": "568", "epg_id": "15031", "name": "Disney XD"},
    {"index": "569", "epg_id": "14217", "name": "Cartoon Network HD"},
    {"index": "666", "epg_id": "15039", "name": "MTV Polska HD"},
    {"index": "667", "epg_id": "14037", "name": "MTV Music"},
    {"index": "676", "epg_id": "14005", "name": "4FUN.TV"},
    {"index": "679", "epg_id": "14291", "name": "Eska Rock TV"},
    {"index": "777", "epg_id": "14031", "name": "BBC World News"},
    {"index": "778", "epg_id": "14009", "name": "Euronews"},
    {"index": "779", "epg_id": "15055", "name": "CNBC Europe"},
    {"index": "780", "epg_id": "14028", "name": "Bloomberg"},
    {"index": "781", "epg_id": "14223", "name": "CNN"},
    {"index": "782", "epg_id": "14265", "name": "SkyNews"},
    {"index": "786", "epg_id": "14038", "name": "France 24 English HD"},
    {"index": "990", "epg_id": "radio", "name": "Radio"},
    {"index": "996", "epg_id": "interactivehelp", "name": "PomocInteraktywna"},
    {"index": "997", "epg_id": "orangeekspert", "name": "OrangeExpert"},
    {"index": "998", "epg_id": "diagnostic", "name": "Kanałtechniczny"},
    {"index": "999", "epg_id": "101", "name": "Promo TV"},
]
