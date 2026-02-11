'''
Responsável por:
    Definir os modelos de Request e Response
    Validar estruturas
    Construir respostas padronizadas
'''

import uuid
from typing import Any, Dict

from core.exceptions import (
    InvalidMessageError,
    UnsupportedMessageTypeError,
    UnsupportedVersionError
)

SUPPORTED_VERSION = "1.0"
SUPPORTED_TYPES = {"greeting", "health_check"}

class Request:
    def __init__(self, version: str, request_id: str, message_type: str, payload: Dict[str, Any]):
        self.version = version
        self.request_id = request_id
        self.message_type = message_type
        self.payload = payload

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "request_id": self.request_id,
            "type": self.type,
            "payload": self.payload,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Request":
        cls._validate_structure(data)

        version = data["version"]
        request_id = data["request_id"]
        message_type = data["type"]
        payload = data.get("payload", {})

        if version != SUPPORTED_VERSION:
            raise UnsupportedVersionError(f"Versão não suportada: {version}")
        
        if message_type not in SUPPORTED_TYPES:
            raise UnsupportedMessageTypeError(f"Tipo não suportado: {message_type}")
        
        return cls(version, request_id, message_type, payload)
    
    @staticmethod
    def _validate_structure(data: Dict[str, Any]):
        required_fields = {"version", "request_id", "type"}

        if not isinstance(data, dict):
            raise InvalidMessageError("Mensagem deve ser um objeto JSON.")
        
        missing = required_fields - data.keys()
        if missing:
            raise InvalidMessageError(f"Campos obrigatórios ausentes: {missing}")
    

class Response:
    def __init__(self, request_id: str, status: str, data: Any = None, error: Any = None):
        self.version = SUPPORTED_VERSION
        self.request_id = request_id
        self.status = status
        self.data = data
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "version": self.version,
            "request_id": self.request_id,
            "status": self.status,
            "data": self.data,
            "error": self.error,
        }

    @classmethod
    def success(cls, request_id: str, data: Any = None) -> "Response":
        return cls(request_id=request_id, status="success", data=data)

    @classmethod
    def error(cls, request_id: str, code: str, message: str) -> "Response":
        return cls(
            request_id=request_id,
            status="error",
            data=None,
            error={
                "code": code,
                "message": message,
            },
        )

def generate_request_id() -> str:
    return str(uuid.uuid4())