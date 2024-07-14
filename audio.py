from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_audio(input_file, output_file, key):
    # Read the audio file
    print(input_file, output_file)
    with open(input_file, 'rb') as file:
        audio_data = file.read()

    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)

    # Create an AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Pad the audio data to be a multiple of the block size
    padded_audio_data = pad(audio_data, AES.block_size)

    # Encrypt the padded audio data
    encrypted_audio_data = cipher.encrypt(padded_audio_data)

    # Write the IV and encrypted data to the output file
    with open(output_file, 'wb') as file:
        file.write(iv + encrypted_audio_data)


def decrypt_audio(input_file, output_file, key):
    # Read the encrypted audio file
    with open(input_file, 'rb') as file:
        encrypted_data = file.read()

    # Extract the IV from the first block
    iv = encrypted_data[:AES.block_size]

    # Create an AES cipher object with the given key and IV
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the audio data
    decrypted_audio_data = cipher.decrypt(encrypted_data[AES.block_size:])

    # Unpad the decrypted audio data
    unpadded_audio_data = unpad(decrypted_audio_data, AES.block_size)

    # Write the decrypted audio data to the output file
    with open(output_file, 'wb') as file:
        file.write(unpadded_audio_data)
