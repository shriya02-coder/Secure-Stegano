from stegano import lsb  # For steganography in images
import cv2  # For handling videos and images
import math  # For mathematical operations
import os  # For handling file operations
import shutil  # For directory operations
from subprocess import call, STDOUT  # For calling command-line arguments
import aesutil  # For AES encryption and decryption
import sys  # For accessing system parameters
from termcolor import cprint  # For printing colored text in the terminal
from pyfiglet import figlet_format  # For ASCII art headers
import rsautil1  # For RSA encryption and decryption
import PIL.Image as PILImage  # For image operations

# Function to split strings into equal parts
def split_string(s_str, count=15):
    per_c = math.ceil(len(s_str) / count)
    c_count = 0
    out_str = ''
    split_list = []
    for s in s_str:
        out_str += s
        c_count += 1
        if c_count == per_c:
            split_list.append(out_str)
            out_str = ''
            c_count = 0
    if c_count != 0:
        split_list.append(out_str)
    return split_list

# Function to count frames in a video file
def countFrames():
    cap = cv2.VideoCapture(f_name)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cprint(f"Total frames in the video: {length - 1}", 'cyan')
    return length

# Function to extract frames from the video
def frame_extraction(video):
    if not os.path.exists("./tmp"):
        os.makedirs("tmp")
    temp_folder = "./tmp"
    cprint("[INFO] Temporary directory created", 'green')
    vidcap = cv2.VideoCapture(video)
    count = 0
    cprint("[INFO] Beginning frame extraction from video. This may take a while.", 'cyan')
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(temp_folder, f"{count}.png"), image)
        count += 1
    cprint("[INFO] Frame extraction complete.", 'green')

# Function to encode and encrypt the string into the frames
def encode_string(input_string, root="./tmp/"):
    cprint("\nSelect your preferred encryption type: \n 1.AES (Symmetric Encryption) \n 2.RSA (Asymmetric Encryption)")
    Encryption_Style = int(input(""))
    if Encryption_Style == 1:
        res = input_string
        key_type = int(input("\nChoose key type: \n 1.HEX \n 2.ASCII: "))
        key = input("\nEnter the encryption key: ")
        if key_type == 1:
            input_string = aesutil.encrypt(key=key, source=res)
        else:
            input_string = aesutil.encrypt(key=key, source=res, keyType='ascii')
        key_path = input("\nEnter path to recipient's public key to encrypt the AES key: ")
        key_rsa = rsautil1.encrypt(message=key, key_path=key_path).decode('utf-8')
        cprint(f"\nEncrypted key for the recipient: \n{key_rsa}", 'magenta')
        # Saving encrypted key for the receiver
        with open("./AES-encryption-key/ReceiverKey.txt", "wb") as file_obj:
            file_obj.write(key_rsa.encode())
        print(f"Encrypted message: {input_string}")
        split_string_list = split_string(input_string)
        split_string_length = len(split_string_list)
        FRAMES = list(map(int, input(f"\nEnter {split_string_length} frame numbers separated by spaces: ").split()))
        frame_choice = int(input("\n1.Store frame numbers in an image \n 2.Do not store frame numbers: "))
        if frame_choice == 1:
            ENCODE_IMAGE = input("\nEnter the name of the image file (with extension): ")
            res = str(FRAMES)
            if key_type == 1:
                FRAMES_ENCODED = aesutil.encrypt(key=key, source=res)
            else:
                FRAMES_ENCODED = aesutil.encrypt(key=key, source=res, keyType='ascii')
            secret = lsb.hide(ENCODE_IMAGE, str(FRAMES_ENCODED))
            secret.save("encrypt.png")
            cprint("[INFO] Frame numbers encrypted and stored in 'encrypt.png'.", 'green')
        else:
            cprint("[INFO] Frame numbers are not stored. Please keep them safe.", 'green')
    else:
        res = input_string
        key_path = input("\nEnter the public key file path: ")
        input_string = rsautil1.encrypt(message=res, key_path=key_path).decode('utf-8')
        print(f"\nEncrypted message: {input_string}")
        split_string_list = split_string(input_string)
        split_string_length = len(split_string_list)
        FRAMES = list(map(int, input(f"Enter {split_string_length} frame numbers separated by spaces: ").split()))
        frame_choice = int(input("\n 1.Store frame numbers in an image \n2.Do not store: "))
        if frame_choice == 1:
            ENCODE_IMAGE = input("\nEnter the name of the image file (with extension): ")
            res = str(FRAMES)
            FRAMES_ENCODED = rsautil1.encrypt(message=res, key_path=key_path).decode('utf-8')
            secret = lsb.hide(ENCODE_IMAGE, str(FRAMES_ENCODED))
            secret.save("encrypt.png")
            cprint("[INFO] Frame numbers encrypted and stored in 'encrypt.png'.", 'green')
        else:
            cprint("[INFO] Frame numbers are not stored. Please keep them safe.", 'green')
    for i in range(len(FRAMES)):
        frame_name = f"{root}{FRAMES[i]}.png"
        secret_enc = lsb.hide(frame_name, split_string_list[i])
        secret_enc.save(frame_name)
        cprint(f"[INFO] Frame {FRAMES[i]} now contains encrypted data.", 'green')

# Function to clean up temporary files
def clean_tmp(path="./tmp"):
    if os.path.exists(path):
        shutil.rmtree(path)
        cprint("[INFO] Temporary files cleaned up.", 'green')

# Main function to execute the program
def main():
    ENCODE_CHOICE = int(input("\nSelect input type: \n 1.Text \n 2.Text from document: "))
    if ENCODE_CHOICE == 1:
        TEXT_TO_ENCODE = input("\nEnter text to encrypt and encode: ")
        countFrames()
        frame_extraction(f_name)
        encode_string(TEXT_TO_ENCODE)
        call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        cprint("\nVideo successfully encoded with the encrypted text.", 'cyan')
        clean_tmp()
    else:
        FILE_TO_ENCODE = input("Enter the file path for the text document: ")
        with open(FILE_TO_ENCODE) as f:
            TEXT_TO_ENCODE = ''.join(f.readlines())
        countFrames()
        frame_extraction(f_name)
        encode_string(TEXT_TO_ENCODE)
        call(["ffmpeg", "-i", f_name, "-q:a", "0", "-map", "a", "tmp/audio.mp3", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "tmp/%d.png", "-vcodec", "png", "tmp/video.mov", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        call(["ffmpeg", "-i", "tmp/video.mov", "-i", "tmp/audio.mp3", "-codec", "copy", "video.mov", "-y"], stdout=open(os.devnull, "w"), stderr=STDOUT)
        cprint("Video successfully encoded with the encrypted text.", 'green')
        clean_tmp()

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    cprint(figlet_format('Secure Stegano', font='roman'), 'cyan', attrs=['bold'])
    cprint(figlet_format('Video Steganography', font='cybermedium'), 'magenta', attrs=['bold'])
    f_name = sys.argv[1]
    main()
