#!/usr/bin/env python3
from filelock import FileLock
from systemd import service
import os
from tempfile import gettempdir

VALHEIM_SERVICE = "bluetooth"


def create_lock(lock_type: str) -> FileLock:
    lock_path = os.path.join(gettempdir(), lock_type + ".lock")
    lock = FileLock(lock_path)
    return lock


def check_status(serv: service.Service):
    lock = create_lock("status")
    lock.acquire(timeout=5)
    status = serv.check_status()
    print(status)
    lock.release()

def restart_service(serv: service.Service):
    lock = create_lock("restart")
    lock.acquire(timeout=5)
    status = serv.restart()


def main():
    valheim = service.Service(VALHEIM_SERVICE)
    check_status(valheim)
    restart_service(valheim)


if __name__ == "__main__":
    main()
