import pytest
import struct
from tcp_basic.core.framing import encode_message, recv_exact, decode_message


class FakeSocket:
    """
    Simula comportamento de socket.recv()
    """
    def __init__(self, chunks):
        self.chunks = chunks

    def recv(self, n):
        if not self.chunks:
            return b""
        return self.chunks.pop(0)


def test_encode_message_prefix():
    payload = b"hello"
    framed = encode_message(payload)

    length = struct.unpack("!I", framed[:4])[0]

    assert length == 5
    assert framed[4:] == payload


def test_recv_exact_reads_full_message():
    fake = FakeSocket([b"he", b"ll", b"o"])
    result = recv_exact(fake, 5)

    assert result == b"hello"


def test_recv_exact_connection_closed_early():
    fake = FakeSocket([b"he"])

    with pytest.raises(ConnectionError):
        recv_exact(fake, 5)


def test_decode_message():
    payload = b"world"
    header = struct.pack("!I", len(payload))
    fake = FakeSocket([header[:2], header[2:], b"wo", b"rld"])

    result = decode_message(fake)

    assert result == payload