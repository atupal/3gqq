import os
os.system('scp -P 56369  atupal@168.63.179.223:~/img.jpg img.gif')

from PIL import Image
image = Image.open('./img.gif')
image.show()

with open('verify', 'w') as fi:
    fi.write(raw_input('verify:'))

os.system('scp -P 56369  verify atupal@168.63.179.223:~/verify')
