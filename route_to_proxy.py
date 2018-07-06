import sys
import json
from subprocess import call

try:
  with open(sys.argv[1], 'r') as f:
    config = json.loads(f.read())

except:
  exit()

call(["/bin/bash", "setRoutes.sh", config["real_address"], config["torii_port"], config["yac_port"], config["fake_port"] ])
#call(["/bin/bash", "unsetRoutes.sh", config["real_address"], config["torii_port"], config["yac_port"], config["fake_port"] ])