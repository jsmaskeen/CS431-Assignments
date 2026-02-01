a = input("""As you know already, we have intercepted a message, but it seems to be encrypted.
Luckily, we found the key written on a sticky note nearby.
Key: VICTORY
Ciphertext: Be3cmXfz!T0cEk4qb3bDb

Decrypt the message and verify the passcode to get the flag: """)

corr = 'Gw3atJob!Y0uCr4ck3dIt'
if a!=corr:
    tries = 0
    while tries < 9:
        a = input('Incorrect. Try again: ')
        tries +=1
        if a == corr:
            break
    if a!=corr:
        print('Too many failed attempts. Bye! ')

if a == corr:
    print(r'Correct! Here is your flag: CNS431{v1g3n3r3_c1ph3r_1s_cl4ss1c}')
    