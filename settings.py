

import socket

host = socket.gethostname()

roots = {
    'agni.local': '/Users/chris/soccer',
    'agni': '/Users/chris/soccer',
    'bert': '/home/chris/www',
    'oscar': '/home/chris/soccer',
    'li1014-58': '/home/chris/soccer',
    'jason': '/home/chris/soccer',

    }

ROOT_DIR = roots[host]

