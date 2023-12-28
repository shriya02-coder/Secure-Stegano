import binascii
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import sys

def encrypt(message, key_path):
    """
    Encrypt a message using RSA public key.

    Args:
    message: A string message to encrypt.
    key_path: Path to the RSA public key file.

    Returns:
    A Base64 encoded string of the encrypted message.
    """
    # Load the public key from the specified file
    with open(key_path, 'r') as file:
        public_key = RSA.importKey(file.read())
    
    # Create RSA cipher object and encrypt the message
    rsa_object = PKCS1_OAEP.new(public_key)
    cipher_text = rsa_object.encrypt(message.encode('utf-8'))
    
    # Encode the encrypted message with Base64 to ensure safe transport
    cipher_text = base64.b64encode(cipher_text)
    return cipher_text

def decrypt(message):
    """
    Decrypt a message using RSA private key.

    Args:
    message: A Base64 encoded string of the encrypted message.

    Returns:
    The decrypted message as a byte string.
    """
    # Path to your RSA private key
    private_key_path = './keys/private_key_5000.pem'
    
    # Load the private key from the specified file
    private_key = RSA.importKey(open(private_key_path, 'r').read())

    
    # Create RSA cipher object
    rsa_object = PKCS1_OAEP.new(private_key)

    try:
        # Attempt to decode the Base64 string and decrypt it
        cipher_text = base64.b64decode(message)
    except binascii.Error as e:
        # Handle incorrect padding or incomplete Base64 strings
        print(f"Decoding failed: {e}. Ensure the Base64 string is correctly formatted.")
        return None

    # Decrypt the message and return
    decrypted_message = rsa_object.decrypt(cipher_text)
    return decrypted_message


if __name__ == '__main__':
    # Command line argument handling
    operation = sys.argv[1].lower()  # Convert to lowercase to standardize
    
    if operation == "encrypt" or operation == '1':
        # Encrypt the message
        message_to_encrypt = sys.argv[2]
        public_key_path = sys.argv[3]
        encrypted_message = encrypt(message_to_encrypt, public_key_path)
        print("Encrypted message:", encrypted_message)
    
    elif operation == "decrypt" or operation == '2':
        # Decrypt the message
        encrypted_message = sys.argv[2]
        decrypted_message = decrypt(encrypted_message)
        print("Decrypted message:", decrypted_message)
