import socket
from pyrtcm import RTCMReader


stream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
stream.connect(('10.10.8.43', 8888))
rtr = RTCMReader(stream)
for (raw_data, parsed_data) in rtr.iterate(): print(raw_data)
