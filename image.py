from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from PIL import Image
import os


def encrypt_image(input_image_path, output_image_path, key):
    image = Image.open(input_image_path)
    image_data = image.tobytes()

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(image_data, AES.block_size))

    encrypted_image = Image.frombytes(image.mode, image.size, encrypted_data)
    encrypted_image.save(output_image_path)


def decrypt_image(input_image_path,filename, output_image_path, key):
    try:
        encrypted_image = Image.open(input_image_path)
        encrypted_data = encrypted_image.tobytes()

        # Decrypt the data
        outputfile = os.path.join(output_image_path,filename)
        encrypted_image.save(outputfile)
        cipher = AES.new(key, AES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size, style='pkcs7')

        # Create a new image from the decrypted data
        decrypted_image = Image.frombytes(encrypted_image.mode, encrypted_image.size, decrypted_data)

        # Save the decrypted image
        decrypted_image.save(output_image_path)
    except:
        return "Something went wrong"

    
