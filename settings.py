

import socket

host = socket.gethostname()

roots = {
    'agni.local': '/Users/chris/soccer',
    'agni': '/Users/chris/soccer',
    'Christophers-MacBook-Air.local': '/Users/chirs/soccer',
    'Christophers-MacBook-Air': '/Users/chirs/soccer',
    'bert': '/home/chris/www',
    'oscar': '/home/chris/soccer',
    'li1014-58': '/home/chris/soccer',
    'jason': '/home/chris/soccer',

    }

ROOT_DIR = roots[host]

