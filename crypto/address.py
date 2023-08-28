import bitcoin

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from eth_utils import to_checksum_address
import os

def generate_cryptocurrency_address(cryptocurrency):    
    # Load the RSA public key from the PEM file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    public_key_path = os.path.join(current_directory, 'public.txt')
    with open(public_key_path, 'rb') as key_file:
        public_key_data = key_file.read()
        rsa_public_key = load_pem_public_key(public_key_data, backend=default_backend())

    # Generate the cryptocurrency address using the public key
    if cryptocurrency == "BTC":
        address = bitcoin.pubkey_to_address(public_key_data, 0)
    elif cryptocurrency == "ETH":
        # Get the public key in bytes format
        public_key_bytes = rsa_public_key.public_bytes(
            encoding=serialization.Encoding.DER,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        address = to_checksum_address(public_key_bytes[-20:])
    else:
        return f"Unsupported cryptocurrency: {cryptocurrency}"  # Return a message indicating unsupported cryptocurrency

    # Return the address
    return address