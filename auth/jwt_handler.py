from datetime import datetime, timedelta
import jwt




JWT_SECRET = "bb4a1d94ff2c93430ea15f24cf35ae"
JWT_ALGORITHM = "HS256"

def token_response(token: str, expires: datetime):
    return {
        'access_token': token,
        'expires_at': expires.strftime('%Y-%m-%d %H:%M:%S')
    }
    
def sign_jwt(user_id: str):
    expires = datetime.now() + timedelta(minutes=10)
    payload = {
        'user_id': user_id,
        'expiry': expires.timestamp(),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token, expires)

def decode_jwt(token: str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return payload if payload['expiry'] > time.time() else None