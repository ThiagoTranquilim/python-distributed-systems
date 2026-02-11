import socket
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from core.protocol import Request, generate_request_id
from core.framing import encode_message, decode_message


HOST = "127.0.0.1"
PORT = 5000

TOTAL_REQUESTS = 200
CONCURRENT_CLIENTS = 50
TIMEOUT = 3

REQUEST_TYPES = ["greeting", "health_check"]


def build_payload(message_type: str):
    if message_type == "greeting":
        return {"name": "Thiago"}
    elif message_type == "health_check":
        return {}
    return {}


def send_request(message_type: str):
    try:
        with socket.create_connection((HOST, PORT), timeout=TIMEOUT) as s:

            request = Request(
                version="1.0",
                request_id=generate_request_id(),
                message_type=message_type,
                payload=build_payload(message_type),
            )

            encoded = encode_message(request.to_dict())
            s.sendall(encoded)

            response_data = s.recv(4096)
            response = decode_message(response_data)

            return message_type, response.get("status") == "success"

    except Exception as e:
        return message_type, False


def run_stress_test():
    start_time = time.time()
    errors_by_type = {t: 0 for t in REQUEST_TYPES}
    success_by_type = {t: 0 for t in REQUEST_TYPES}

    with ThreadPoolExecutor(max_workers=CONCURRENT_CLIENTS) as executor:

        futures = []
        for _ in range(TOTAL_REQUESTS):
            message_type = random.choice(REQUEST_TYPES)
            futures.append(executor.submit(send_request, message_type))

        for future in as_completed(futures):
            message_type, success = future.result()

            if success:
                success_by_type[message_type] += 1
            else:
                errors_by_type[message_type] += 1

    end_time = time.time()
    total_time = end_time - start_time

    print("\n===== Resultado do Stress Test =====")
    print(f"Total de Requisições: {TOTAL_REQUESTS}")
    print(f"Clientes Simultâneos: {CONCURRENT_CLIENTS}")
    print(f"Tempo Total: {total_time:.2f} segundos")
    print(f"Requisições por Segundo: {TOTAL_REQUESTS / total_time:.2f}")

    print("\n--- Sucessos por Tipo ---")
    for t in REQUEST_TYPES:
        print(f"{t}: {success_by_type[t]}")

    print("\n--- Erros por Tipo ---")
    for t in REQUEST_TYPES:
        print(f"{t}: {errors_by_type[t]}")


if __name__ == "__main__":
    run_stress_test()