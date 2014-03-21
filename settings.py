

import socket

host = socket.gethostname()

roots = {
    'agni.local': '/Users/chris/soccer',
    'agni': '/Users/chris/soccer',
    'bert': '/home/chris/www',
    }

ROOT_DIR = roots[host]

