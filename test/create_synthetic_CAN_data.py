ids = [217056305, 418383153, 418381873, 418383164]
ticks = [50000, 30000, 60000, 10000]
data =  [0, 0xdeadbeef, 0xbeefdead, 0x27032022]
messages = []
for x in range(1, 1000):
    for y in range(0, len(ids)):
        msg = {"id": ids[y], "time": x * ticks[y] , "data": data[y]}
        messages.append(msg)
messages = sorted(messages, key=lambda k: k['time'])

import json
with open("test_data.json", "w") as f:
    json.dump(messages,f)
