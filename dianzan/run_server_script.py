import paramiko

pkey_file = '/home/atupal/.ssh/id_rsa'
hostname = '168.63.179.223'
port = 56369

key = paramiko.RSAKey.from_private_key_file(pkey_file)

client = paramiko.SSHClient()
client.load_system_host_keys()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

client.connect(hostname, port, pkey=key)


import os
os.system('scp -P 56369 server_dianzan.py atupal@168.63.179.223:~/ts.py')

stdin, stdout, stderr = client.exec_command('pkill -9 python')
stdin, stdout, stderr = client.exec_command('nohup python ts.py &')

client.close()

#import subprocess
#P = subprocess.Popen()

os.system('scp -P 56369  atupal@168.63.179.223:~/img.jpg img.gif')

from PIL import Image
image = Image.open('./img.gif')
image.show()

with open('verify', 'w') as fi:
    fi.write(raw_input('verify:'))

os.system('scp -P 56369  verify atupal@168.63.179.223:~/verify')
