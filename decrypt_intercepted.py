import base64
import string
from pathlib import Path

source = 'zyxwvutsrqponZYXWVUTSRQPONmlkjihgfedcbaMLKJIHGFEDCBA'
target = 'mlkjihgfedcbaMLKJIHGFEDCBAzyxwvutsrqponZYXWVUTSRQPON'
reverse_step1 = str.maketrans(target, source)
lower = string.ascii_lowercase
reverse_step3 = str.maketrans(lower[4:] + lower[:4], lower)


def decode(message):
    steps = []
    while message and message[0] in '123':
        marker, message = message[0], message[1:]
        if marker == '1':
            message = message.translate(reverse_step1)
        elif marker == '2':
            message = base64.b64decode(message, validate=True).decode('latin1')
        else:
            message = message.translate(reverse_step3)
        steps.append(marker)

    if message.startswith('2'):
        raise ValueError('Initial Base64 layer has not been removed')
    if not steps or steps[-1] != '2':
        raise ValueError('Did not reach the expected initial Base64 layer')
    return message, steps


if __name__ == '__main__':
    ciphertext = Path(__file__).with_name('intercepted.txt').read_text().strip()
    plaintext, steps = decode(ciphertext)
    print('Decoded message:', plaintext)
    print('Total reversed operations:', len(steps))
    print('Randomly selected rounds:', len(steps) - 1)
    Path(__file__).with_name('decoded_message.txt').write_text(plaintext + '\n')
