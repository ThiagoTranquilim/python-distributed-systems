from core.protocol import Request
from client.tcp_client import TCPClient

HOST = "127.0.0.1"
PORT = 5000

if __name__ == "__main__":
    client = TCPClient(HOST, PORT)

    request = Request(
        type="greet",
        payload={"name": "Thiago"}
    )

    response = client.send_request(request)

    print("Server response:", response)