#!/usr/bin/env python3
from filelock import FileLock
from systemd import service

VALHEIM_SERVICE = "bluetooth"


def create_lock(locktype: str) -> FileLock:
    lock_path = locktype + ".lock"
    lock = FileLock(lock_path)
    return lock


def main():
    lock = create_lock("status")
    lock.acquire(timeout=5)

    valheim = service.Service(VALHEIM_SERVICE)
    print(valheim.check_status())

    lock.release()

if __name__ == "__main__":
    main()
