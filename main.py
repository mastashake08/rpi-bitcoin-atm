import qrcode
from bitcoin import *
import subprocess
import numpy as np
my_private_key = random_key()

my_public_key = privtopub(my_private_key)

addr = pubtoaddr(my_public_key)
print(addr)
data = "Your BTC address is " + addr + "and your private key is " + my_private_key
img = qrcode.make(data)
path = addr+'.png'
img.save(path)
lpr =  subprocess.call(["/usr/bin/lp", path])

