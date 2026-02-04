# lab1_udp_receive_check.py
# 목적 : UDP 패킷이 "들어오는지"만 확인 (바이트 수, 송신 주소)

import socket
BIND_IP  = "10.64.163.138" # 내 컴퓨터가 어떤 IP로 들어오는 패킷을 받을지 설정 , 약간 넓은 의미의 집 주소
READ_PORT = 7000 # TODO : CNS 송신 포트로 변경 , 약간 아파트 동호수 느낌

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # socket 생성
sock.bind((BIND_IP, READ_PORT))
sock.settimeout(1.0)

print(f"[LAB1] Listening on {(BIND_IP, READ_PORT)}")

cnt = 0
while True:
    try:
        msg, addr = sock.recvfrom(65535) # 받는 패킷의 최대 길이 : 65535
        cnt +=1
        print(f"#{cnt} bytes = {len(msg)} from = {addr} head ={msg:12}")
    except socket.timeout:
        print("timeout... (CNS가 이 포트로 송신 중인지 확인)")