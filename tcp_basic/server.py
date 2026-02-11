import socket
from concurrent.futures import ThreadPoolExecutor
from core.framing import encode_message, decode_message
from core.serializer import serialize, deserialize
from core.protocol import Request, Response
from core.exceptions import ProtocolError
from domain.greeting_service import GreetingService

HOST = "127.0.0.1"
PORT = 5000
MAX_WORKERS = 10


def handle_connection(conn, addr):
    service = GreetingService()
    print(f"[+] Connected {addr}")

    try:
        data = decode_message(conn)
        request_dict = deserialize(data)
        request = Request.from_dict(request_dict)

        result = service.handle(request)
        response = Response.success(result)

    except ProtocolError as e:
        response = Response.error(str(e))
    except Exception as e:
        response = Response.error("Erro interno do Servidor")

    conn.sendall(encode_message(serialize(response.to_dict())))
    conn.close()
    print(f"Encerrado {addr}")


def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((HOST, PORT))
        server.listen()

        print(f"Servidor rodando em {HOST}:{PORT}")
        print(f"Tamanho de Thread pool: {MAX_WORKERS}")

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            while True:
                conn, addr = server.accept()
                executor.submit(handle_connection, conn, addr)


if __name__ == "__main__":
    start_server()