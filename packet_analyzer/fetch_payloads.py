from logger.time_logger import time_log

#@time_log
def fetch_payloads(clean_packet_generator):
    print("Payloads:")
    for clean_packet in clean_packet_generator:
        payload:str = clean_packet["tcp.payload"]
        while payload.startswith("00:"):
            payload = payload[3:]
        while payload.endswith(":00"):
            payload = payload[:-3]
        payload = payload.replace(":","")
        yield payload