import rich
import re
import sys

#2024-03-25 18:50:30.145836 +00:00	intg-appletv	INFO	DEBUG:ucapi.api:[('127.0.0.1', 37764)] ->: {"kind": "resp", "req_id": 50, "code": 200, "msg": "result", "msg_data": {}}
filename = sys.argv[1] if len(sys.argv) > 1 else input('Fichier\n')

regex = re.compile(r"(->|<-):\S*([^$]+)")

file1 = open(filename, 'r')
while True:
    line = file1.readline()
    if not line:
        break
    # if not "intg-appletv" in line:
    #     continue
    if not "ucapi.api" in line:
        continue
    line = line.strip().replace("\\\"", "\"")
    result = regex.search(line)
    if result:
        print(result.group(1))
        rich.print_json(result.group(2), indent=None)
