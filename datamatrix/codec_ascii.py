DIGITS = '0123456789'


def encode_to_ascii(data: str) -> bytes:
    enc = []
    i = 0
    while i < len(data):
        if data[i] in DIGITS and i + 1 < len(data) and data[i + 1] in DIGITS:
            enc.append(130 + int(data[i:i + 2]))
            i += 1
        else:
            enc.append(list(data[i].encode('ascii'))[0] + 1)
        i += 1

    return bytes(enc)


def decode_to_ascii(data: bytes) -> tuple[str, int]:
    msg = ''
    for c in data:
        if 130 <= c < 230:
            msg += f'{c - 130:02d}'
        else:
            msg += bytes([c - 1]).decode('ascii')

    return msg, len(msg)
