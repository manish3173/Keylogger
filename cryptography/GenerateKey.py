from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

def generate_rsa_keys(key_size=2048, output_folder=None):
    """
    Generate an RSA key pair and save to files.
    
    Args:
        key_size: Size of the RSA key in bits (default: 2048)
        output_folder: Folder to save keys (default: current directory)
    
    Returns:
        Tuple of (private_key_path, public_key_path)
    """
    # Generate RSA private key
    print(f"Generating {key_size}-bit RSA key pair...")
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )

    # Generate public key from the private key
    public_key = private_key.public_key()
    
    # Determine output directory
    if output_folder is None:
        output_folder = os.getcwd()
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created output directory: {output_folder}")
    
    # Define file paths
    private_key_path = os.path.join(output_folder, "private_key.pem")
    public_key_path = os.path.join(output_folder, "public_key.pem")
    
    # Save the private key to a file
    with open(private_key_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()  # No encryption for simplicity
        ))
    
    print(f"Private key saved to: {private_key_path}")
    
    # Save the public key to a file
    with open(public_key_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))
    
    print(f"Public key saved to: {public_key_path}")
    
    return private_key_path, public_key_path

def main():
    """Main function to generate RSA keys"""
    # Set path for Cryptography folder
    cryptography_folder = r"C:\Users\ymani\OneDrive\Desktop\Projects\Keylogger\cryptography"
    
    # Generate RSA key pair
    private_key_path, public_key_path = generate_rsa_keys(
        key_size=2048,
        output_folder=cryptography_folder
    )
    
    print("\nRSA key pair generation complete!")
    print("\nSecurity Note:")
    print("- Keep the private key secure and never share it")
    print("- The public key can be distributed and used for encryption")
    print("- Anyone with the private key can decrypt the data")

if __name__ == "__main__":
    main()
