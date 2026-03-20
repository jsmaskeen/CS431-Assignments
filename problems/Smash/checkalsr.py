from pwn import *

p = process(['./hello'], env={'LD_PRELOAD': './libc-2.23.so'})

libc_base = [addr for path, addr in p.libs().items() if 'libc' in path][0]
print(hex(libc_base))