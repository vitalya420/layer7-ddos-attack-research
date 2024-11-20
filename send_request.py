import socket
import ssl
import time

import dummy_json_generator


HOST = "localhost"
ADDR = (socket.gethostbyname(HOST), 5000)
print(ADDR)
SSL_CONTEXT = ssl.create_default_context()
DUMMY_DATA = dummy_json_generator.generate_large(50000, 500)


def create_connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(ADDR)
    return sock


def craft_request():
    data = DUMMY_DATA
    data = data.encode()
    content_len = len(data)
    request = (
        "POST /orjson HTTP/1.1\r\n"
        f"Content-Length: {content_len}\r\n"
        "Content-Type: application/json\r\n"
        "accept: application/json\r\n"
        "\r\n"
    ).encode() + data
    return request


def send_request(sock: socket.socket):
    req = craft_request()
    return sock.send(req)


def receive_response(sock: socket.socket):
    return sock.recv(0xFFFFFFF)


def main():
    conn = create_connection()
    start = time.time()
    bytes_sent = send_request(conn)
    end = time.time()
    print(
        f"{bytes_sent / 1024 / 1024} mb sent in {end-start:02f} seconds. Waiting response..."
    )
    start = time.time()
    res = receive_response(conn)
    end = time.time()
    print(res)
    print(f"Response received in {end-start:02f} seconds!")


if __name__ == "__main__":
    main()
