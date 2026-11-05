from tkinter import filedialog
from pathlib import Path
import tkinter as tk
import ijson
import json
import sys

project_root = Path(__file__).parent.parent

def read_packets(file_path):
    with open(file_path, "rb") as file:
        for packet in ijson.items(file, "item"):
            yield packet

def generate_clean_packets():

    root = tk.Tk()
    root.withdraw()
    filepath = filedialog.askopenfilename(title="Select the Wireshark JSON file.", filetypes=[("JSON Files", "*.json")])
    if not filepath:
        print("\x1b[38;2;255;0;0mUser didn't select a file. Please re-run the program.\x1b[0m")
        sys.exit(1)

    clean_packets = []

    for packet in read_packets(filepath):

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

    with open(project_root/"jsons/clean_packets.json","w", encoding="utf-8") as file:
        json.dump(clean_packets, file, indent=5)
    print("\x1b[38;2;0;256;0mSaved.\x1b[0m")