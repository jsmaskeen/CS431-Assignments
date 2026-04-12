import hashlib
import hmac

def build_message(parts):
    result = b""
    for i, p in enumerate(parts):
        if isinstance(p, str):
            p = p.encode()
        if p is None:
            p = b""
        if i != 0:
            result += b"|"
        if i == 0 or p == b"":
            result += p
        else:
            length = str(len(p)).encode()
            result += length + b":" + p
    return result

def sign_data(secret, data):
    if isinstance(secret, str):
        secret = secret.encode()
    if isinstance(data, str):
        data = data.encode()

    mac = hmac.new(secret, digestmod=hashlib.sha256)
    mac.update(data)
    return mac.hexdigest().encode()


msg = build_message([b"2", "0", "1775950021", "admin", "dHJ1ZQ==", b""])
sig = sign_data("MangoDB\n", msg)

print((msg + sig).decode())

