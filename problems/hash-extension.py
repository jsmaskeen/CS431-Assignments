import os
import binascii
import hashlib
SECRET_KEY = os.urandom(16)  

original_cookie = b"username=cns431&groups=students,users,"

original_sig = hashlib.sha256(SECRET_KEY + original_cookie).hexdigest()

print("Welcome to the CNS431 Hash Extension Attack Challenge!")
print("\nHere is your cookie as plaintext:")
print(original_cookie.decode())

print("\nAnd here it is as hex:")
print(binascii.hexlify(original_cookie).decode())

print("\nSECRET_KEY is a 16-byte key that is unknown to you")
print("The signature is computed as SHA256(SECRET_KEY || message)")
print("The signature of your cookie is:")
print(original_sig)

k = input("\nPlease provide your cookie encoded as hex: ")

try:
    decoded = binascii.unhexlify(k)
except Exception:
    print("Invalid hex input!")
    exit()

sig = input("Please provide the signature SHA256(SECRET_KEY || message) of the cookie:\n")

computed_sig = hashlib.sha256(SECRET_KEY + decoded).hexdigest()

print(f"\nDecoded cookie: {decoded!r}")
print(f"Computed signature: {computed_sig}")
print(f"Provided signature: {sig}")

if sig == computed_sig:
    print("Signature verified")
    if b"admins" in decoded:
        print("Welcome admin! Here is your flag:")
        print("431fl@g{D3@D3Xt3ns!0nL3ngth}")
    else:
        print("Welcome user!")
else:
    print("Invalid signature. This incident will be reported.")

print("Goodbye")
