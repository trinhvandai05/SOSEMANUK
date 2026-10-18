"""Zero-install demonstration: python run_demo.py."""
from pathlib import Path
import sys
import secrets

sys.path.insert(0, str(Path(__file__).resolve().parent / 'src'))
from sosemanuk import encrypt, decrypt

key = secrets.token_bytes(32)
iv = secrets.token_bytes(16)
plaintext = 'Ví dụ mã hóa SOSEMANUK bằng Python'.encode('utf-8')
ciphertext = encrypt(key, iv, plaintext)
decrypted = decrypt(key, iv, ciphertext)

print('Plaintext:', plaintext.decode())
print('Key (hex):', key.hex())
print('IV (hex):', iv.hex())
print('Ciphertext (hex):', ciphertext.hex())
print('Decrypted:', decrypted.decode())
assert decrypted == plaintext
