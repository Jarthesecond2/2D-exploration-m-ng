"""Utils"""

import random

def search_trash_can():
    roll = random.randint(1, 100)
    if roll <= 15:
        return "Bottle"
    elif roll <= 74:
        return "Trash"
    elif roll <= 75:
        return "Token"
    else:
        return "Nothing"