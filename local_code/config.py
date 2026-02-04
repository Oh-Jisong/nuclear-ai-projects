# config.py
# 실습용 기본 설정 (필요한 값만 수정하면 main.py로 바로 실행 가능)
# TIP: 처음엔 REMOTE_IP="0.0.0.0" 권장 (모든 인터페이스에서 수신)

REMOTE_IP = "192.168.0.3"    # TODO: 필요 시 본인(수신기) IP로 변경
READ_PORT = 7000             # TODO: CNS가 송신하는 포트로 변경

# 같은 폴더에 list.dat / pids.txt를 두면 아래처럼 상대경로로 가장 편합니다.
OUT_DIR  = "./logs"          # TODO: 저장 폴더(상대/절대 모두 가능)
LIST_DAT = "./list.dat"
PIDS_TXT = "./pids.txt"

# KCNTOMS가 이 시간 동안 변하지 않으면 자동 종료 (Freeze 시 종료 유도)z
STOP_NOCHANGE_SEC = 2

# KCNTOMS 기준 기록 주기 (ReadCNS.py와 동일하게 '초' 단위로 취급)
LOG_PERIOD_SEC = 1.0