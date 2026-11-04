import ijson

def read_packets(file_path):
    with open(file_path, "rb") as file:
        for packet in ijson.items(file, "item"):
            yield packet

i = 1
packets = []
for packet in read_packets("sample_docs/test.json"):
    #print("Iteration:",i, end="")
    i += 1
    with open("single_packet.json","w") as file:
        import json
        packets.append(packet)
        json.dump(packets, file, indent=4)
    # if i==2:
    #     break
    #print(packet, "\n\n")

clean_packets = []
for packet in packets:
    clean_packet = {}
    #
    layer = packet["_source"]["layers"]
    #
    frame = layer["frame"]
    ip = layer["ip"]
    tcp = layer["tcp"]
    #
    clean_packet["frame.time"] = frame["frame.time"]
    clean_packet["frame.number"] = frame["frame.number"]
    #
    clean_packet["ip.src"] = ip["ip.src"]
    clean_packet["ip.dst"] = ip["ip.dst"]
    #
    clean_packet["tcp.srcport"] = tcp["tcp.srcport"]
    clean_packet["tcp.dstport"] = tcp["tcp.dstport"]
    clean_packet["tcp.len"] = tcp["tcp.len"]
    clean_packet["tcp.flags_tree"] = tcp["tcp.flags_tree"]
    try:
        clean_packet["tcp.payload"] = tcp["tcp.payload"]
    except KeyError:
        continue
    clean_packets.append(clean_packet)

with open("clean_packets.json","w") as file:
    json.dump(clean_packets, file, indent=5)