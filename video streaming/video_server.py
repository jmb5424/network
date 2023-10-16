import socket
import cv2
import numpy as np
import threading

# 서버 설정
SERVER_HOST = 'localhost'
SERVER_PORT = 2500

# 웹캠 또는 비디오 파일
VIDEO_SOURCE = 0  # 0은 웹캠을 나타냅니다.

# 클라이언트 목록
clients = []

# 비디오 스트리밍 함수
def send_video():
    cap = cv2.VideoCapture(VIDEO_SOURCE)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))  # 비디오 크기 조정
        _, img_encoded = cv2.imencode('.jpg', frame)
        data = img_encoded.tobytes()
        for client in clients:
            client.send(data)

# 채팅 메시지 전송 함수
def send_message(client, message):
    for c in clients:
        if c != client:
            try:
                c.send(message.encode('utf-8'))
            except:
                clients.remove(c)

# 클라이언트 처리 함수
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            if message:
                print(message.decode('utf-8'))
                send_message(client, message.decode('utf-8'))
        except:
            clients.remove(client)

# 서버 설정 및 클라이언트 대기
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_HOST, SERVER_PORT))
server.listen(5)
print(f"서버가 {SERVER_HOST}:{SERVER_PORT}에서 시작되었습니다.")

# 비디오 스트리밍 스레드 시작
video_thread = threading.Thread(target=send_video)
video_thread.start()

while True:
    client, addr = server.accept()
    clients.append(client)
    print(f"{addr} 클라이언트가 연결되었습니다.")
    client_thread = threading.Thread(target=handle_client, args=(client,))
    client_thread.start()