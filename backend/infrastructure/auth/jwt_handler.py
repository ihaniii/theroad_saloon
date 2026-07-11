import hmac
import hashlib
import base64
import json
import time

class JwtHandler:
    SECRET_KEY = b"the_road_secret_key_2026_super_private"

    @classmethod
    def _base64_url_encode(cls, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).decode('utf-8').replace('=', '')

    @classmethod
    def _base64_url_decode(cls, data: str) -> bytes:
        padding = '=' * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode(data + padding)

    @classmethod
    def generate_token(cls, user_id: str, role: str, expires_in: int = 3600) -> str:
        header = {"alg": "HS256", "typ": "JWT"}
        payload = {
            "sub": user_id,
            "role": role,
            "exp": int(time.time()) + expires_in
        }
        
        header_b64 = cls._base64_url_encode(json.dumps(header).encode('utf-8'))
        payload_b64 = cls._base64_url_encode(json.dumps(payload).encode('utf-8'))
        
        signature_base = f"{header_b64}.{payload_b64}".encode('utf-8')
        signature = hmac.new(cls.SECRET_KEY, signature_base, hashlib.sha256).digest()
        signature_b64 = cls._base64_url_encode(signature)
        
        return f"{header_b64}.{payload_b64}.{signature_b64}"

    @classmethod
    def verify_token(cls, token: str) -> dict:
        try:
            parts = token.split('.')
            if len(parts) != 3:
                raise ValueError("Invalid token format")
            
            header_b64, payload_b64, signature_b64 = parts
            signature_base = f"{header_b64}.{payload_b64}".encode('utf-8')
            
            expected_signature = hmac.new(cls.SECRET_KEY, signature_base, hashlib.sha256).digest()
            expected_signature_b64 = cls._base64_url_encode(expected_signature)
            
            if not hmac.compare_digest(signature_b64, expected_signature_b64):
                raise ValueError("Signature mismatch")
                
            payload = json.loads(cls._base64_url_decode(payload_b64).decode('utf-8'))
            if payload.get("exp", 0) < time.time():
                raise ValueError("Token expired")
                
            return payload
        except Exception as e:
            raise ValueError(f"Token validation failed: {str(e)}")
