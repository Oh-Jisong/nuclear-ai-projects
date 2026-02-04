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

def read_pid_from_msg(msg: bytes, pid2info: dict, pid: str) -> float:
    info =  pid2info.get(pid)
    if info is None:
        return float("nan")
    loc,typ = info

    start = HEADER + SLOT*loc
    block = msg[start:start+SLOT]
    if len(block) < SLOT :
        return float("nan")
    
    vals = unpack("<ififif", block)    # [i,f,i,f,i,f]
    return vals[4 + typ]               # typ=0 -> int, typ=1 -> float