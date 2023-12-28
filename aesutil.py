import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import sys

# AES Utility Script for Encryption and Decryption using pycryptodome
# Utilizes AES-256 encryption for securing messages

def encrypt(key, source, encode=True, keyType='hex'):
    '''
    Encrypts a given message using AES-256-CBC.
    
    Parameters:
    - key: The encryption key. Accepts hex or ASCII based on keyType.
    - source: The message to encrypt.
    - encode: Flag to determine if the output should be base64 encoded.
    - keyType: Type of the key provided ('hex' or 'ascii').
    
    Returns:
    - The encrypted message, base64 encoded by default.
    '''
    source = source.encode()

    # Convert key to bytes based on the key type
    if keyType == "hex":
        key = bytes(bytearray.fromhex(key))
    else:
        key = key.encode()
        key = SHA256.new(key).digest()

    # Initialization Vector for AES
    IV = Random.new().read(AES.block_size)

    # Setting up encryptor with the key and mode
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    # Calculating padding for the source
    padding = AES.block_size - len(source) % AES.block_size
    source += bytes([padding]) * padding  # Adding padding to the source

    # Encrypting the data
    data = IV + encryptor.encrypt(source)

    # Returning the encrypted data, base64 encoded if encode is True
    return base64.b64encode(data).decode() if encode else data


def decrypt(key, source, decode=True, keyType="hex"):
    '''
    Decrypts a given message using AES-256-CBC.
    
    Parameters:
    - key: The decryption key. Accepts hex or ASCII based on keyType.
    - source: The encrypted message to decrypt.
    - decode: Flag to determine if the input is base64 encoded.
    - keyType: Type of the key provided ('hex' or 'ascii').
    
    Returns:
    - The decrypted message.
    '''
    if decode:
        source = base64.b64decode(source.encode())

    # Convert key to bytes based on the key type
    if keyType == "hex":
        key = bytes(bytearray.fromhex(key))
    else:
        key = key.encode()
        key = SHA256.new(key).digest()

    # Extracting Initialization Vector from the source
    IV = source[:AES.block_size]

    # Setting up decryptor with the key and mode
    decryptor = AES.new(key, AES.MODE_CBC, IV)

    # Decrypting the source
    data = decryptor.decrypt(source[AES.block_size:])

    # Handling padding
    padding = data[-1]
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")

    # Returning the decrypted data without padding
    return data[:-padding]


# Main execution
if __name__ == "__main__":
    operation = sys.argv[1].lower()  # Encrypt or decrypt

    if operation in ["encrypt", "1"]:
        message = sys.argv[2]
        key = sys.argv[3]
        keyType = sys.argv[4]
        cipher = encrypt(key, message, keyType=keyType)
        print("Encrypted:", cipher)
    elif operation in ["decrypt", "2"]:
        cipher = sys.argv[2]
        key = sys.argv[3]
        keyType = sys.argv[4]
        message = decrypt(key, cipher, keyType=keyType)
        print("Decrypted:", message)
