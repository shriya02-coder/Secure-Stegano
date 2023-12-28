from Crypto.PublicKey import RSA
import os

def generate_keys(key_size):
    """
    Generate RSA public and private keys of the specified size.

    Args:
    key_size: Size of the RSA key to generate, in this case 5000 bits.
    """
    # Define the paths for the keys
    private_key_path = './keys/private_key_1024.pem'
    public_key_path = './keys/public_key_1024.pem'
    
    # Check if the key files already exist
    is_private_key_existing = os.path.isfile(private_key_path)
    is_public_key_existing = os.path.isfile(public_key_path)
    
    # If both keys exist, notify the user
    if is_private_key_existing and is_public_key_existing:
        print("Public and private keys already exist.")
    else:
        # Generate new RSA keys if either key does not exist
        print("Generating new RSA key pair...")
        key_pair = RSA.generate(key_size)
        
        # Create the keys directory if it doesn't exist
        if not os.path.exists('./keys'):
            os.makedirs('./keys')
        
        # Write the private key to a PEM file
        with open(f"./keys/private_key_{key_size}.pem", "wb") as private_file:
            private_file.write(key_pair.exportKey('PEM'))
        
        # Extract the public key from the key pair and write to a file
        pubkey = key_pair.publickey()
        with open(f"./keys/public_key_{key_size}.pem", "wb") as public_file:
            public_file.write(pubkey.exportKey('OpenSSH'))
        
        print(f"RSA keys of size {key_size} bits have been generated and stored in the keys directory.")

if __name__ == '__main__':
    # Set the desired key size as 5000 bits
    key_size = 5000
    generate_keys(key_size)
