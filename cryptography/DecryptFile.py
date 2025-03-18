from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
import os

def decrypt_file(private_key_path, encrypted_file_path, output_file_path):
    """
    Decrypt a file that was encrypted with RSA
    
    Args:
        private_key_path: Path to the RSA private key PEM file
        encrypted_file_path: Path to the encrypted file
        output_file_path: Path where the decrypted file will be saved
    """
    # Load the private key
    with open(private_key_path, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )
    
    # Read the encrypted file
    with open(encrypted_file_path, 'rb') as f:
        # Read the number of chunks (first 4 bytes)
        num_chunks = int.from_bytes(f.read(4), byteorder='big')
        
        decrypted_data = bytearray()
        
        # Read and decrypt each chunk
        for _ in range(num_chunks):
            # Read the length of this chunk (4 bytes)
            chunk_length = int.from_bytes(f.read(4), byteorder='big')
            # Read the encrypted chunk
            encrypted_chunk = f.read(chunk_length)
            
            # Decrypt the chunk
            decrypted_chunk = private_key.decrypt(
                encrypted_chunk,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
            
            # Add the decrypted chunk to our result
            decrypted_data.extend(decrypted_chunk)
    
    # Write the decrypted data to the output file
    with open(output_file_path, 'wb') as f:
        f.write(decrypted_data)
    
    return True

def main():
    # Path to the cryptography folder
    cryptography_folder = r"C:\Users\ymani\OneDrive\Desktop\Projects\Keylogger\cryptography"
    
    # Path to the private key
    private_key_path = os.path.join(cryptography_folder, "private_key.pem")
    
    # Encrypted files
    encrypted_files = [
        os.path.join(cryptography_folder, "e_systeminfo.txt"),
        os.path.join(cryptography_folder, "e_clipboard.txt"),
        os.path.join(cryptography_folder, "e_key_log.txt")
    ]
    
    # Output files
    output_files = [
        "decrypted_systeminfo.txt",
        "decrypted_clipboard.txt",
        "decrypted_key_log.txt"
    ]
    
    for i, encrypted_file in enumerate(encrypted_files):
        if os.path.exists(encrypted_file) and os.path.getsize(encrypted_file) > 0:
            try:
                print(f"Decrypting {os.path.basename(encrypted_file)}...")
                success = decrypt_file(private_key_path, encrypted_file, output_files[i])
                
                if success:
                    print(f"Successfully decrypted to {output_files[i]}")
                else:
                    print(f"Failed to decrypt {os.path.basename(encrypted_file)}")
            except Exception as e:
                print(f"Error decrypting {os.path.basename(encrypted_file)}: {e}")
        else:
            print(f"Skipping {os.path.basename(encrypted_file)} because it doesn't exist or is empty")

if __name__ == "__main__":
    main()