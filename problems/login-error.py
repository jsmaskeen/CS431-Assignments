import os
import time
import sys
import hashlib

try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
except ImportError:
    print("Error: This challenge requires 'pycryptodome'.")
    print("Please install it using: pip install pycryptodome")
    sys.exit(1)

KEY = os.urandom(16) 
BLOCK_SIZE = 16

def get_flag(roll_no):
    """Generates a flag similar to the transcript format."""
    timestamp = str(time.time())
    random_hash = hashlib.sha256(os.urandom(32)).hexdigest()
    return f"cnsctf{{{roll_no}_{timestamp}_{random_hash}}}"

def encrypt_data(plaintext):
    """
    Encrypts data using AES-CBC with a random IV.
    Returns the hex string of (IV + Ciphertext).
    """
    iv = os.urandom(BLOCK_SIZE)
    cipher = AES.new(KEY, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode(), BLOCK_SIZE)
    encrypted = cipher.encrypt(padded_data)
    return (iv + encrypted).hex()

def decrypt_data(hex_string):
    """
    Decrypts hex string (IV + Ciphertext).
    Returns tuple: (Plaintext, ErrorMessage)
    """
    try:
        # Convert hex to bytes
        data = bytes.fromhex(hex_string)
        
        if len(data) < BLOCK_SIZE:
            return None, "Error! Data too short."
            
        # Extract IV (first 16 bytes) and Ciphertext
        iv = data[:BLOCK_SIZE]
        ciphertext = data[BLOCK_SIZE:]
        
        cipher = AES.new(KEY, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)
        
        # Unpad raises ValueError if padding is invalid
        plaintext = unpad(decrypted, BLOCK_SIZE)
        
        # Return decoded string (ignoring errors to allow seeing "garbled" text if needed)
        return plaintext.decode(errors='ignore'), "Success"
        
    except (ValueError, KeyError):
        return None, "Padding is incorrect."
    except Exception:
        return None, "Error! Something went wrong."

def main():
    try:
        print("Welcome to our super cool AES-encryption portal!")
        print("Oops! We forgot the admin credentials, but we remember the username was like c?s and the password was like c?f.")
        
          
        original_user = "user:c?s"
        original_pass = "pass:c?f"
        
        user_hex = encrypt_data(original_user)
        pass_hex = encrypt_data(original_pass)
        
        print(f"When we tried '{original_user}' and '{original_pass}', the portal gave us these hex strings:\n")
        print(user_hex)
        print(pass_hex)
        print("\nTo unlock the portal, enter the correct hex strings that decrypt to the right credentials. Good luck!")

        roll_no = ""
        while True:
            roll_no = input("Enter your 8 digit roll no : ")
            if len(roll_no) == 8 and roll_no.isdigit():
                break
            else:
                print("Please give a valid roll no")

        input_user_hex = input("Enter username hex string : ").strip()
        input_pass_hex = input("Enter password hex string : ").strip()
        

        decrypted_user, u_msg = decrypt_data(input_user_hex)
        if not decrypted_user:
            print(u_msg)
            if u_msg == "Padding is incorrect.":
                print("Error! Something went wrong. Try to connect again.")
            return

        decrypted_pass, p_msg = decrypt_data(input_pass_hex)
        if not decrypted_pass:
            print(p_msg)
            if p_msg == "Padding is incorrect.":
                print("Error! Something went wrong. Try to connect again.")
            return

        if "user:cns" in decrypted_user and "pass:ctf" in decrypted_pass:
            print("Congratulations! You've unlocked the portal!")
            print(f"Here's the flag for your efforts: {get_flag(roll_no)}")
        else:
            print("Not even close. Try again!")

    except KeyboardInterrupt:
        print("\nExiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()