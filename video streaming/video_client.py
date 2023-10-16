import socket
import cv2
import numpy as np
import threading

# 서버 설정
SERVER_HOST = 'localhost'
SERVER_PORT = 2500

# 비디오 스트림 표시 함수
def receive_video(client_socket):
    while True:
        try:
            data = client_socket.recv(921600)
            if data:
                frame = cv2.imdecode(np.frombuffer(data, dtype=np.uint8), 1)
                cv2.imshow("Video", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        except:
            pass

# 채팅 입력 및 전송 함수
def send_message(client_socket):
    while True:
        message = input()
        client_socket.send(message.encode('utf-8'))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_HOST, SERVER_PORT))

video_thread = threading.Thread(target=receive_video, args=(client,))
video_thread.start()

message_thread = threading.Thread(target=send_message, args=(client,))
message_thread.start()

message_thread.join()
client.close()