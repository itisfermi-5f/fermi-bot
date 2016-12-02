"""
This file is part of the fermi-bot project.
"""

import os
import csv
import threading
import utils


FIELD_NAMES = ('VM_IP', 'Telegram_ID')

users = [
    # utils.User(VM.IP, Telegram.ID)
]

serializer_lock = threading.Lock()

def load(path):
    if not os.path.ispath(path):
        raise OSError("path '{}' is not a file.".format(path))
    with serializer_lock:
        with open(path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                user = utils.User(ip=row[FIELD_NAMES[0]], id=row[FIELD_NAMES[1]])
                if user not in users:
                    users.append(user)


def save(path):
    if not os.path.isfile(path):
        raise OSError("path '{}' is not a file.".format(path))
    with serializer_lock:
        with open(path, 'w') as f:
            writer = csv.DictWriter(f, FIELD_NAMES)
            writer.writeheader()
            for user in users:
                writer.writerow({FIELD_NAMES[0]: user.ip, FIELD_NAMES[1]: user.id})
