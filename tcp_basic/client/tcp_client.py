import socket
from core.serializer import serialize, deserialize
from core.protocol import Request
from core.exceptions import ProtocolError
from core.framing import encode_message, decode_message


class TCPClient:
    def __init__(self, host: str, port: int, timeout: int = 5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def send_request(self, request: Request):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(self.timeout)

            try:
                s.connect((self.host, self.port))

                s.sendall(encode_message(serialize(request.to_dict())))

                data = decode_message(s)
                if not data:
                    raise ProtocolError("Response vazia do Servidor")

                return deserialize(data)

            except socket.timeout:
                raise TimeoutError(" timeout do Servidor")

            except Exception as e:
                raise e