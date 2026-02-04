# pids_io.py
# pids.txt 로딩/정리 유틸

def load_pids_txt(path: str):
    """pids.txt에서 pid 목록을 읽고 (주석/빈줄 제거), 중복 제거(순서 유지)"""
    pids = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            pids.append(s)

    seen, out = set(), []
    for p in pids:
        if p not in seen:
            out.append(p)
            seen.add(p)
    return out