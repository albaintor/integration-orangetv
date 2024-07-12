# EPG
EPG_URL = "https://rp-ott-mediation-tv.woopic.com/api-gw/live/v3/applications/STB4PC/programs"
EPG_USER_AGENT = "Opera/9.80 (Linux i686; U; fr) Presto/2.10.287 Version/12.00 ; SC/IHD92 STB"

TIMEZONE = "Europe/Paris"

# channels
CHANNELS = [
    {"index": "-1", "epg_id": "-1", "name": "N/A"},
    {"index": "1", "epg_id": "192", "name": "TF1"},
    {"index": "2", "epg_id": "4", "name": "FRANCE 2"},
    # {"index": "902", "epg_id": "4", "name": "FRANCE 2 UHD"}, # Won't work : cannot send index
    {"index": "3", "epg_id": "1939", "name": "FRANCE 3"},
    # {"index": "3", "epg_id": "80", "name": "FRANCE 3"},
    {"index": "4", "epg_id": "34", "name": "CANAL+"},
    {"index": "5", "epg_id": "47", "name": "FRANCE 5"},
    {"index": "6", "epg_id": "118", "name": "M6"},
    {"index": "7", "epg_id": "111", "name": "ARTE"},
    {"index": "8", "epg_id": "445", "name": "C8"},
    {"index": "9", "epg_id": "119", "name": "W9"},
    {"index": "10", "epg_id": "195", "name": "TMC"},
    {"index": "11", "epg_id": "446", "name": "TFX"},
    {"index": "12", "epg_id": "444", "name": "NRJ12"},
    {"index": "13", "epg_id": "234", "name": "LCP/PS"},
    {"index": "14", "epg_id": "78", "name": "FRANCE 4"},
    {"index": "15", "epg_id": "481", "name": "BFM TV"},
    {"index": "16", "epg_id": "226", "name": "CNEWS"},
    {"index": "17", "epg_id": "458", "name": "CSTAR"},
    {"index": "18", "epg_id": "482", "name": "GULLI"},
    {"index": "19", "epg_id": "160", "name": "FRANCE Ô"},
    {"index": "20", "epg_id": "1404", "name": "TF1 SERIES FILMS"},
    {"index": "21", "epg_id": "1401", "name": "LA CHAINE L'EQUIPE"},
    {"index": "22", "epg_id": "1403", "name": "6TER"},
    {"index": "23", "epg_id": "1402", "name": "RMC STORY"},
    {"index": "24", "epg_id": "1400", "name": "RMC DECOUVERTE"},
    {"index": "25", "epg_id": "1399", "name": "CHERIE 25"},
    {"index": "26", "epg_id": "112", "name": "LCI"},
    {"index": "27", "epg_id": "2111", "name": "FRANCEINFO:"},
    {"index": "28", "epg_id": "4294967295", "name": "L'ACTU DE LA TV D'ORANGE"},
    {"index": "31", "epg_id": "1061", "name": "A la maison"},
    {"index": "34", "epg_id": "205", "name": "TV5MONDE"},
    {"index": "35", "epg_id": "191", "name": "TEVA"},
    {"index": "36", "epg_id": "145", "name": "PARIS PREMIERE"},
    {"index": "37", "epg_id": "115", "name": "RTL9"},
    {"index": "38", "epg_id": "225", "name": "TV BREIZH"},
    {"index": "40", "epg_id": "33", "name": "C+ CINEMA"},
    {"index": "41", "epg_id": "35", "name": "C+ SPORT"},
    {"index": "42", "epg_id": "1563", "name": "C+ SERIES"},
    {"index": "43", "epg_id": "657", "name": "C+ FAMILY"},
    {"index": "44", "epg_id": "30", "name": "C+ DECALE"},
    {"index": "45", "epg_id": "1290", "name": "BEIN SPORTS 1"},
    {"index": "46", "epg_id": "1304", "name": "BEIN SPORTS 2"},
    {"index": "47", "epg_id": "1335", "name": "BEIN SPORTS 3"},
    {"index": "49", "epg_id": "4294967295", "name": "Actu OCS"},
    {"index": "50", "epg_id": "730", "name": "OCS MAX"},
    {"index": "51", "epg_id": "733", "name": "OCS CITY, génération HBO"},
    {"index": "52", "epg_id": "732", "name": "OCS CHOC"},
    {"index": "53", "epg_id": "734", "name": "OCS GEANTS"},
    {"index": "56", "epg_id": "1562", "name": "PARAMOUNT CHANNEL"},
    {"index": "57", "epg_id": "2072", "name": "PARAMOUNT CHANNEL DECALE"},
    {"index": "58", "epg_id": "10", "name": "ACTION"},
    {"index": "59", "epg_id": "282", "name": "CINE+ PREMIER"},
    {"index": "60", "epg_id": "284", "name": "CINE+ FRISSON"},
    {"index": "61", "epg_id": "283", "name": "CINE+ EMOTION"},
    {"index": "62", "epg_id": "401", "name": "CINE+ FAMIZ"},
    {"index": "63", "epg_id": "285", "name": "CINE+ CLUB"},
    {"index": "64", "epg_id": "287", "name": "CINE+ CLASSIC"},
    {"index": "66", "epg_id": "1190", "name": "EUROCHANNEL"},
    {"index": "71", "epg_id": "1960", "name": "BET"},
    {"index": "72", "epg_id": "5", "name": "AB1"},
    {"index": "73", "epg_id": "121", "name": "MCM"},
    {"index": "74", "epg_id": "2441", "name": "TF1 +1"},
    {"index": "75", "epg_id": "2752", "name": "COMEDY CENTRAL"},
    {"index": "76", "epg_id": "87", "name": "GAME ONE"},
    {"index": "77", "epg_id": "1167", "name": "GAME ONE +1"},
    {"index": "78", "epg_id": "54", "name": "COMEDIE+"},
    {"index": "79", "epg_id": "2326", "name": "POLAR+"},
    {"index": "80", "epg_id": "2334", "name": "WARNER TV"},
    {"index": "81", "epg_id": "49", "name": "SERIE CLUB"},
    {"index": "82", "epg_id": "128", "name": "MTV"},
    {"index": "84", "epg_id": "1408", "name": "NON STOP PEOPLE"},
    {"index": "85", "epg_id": "1832", "name": "NOVELAS TV"},
    {"index": "88", "epg_id": "2803", "name": "TV PITCHOUN"},
    {"index": "92", "epg_id": "928", "name": "BOOMERANG +1"},
    {"index": "93", "epg_id": "924", "name": "BONG"},
    {"index": "94", "epg_id": "229", "name": "TIJI"},
    {"index": "95", "epg_id": "32", "name": "CANAL J"},
    {"index": "97", "epg_id": "344", "name": "PIWI+"},
    {"index": "98", "epg_id": "197", "name": "TELETOON+"},
    {"index": "99", "epg_id": "293", "name": "TELETOON+1"},
    {"index": "100", "epg_id": "58", "name": "DISNEY CHANNEL"},
    {"index": "101", "epg_id": "299", "name": "DISNEY CHANNEL+1"},
    {"index": "102", "epg_id": "300", "name": "DISNEY JUNIOR"},
    {"index": "103", "epg_id": "36", "name": "CARTOON NETWORK"},
    {"index": "104", "epg_id": "888", "name": "NICKELODEON JUNIOR"},
    {"index": "106", "epg_id": "473", "name": "NICKELODEON"},
    {"index": "107", "epg_id": "2065", "name": "NICKELODEON+1"},
    {"index": "108", "epg_id": "1746", "name": "NICKELODEON TEEN"},
    {"index": "115", "epg_id": "2094", "name": "ULTRA NATURE UHD"},
    {"index": "116", "epg_id": "12", "name": "ANIMAUX"},
    {"index": "117", "epg_id": "2037", "name": "CRIME DISTRICT"},
    {"index": "118", "epg_id": "38", "name": "CHASSE PECHE"},
    {"index": "119", "epg_id": "1776", "name": "TREK"},
    {"index": "121", "epg_id": "7", "name": "TOUTE L'HISTOIRE"},
    {"index": "122", "epg_id": "88", "name": "HISTOIRE TV"},
    {"index": "123", "epg_id": "451", "name": "USHUAIA TV"},
    {"index": "124", "epg_id": "829", "name": "MY ZEN TV"},
    {"index": "125", "epg_id": "63", "name": "SCIENCE & VIE TV"},
    {"index": "129", "epg_id": "508", "name": "NATIONAL GEOGRAPHIC"},
    {"index": "130", "epg_id": "719", "name": "NATIONAL GEOGRAPHIC WILD"},
    {"index": "131", "epg_id": "212", "name": "VOYAGE"},
    {"index": "132", "epg_id": "147", "name": "PLANETE+"},
    {"index": "133", "epg_id": "662", "name": "PLANETE+ CI"},
    {"index": "134", "epg_id": "402", "name": "PLANETE+ Aventure - Expérience"},
    {"index": "136", "epg_id": "1072", "name": "MUSEUM"},
    {"index": "140", "epg_id": "563", "name": "GINX"},
    {"index": "141", "epg_id": "2942", "name": "01TV, votre vie numérique"},
    {"index": "142", "epg_id": "2353", "name": "ES1"},
    {"index": "144", "epg_id": "2442", "name": "TMC +1"},
    {"index": "145", "epg_id": "6", "name": "MANGAS"},
    {"index": "146", "epg_id": "2040", "name": "TOONAMI"},
    {"index": "147", "epg_id": "1585", "name": "J-ONE"},
    {"index": "148", "epg_id": "2171", "name": "VICE TV"},
    {"index": "149", "epg_id": "2781", "name": "CLIQUE TV"},
    {"index": "151", "epg_id": "605", "name": "NRJ HITS"},
    {"index": "152", "epg_id": "2321", "name": "MELODY d'AFRIQUE"},
    {"index": "155", "epg_id": "1989", "name": "CLUBBING TV"},
    {"index": "156", "epg_id": "2153", "name": "OKLM TV"},
    {"index": "157", "epg_id": "453", "name": "M6MUSIC"},
    {"index": "160", "epg_id": "265", "name": "MELODY"},
    {"index": "163", "epg_id": "2006", "name": "MTV HITS"},
    {"index": "166", "epg_id": "2958", "name": "OLYMPIA TV"},
    {"index": "167", "epg_id": "125", "name": "MEZZO"},
    {"index": "168", "epg_id": "907", "name": "MEZZO LIVE HD"},
    {"index": "169", "epg_id": "1353", "name": "STINGRAY CLASSICA"},
    {"index": "173", "epg_id": "64", "name": "EQUIDIA"},
    {"index": "174", "epg_id": "2837", "name": "SPORT EN FRANCE"},
    {"index": "179", "epg_id": "1336", "name": "BEIN SPORTS MAX 4"},
    {"index": "180", "epg_id": "1337", "name": "BEIN SPORTS MAX 5"},
    {"index": "181", "epg_id": "1338", "name": "BEIN SPORTS MAX 6"},
    {"index": "182", "epg_id": "1339", "name": "BEIN SPORTS MAX 7"},
    {"index": "183", "epg_id": "1340", "name": "BEIN SPORTS MAX 8"},
    {"index": "184", "epg_id": "1341", "name": "BEIN SPORTS MAX 9"},
    {"index": "185", "epg_id": "1342", "name": "BEIN SPORTS MAX 10"},
    {"index": "186", "epg_id": "15", "name": "AUTOMOTO, la chaîne"},
    {"index": "189", "epg_id": "1166", "name": "GOLF CHANNEL"},
    {"index": "214", "epg_id": "1996", "name": "FASHIONTV"},
    {"index": "215", "epg_id": "531", "name": "LUXE TV"},
    {"index": "219", "epg_id": "57", "name": "DEMAIN"},
    {"index": "220", "epg_id": "110", "name": "KTO"},
    {"index": "225", "epg_id": "992", "name": "LCP 100%"},
    {"index": "227", "epg_id": "529", "name": "FRANCE 24 FRANCAIS"},
    {"index": "228", "epg_id": "1073", "name": "BFM BUSINESS"},
    {"index": "229", "epg_id": "140", "name": "EURONEWS Français"},
    {"index": "232", "epg_id": "671", "name": "FRANCE 24 ANGLAIS"},
    {"index": "234", "epg_id": "53", "name": "CNN"},
    {"index": "235", "epg_id": "51", "name": "CNBC"},
    {"index": "236", "epg_id": "410", "name": "BLOOMBERG EUROPE"},
    {"index": "237", "epg_id": "19", "name": "BBC WORLD NEWS"},
    {"index": "238", "epg_id": "525", "name": "AL JAZEERA ANGLAIS"},
    {"index": "243", "epg_id": "781", "name": "I24NEWS"},
    {"index": "244", "epg_id": "830", "name": "NHK WORLD - JAPAN"},
    {"index": "245", "epg_id": "61", "name": "DEUTSCHE WELLE"},
    {"index": "271", "epg_id": "1662", "name": "COLMAX TV"},
    {"index": "272", "epg_id": "1711", "name": "HUSTLER HD"},
    {"index": "273", "epg_id": "218", "name": "XXL"},
    {"index": "274", "epg_id": "560", "name": "DORCEL TV"},
    {"index": "275", "epg_id": "1474", "name": "DORCEL XXX"},
    {"index": "277", "epg_id": "837", "name": "PENTHOUSE GOLD"},
    {"index": "278", "epg_id": "1592", "name": "PENTHOUSE QUICKIES"},
    {"index": "279", "epg_id": "1468", "name": "PENTHOUSE BLACK"},
    {"index": "284", "epg_id": "406", "name": "PINK X"},
    {"index": "285", "epg_id": "683", "name": "MAN-X"},
    {"index": "301", "epg_id": "655", "name": "FRANCE 3 ALPES"},
    {"index": "302", "epg_id": "249", "name": "FRANCE 3 ALSACE"},
    {"index": "303", "epg_id": "304", "name": "FRANCE 3 AQUITAINE"},
    {"index": "304", "epg_id": "649", "name": "FRANCE 3 AUVERGNE"},
    {"index": "305", "epg_id": "647", "name": "FRANCE 3 NORMANDIE CAEN"},
    {"index": "306", "epg_id": "636", "name": "FRANCE 3 BOURGOGNE"},
    {"index": "307", "epg_id": "634", "name": "FRANCE 3 BRETAGNE"},
    {"index": "308", "epg_id": "306", "name": "FRANCE 3 CENTRE"},
    {"index": "309", "epg_id": "641", "name": "FRANCE 3 CHAMPAGNES"},
    {"index": "310", "epg_id": "308", "name": "FRANCE 3 CORSE"},
    {"index": "311", "epg_id": "642", "name": "FRANCE 3 CÔTE D'AZUR"},
    {"index": "312", "epg_id": "637", "name": "FRANCE 3 FRANCHE COMTE"},
    {"index": "313", "epg_id": "646", "name": "FRANCE 3 NORMANDIE ROUEN"},
    {"index": "314", "epg_id": "650", "name": "FRANCE 3 LANGUEDOC"},
    {"index": "315", "epg_id": "638", "name": "FRANCE 3 LIMOUSIN"},
    {"index": "316", "epg_id": "640", "name": "FRANCE 3 LORRAINE"},
    {"index": "317", "epg_id": "651", "name": "FRANCE 3 MIDI-PYRENEES"},
    {"index": "318", "epg_id": "644", "name": "FRANCE 3 NORD PAS DE CALAIS"},
    {"index": "319", "epg_id": "313", "name": "FRANCE 3 PARIS IDF"},
    {"index": "320", "epg_id": "635", "name": "FRANCE 3 PAYS DE LA LOIRE"},
    {"index": "321", "epg_id": "645", "name": "FRANCE 3 PICARDIE"},
    {"index": "322", "epg_id": "639", "name": "FRANCE 3 POITOU CHARENTES"},
    {"index": "323", "epg_id": "643", "name": "FRANCE 3 PACA"},
    {"index": "324", "epg_id": "648", "name": "FRANCE 3 RHONES ALPES"},
    {"index": "325", "epg_id": "80", "name": "FRANCE 3 SD"},
    {"index": "401", "epg_id": "2293", "name": "A+ KIDS"},
    {"index": "403", "epg_id": "185", "name": "TCM CINEMA VO"},
    {"index": "407", "epg_id": "321", "name": "BOOMERANG (VO)"},
    {"index": "408", "epg_id": "18", "name": "FOXNEWS"},
    {"index": "420", "epg_id": "13", "name": "RTL NITRO"},
    {"index": "420", "epg_id": "2311", "name": "RTL NITRO"},
    {"index": "422", "epg_id": "219", "name": "ZDF"},
    {"index": "423", "epg_id": "973", "name": "ZDF_NEO"},
    {"index": "424", "epg_id": "966", "name": "RTL 2"},
    {"index": "425", "epg_id": "971", "name": "VOX"},
    {"index": "427", "epg_id": "964", "name": "PROSIEBEN"},
    {"index": "428", "epg_id": "1854", "name": "SUPER RTL"},
    {"index": "429", "epg_id": "982", "name": "KIKA"},
    {"index": "431", "epg_id": "960", "name": "3SAT"},
    {"index": "432", "epg_id": "979", "name": "ONE"},
    {"index": "433", "epg_id": "208", "name": "TVE INTERNACIONAL"},
    {"index": "452", "epg_id": "2046", "name": "CANAL Q"},
    {"index": "455", "epg_id": "169", "name": "RTPI"},
    {"index": "460", "epg_id": "156", "name": "RAI UNO"},
    {"index": "461", "epg_id": "154", "name": "RAI DUE"},
    {"index": "462", "epg_id": "155", "name": "RAI TRE"},
    {"index": "465", "epg_id": "1129", "name": "RAI NEWS 24"},
    {"index": "499", "epg_id": "2000", "name": "THE ISRAELI NETWORK"},
    {"index": "521", "epg_id": "340", "name": "2M MONDE"},
    {"index": "589", "epg_id": "1133", "name": "VOX AFRICA"},
    {"index": "608", "epg_id": "1461", "name": "NOLLYWOOD TV"},
    {"index": "611", "epg_id": "984", "name": "EQUINOXE"},
    {"index": "612", "epg_id": "1466", "name": "B-ONE"},
    {"index": "613", "epg_id": "3504", "name": "CANAL+ SPORT360"},
    {"index": "614", "epg_id": "3501", "name": "CANAL+ FOOT"},
    {"index": "615", "epg_id": "3779", "name": "CANAL+ BOX OFFICE"},
    {"index": "616", "epg_id": "3347", "name": "CANAL+ DOCS"},
    {"index": "617", "epg_id": "3348", "name": "CANAL+ KIDS"},
    {"index": "618", "epg_id": "3349", "name": "CANAL+ GRAND ECRAN"},
]
