# collector.py
# ReadCNS(수신 전용) 상태머신: 시작/기록/종료 + CSV 저장
import os
import socket
import csv
import time

from config import (
    REMOTE_IP, READ_PORT, OUT_DIR, LIST_DAT, PIDS_TXT,
    STOP_NOCHANGE_SEC, LOG_PERIOD_SEC
)
from fastcns_packet import load_list_dat, read_pid_from_msg
from pids_io import load_pids_txt


def run_collect_only():
    os.makedirs(OUT_DIR, exist_ok=True)

    pid2info = load_list_dat(LIST_DAT)
    watch = load_pids_txt(PIDS_TXT)

    # KCNTOMS는 시작/종료/기록 제어를 위해 반드시 포함
    if "KCNTOMS" not in watch:
        watch = ["KCNTOMS"] + watch

    csv_path = os.path.join(OUT_DIR, f"cns_{int(time.time())}.csv")

    sock_recv = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_recv.bind((REMOTE_IP, READ_PORT))
    sock_recv.settimeout(2.0)

    started = False
    last_kcnt = None
    last_change_wall = time.time()
    next_log_kcnt = None

    with open(csv_path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=["t_sec"] + watch)
        writer.writeheader()

        while True:
            try:
                msg, addr = sock_recv.recvfrom(65535)
            except socket.timeout:
                # 시작 전이면 계속 대기
                if not started:
                    continue

                # 시작 후에는 "KCNTOMS 변화 없음"으로 종료 판정
                if (time.time() - last_change_wall) >= STOP_NOCHANGE_SEC:
                    print("[STOP] KCNTOMS no-change timeout")
                    break
                continue

            kcnt = read_pid_from_msg(msg, pid2info, "KCNTOMS")
            if kcnt != kcnt:  # NaN
                continue

            now_wall = time.time()

            if last_kcnt is None:
                last_kcnt = kcnt
                last_change_wall = now_wall
                continue

            # START: KCNTOMS가 증가하기 시작하면 started=True
            if (not started) and (kcnt > last_kcnt):
                started = True
                print(f"[START] KCNTOMS started: {last_kcnt:.3f} -> {kcnt:.3f}")
                # 다음 기록시각을 LOG_PERIOD 경계로 맞춤(원본 로직 스타일)
                next_log_kcnt = (int(kcnt // LOG_PERIOD_SEC) + 1) * LOG_PERIOD_SEC

            # KCNTOMS 변화 감지
            if kcnt != last_kcnt:
                last_kcnt = kcnt
                last_change_wall = now_wall

            # STOP: 일정 시간 KCNTOMS 변화 없으면 종료 (Freeze 시 종료 유도)
            if started and (now_wall - last_change_wall) >= STOP_NOCHANGE_SEC:
                print("[STOP] KCNTOMS stopped")
                break

            # LOG: KCNTOMS 기준으로 주기 기록
            if started and next_log_kcnt is not None and kcnt >= next_log_kcnt:
                row = {"t_sec": round(kcnt, 3)}
                for pid in watch:
                    row[pid] = read_pid_from_msg(msg, pid2info, pid)
                writer.writerow(row)
                f.flush()
                next_log_kcnt += LOG_PERIOD_SEC

    sock_recv.close()
    print("[DONE] saved:", csv_path)
    return csv_path