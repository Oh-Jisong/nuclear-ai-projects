# lab3_listdat_map_and_one_pid.py
# 목적: list.dat로 pid -> (loc, typ) 매핑을 만들고, pid 1개 값을 언팩해보기

import socket
from struct import unpack


HEADER = 4
SLOT = 24


def load_list_dat(path="list.dat"):
    pid2info = {}
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        loc = 0
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 2:
                continue

            pid = parts[0]
            typ = int(parts[1])   # 0=int, 1=float
            pid2info[pid] = (loc, typ)
            loc += 1
    return pid2info

def read_pid(msg: bytes, loc: int, typ: int):
    start = HEADER + SLOT*loc
    block = msg[start:start+SLOT]
    vals = unpack("<ififif", block)    # [i,f,i,f,i,f]
    return vals[4 + typ]               # typ=0 -> int, typ=1 -> float


pid2info = load_list_dat("list.dat")
print("[LAB3] loaded pids:", len(pid2info))

TARGET_PID = "KCNTOMS"   # TODO: 없으면 list.dat에 있는 다른 pid로 변경
if TARGET_PID not in pid2info:
    print("TARGET_PID not found in list.dat. Change TARGET_PID!")
    raise SystemExit

loc, typ = pid2info[TARGET_PID]
print("[TARGET_PID info:", TARGET_PID, "loc=", loc, "typ=", typ)

BIND_IP = "0.0.0.0"
READ_PORT = 7000   # TODO: CNS 송신 포트로 변경
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, READ_PORT))
sock.settimeout(2.0)

msg, addr = sock.recvfrom(65535)
val = read_pid(msg, loc, typ)
print(f"[LAB3] {TARGET_PID} =", val)