'''
Responsável por
    Converter dict em JSON
    Garantir newline framing
    Evitar vazamento de detalhes de transporte

'''

import json
from typing import Dict, Any


def serialize(message: Dict[str, Any]) -> bytes:
    """
    Converte dict para JSON e adiciona newline para framing.
    """
    return (json.dumps(message) + "\n").encode("utf-8")


def deserialize(raw_data: bytes) -> Dict[str, Any]:
    """
    Converte bytes JSON para dict.
    """
    try:
        return json.loads(raw_data.decode("utf-8"))
    except json.JSONDecodeError:
        raise ValueError("Mensagem JSON inválida.")