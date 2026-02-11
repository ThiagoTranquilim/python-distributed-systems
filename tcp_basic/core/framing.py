import struct


HEADER_SIZE = 4


def encode_message(payload_bytes: bytes) -> bytes:
    """
    Prefixa a mensagem com 4 bytes indicando o tamanho.
    """
    length = len(payload_bytes)
    header = struct.pack("!I", length)
    return header + payload_bytes


def recv_exact(sock, n: int) -> bytes:
    """
    Lê exatamente n bytes do socket.
    Evita partial read.
    """
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Conexão encerrada antes de receber bytes")
        data += chunk
    return data


def decode_message(sock) -> bytes:
    """
    Lê header e payload corretamente.
    """
    header = recv_exact(sock, HEADER_SIZE)
    message_length = struct.unpack("!I", header)[0]

    return recv_exact(sock, message_length)