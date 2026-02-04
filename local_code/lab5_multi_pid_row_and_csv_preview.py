# lab5_multi_pid_row_and_csv_preview.py
# 목적: 여러 pid를 한 패킷에서 뽑아 row(dict) 만들고 CSV 형태로 출력

import socket
from struct import unpack


HEADER, SLOT = 4, 24


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

            pid, typ = parts[0], int(parts[1])
            pid2info[pid] = (loc, typ)
            loc += 1

    return pid2info


def read_pid(msg, loc, typ):
    start = HEADER + SLOT*loc
    vals = unpack("<ififif", msg[start:start+SLOT])
    return vals[4 + typ]


pid2info = load_list_dat("list.dat")

WATCH = ["KCNTOMS", "ZINST63", "ZINST65"]   # TODO: list.dat에 있는 pid로 변경 가능

BIND_IP = "0.0.0.0"
READ_PORT = 7000   # TODO: CNS 송신 포트로 변경

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((BIND_IP, READ_PORT))
sock.settimeout(2.0)

msg, _ = sock.recvfrom(65535)

row = {}
for pid in WATCH:
    loc, typ = pid2info[pid]
    row[pid] = read_pid(msg, loc, typ)

print("[LAB5] one row dict =", row)
print("[LAB5] CSV preview header =", ",".join(WATCH))
print("[LAB5] CSV preview row    =", ",".join(str(row[p]) for p in WATCH))