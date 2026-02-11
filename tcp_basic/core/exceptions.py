'''
Responsável por
    Definir erros padronizados do protocolo
    Mapear erro

'''

class ProtocolError(Exception):
    """Erro base do protocolo."""

class InvalidMessageError(ProtocolError):
    """Mensagem mal formada ou inválida."""

class UnsupportedVersionError(ProtocolError):
    """Versão de protocolo não suportada."""

class UnsupportedMessageTypeError(ProtocolError):
    """Tipo de mensagem não suportada."""