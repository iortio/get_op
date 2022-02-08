import os


# Create api folder
if not os.path.isdir('/opt/api'):
    os.mkdir('/opt/api')

# Create API file
fo = open('/opt/api/main.py', 'w')

# Add header
fo.write('from typing import Optional, Union\n')
fo.write('from fastapi import FastAPI\n')
fo.write('from pydantic import BaseModel\n\n')
fo.write('app = FastAPI()\n\n')

# Iterate over endpoints
for root, dirs, files in os.walk("endpoints", topdown=False, followlinks=True):
    for name in files:
        if name == 'main.py':
            fo.write('# %s\n' % (root))
            fo.write(open(os.path.join(root, name), 'r').read())
            fo.write('\n\n')

# Close API file
fo.close()
