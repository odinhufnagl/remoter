from app.shared.core.serializer import Serializer


class ApiKeySerializer(Serializer):
    api_key: str

    @classmethod
    def serialize(cls, api_key: str):
        return cls(api_key=api_key)
