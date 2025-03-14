from app.shared.core.serializer import Serializer


class MachineRunSerializer(Serializer):
    logs: str
    session_id: str
    is_error: bool
    stderr: str

    @classmethod
    def serialize(cls, logs: str, session_id: str, is_error: bool, stderr: str):
        return cls(logs=logs, session_id=session_id, is_error=is_error, stderr=stderr)
