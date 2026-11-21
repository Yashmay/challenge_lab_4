import base64
import string
from pathlib import Path

from decrypt_intercepted import decode, source, target

forward_step1 = str.maketrans(source, target)
lower = string.ascii_lowercase
forward_step3 = str.maketrans(lower, lower[4:] + lower[:4])


def encode_with_recorded_steps(plaintext, decoded_steps):
    message = plaintext
    for marker in reversed(decoded_steps):
        if marker == "1":
            message = message.translate(forward_step1)
        elif marker == "2":
            message = base64.b64encode(message.encode("latin1")).decode("ascii")
        elif marker == "3":
            message = message.translate(forward_step3)
        else:
            raise ValueError(f"Unknown marker: {marker!r}")
        message = marker + message
    return message


def main():
    intercepted = Path(__file__).with_name("intercepted.txt").read_text().strip()
    plaintext, decoded_steps = decode(intercepted)
    reconstructed = encode_with_recorded_steps(plaintext, decoded_steps)
    verified = reconstructed == intercepted
    print("Recovered plaintext:", plaintext)
    print("Reversed operations:", len(decoded_steps))
    print("Original ciphertext characters:", len(intercepted))
    print("Reconstructed ciphertext characters:", len(reconstructed))
    print("Verification successful:", verified)
    if not verified:
        raise SystemExit("ERROR: reconstructed ciphertext does not match")


if __name__ == "__main__":
    main()
