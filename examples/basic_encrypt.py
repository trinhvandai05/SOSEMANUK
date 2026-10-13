"""Run after pip install -e . ; each helper starts a new stream."""
import secrets
from sosemanuk import encrypt, decrypt

key = secrets.token_bytes(32)
iv = secrets.token_bytes(16)
message = 'Xin chao SOSEMANUK!'.encode('utf-8')
ciphertext = encrypt(key, iv, message)
recovered = decrypt(key, iv, ciphertext)
print('Key (hex):', key.hex())
print('IV (hex):', iv.hex())
print('Ciphertext:', ciphertext.hex())
print('Decrypted:', recovered.decode('utf-8'))
assert recovered == message
