from stegano import lsb
import cv2
import os
import sys
import aesutil
import shutil
from termcolor import cprint 
from pyfiglet import figlet_format
import rsautil1

# Clear the terminal screen for a clean start
os.system('cls' if os.name == 'nt' else 'clear')

# Display the main title and subtitle with artistic ASCII fonts
cprint(figlet_format('Secure Stegano', font='roman'), 'cyan', attrs=['bold'])
cprint(figlet_format('Video Steganography', font='cybermedium'), 'magenta', attrs=['bold'])

# Global variable to hold the path of the encoded video
ENCODED_VIDEO = sys.argv[1]
temp_folder = "tmp2"

# User choice for frame extraction method
frame_choice = int(input("Choose method: \n 1) Extract frames from image \n 2) Enter frame numbers manually : "))
decoded = {}

# Handling user's choice for frame extraction
if frame_choice == 1:
    ENCODED_IMAGE = input("\nEnter image name with extension: ")
    res = lsb.reveal(ENCODED_IMAGE)
    print(f"Encrypted frame numbers: {res}")
    cprint("Select encryption type: \n 1.AES {Symmetric} \n 2.RSA {Asymmetric}")
    Encryption_Style = int(input(""))
    
    # Decryption using AES
    if Encryption_Style == 1:
        key = input("Enter the symmetric key for AES: ")
        key_rsa = rsautil1.decrypt(message=key)
        key_rsa = key_rsa.decode('utf-8')
        print(f"Symmetric decrypted key: \n {key_rsa}")
        key123 = int(input("Choose key type to decrypt image: \n 1.HEX \n 2.ASCII : "))
        key = input("Enter the key to decrypt image: ")
        
        if key123 == 1:
            msg = aesutil.decrypt(key=key, source=res)
            msg1 = msg.decode('utf-8')
            cprint(f"Decoded image: \n {msg}", 'magenta')
            FRAMES = list(map(int, input("Enter Above FRAME NUMBERS separated by space: ").split()))
        else:
            msg = aesutil.decrypt(key=key, source=res, keyType='ascii')
            msg1 = msg.decode('utf-8')
            cprint(f"Decoded image: \n {msg1}", 'magenta')
            FRAMES = list(map(int, input("Enter Above FRAME NUMBERS separated by space: ").split()))
    
    # Decryption using RSA
    else:
        cprint("Decrypting with private key from 'keys' folder", 'red')
        msg1 = rsautil1.decrypt(message=res)
        msg1 = msg1.decode('utf-8')
        cprint(f"Decoded image: \n {msg1}", 'magenta')
        FRAMES = list(map(int, input("Enter Above frame numbers separated by space: ").split()))
    
# Manual entry of frame numbers
else:
    FRAMES = list(map(int, input("Enter frame numbers separated by space: ").split()))
    cprint("Select decryption type: \n 1) AES {Symmetric} \n 2) RSA {Asymmetric}", 'blue')
    Encryption_Style = int(input(""))
    #print(FRAMES)

# Function to create a temporary directory if it doesn't exist
def createTmp():
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)

# Function to count the total number of frames in the video
def countFrames():
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return length

# Function to decode the video by extracting frames and revealing hidden data
def decodeVideo(number_of_frames):
    cap = cv2.VideoCapture(ENCODED_VIDEO)
    frame_number = -1
    while(frame_number <= number_of_frames):
        frame_number += 1
        frame_file_name = os.path.join(temp_folder, f"{frame_number}.png")
        encoded_frame_file_name = os.path.join(temp_folder, f"{frame_number}-enc.png")
        ret, frame = cap.read()

        if frame_number in FRAMES:
            cv2.imwrite(encoded_frame_file_name, frame)
            clear_message = lsb.reveal(encoded_frame_file_name)
            decoded[frame_number] = clear_message
            cprint(f"Frame {frame_number} DECODED: {clear_message}", 'blue')

# Function to clean up temporary files after processing
def clean_tmp(path="./tmp2"):
    if os.path.exists(path):
        shutil.rmtree(path)
        cprint("[INFO] Temporary files cleaned up", 'green')

# Function to arrange the decrypted frames and decrypt the complete message
def arrangeAndDecrypt():
    res = ""
    if Encryption_Style == 1:
        for fn in FRAMES:
            res += decoded[fn]
        cprint(f"Concatenated string: {res}", 'green')
        key123 = int(input("Choose key type: \n 1.HEX \n 2.ASCII : "))
        key = input("Enter the key: ")
        if key123 == 1:
            msg = aesutil.decrypt(key=key, source=res)
            msg1 = msg.decode('utf-8')
            cprint(f"Decoded message: \n {msg}", 'green')
            clean_tmp()
        else:
            msg = aesutil.decrypt(key=key, source=res, keyType='ascii')
            msg1 = msg.decode('utf-8')
            cprint(f"Decoded message: \n {msg1}", 'green')
            clean_tmp()
    else:
        for fn in FRAMES:
            res += decoded[fn]
        cprint(f"Concatenated string: {res}", 'green')
        cprint("Decrypting with private key from 'keys' folder", 'red')
        msg1 = rsautil1.decrypt(message=res)
        msg1 = msg1.decode('utf-8')
        cprint(f"Decoded text: \n {msg1}", 'green')
        clean_tmp()

# Program execution begins here
createTmp()
frames = countFrames()
decodeVideo(frames)
arrangeAndDecrypt()
