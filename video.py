from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


def encrypt_video(input_file, output_file, key):
    cipher = AES.new(key, AES.MODE_CBC)
    with open(input_file, 'rb') as infile:
        plaintext = infile.read()
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))

    with open(output_file, 'wb') as outfile:
        outfile.write(cipher.iv)
        outfile.write(ciphertext)


def decrypt_video(input_file, output_file, key):
    with open(input_file, 'rb') as infile:
        iv = infile.read(AES.block_size)
        ciphertext = infile.read()

    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

    with open(output_file, 'wb') as outfile:
        outfile.write(plaintext)
