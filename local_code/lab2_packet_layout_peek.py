# lab2_packet_layout_peek.py
# 목적: 패킷 구조를 눈으로 확인 (HEADER/SLOT, 슬롯 raw hex, 슬롯 unpack)

import socket
from struct import unpack

HEADER = 4
SLOT = 24
BIND_IP = "10.64.163.138"
READ_PORT = 7000   # TODO: CNS 송신 포트로 변경

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, READ_PORT))
sock.settimeout(2.0)

msg, addr = sock.recvfrom(65535)
print("[LAB2] got:", len(msg), "bytes from", addr)

print("header(4 bytes) =", msg[:HEADER])
# 앞쪽 3개 슬롯만 raw hex로 보기
for i in range(10):
    start = HEADER + SLOT*i
    block = msg[start:start+SLOT]
    print(f"\nslot[{i}] raw hex:", block.hex())

# 슬롯 0을 '<ififif'로 언팩해 보기
block0 = msg[HEADER:HEADER+SLOT]
vals = unpack("<ififif", block0)
print("\nslot[0] unpack <ififif =>", vals)