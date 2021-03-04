#!/usr/bin/env python3
from filelock import FileLock
from systemd import service
import sysinfo
import os
from tempfile import gettempdir

VALHEIM_SERVICE = "bluetooth"


def create_lock(lock_type: str) -> FileLock:
    lock_path = os.path.join(gettempdir(), lock_type + ".lock")
    lock = FileLock(lock_path)
    return lock


def check_status(serv: service.Service):
    print(f"checking the status of {VALHEIM_SERVICE}")
    lock = create_lock("status")
    lock.acquire(timeout=5)
    status = serv.check_status()
    print(status)
    lock.release()


def restart_service(serv: service.Service):
    print(f"restarting {VALHEIM_SERVICE}")
    lock = create_lock("restart")
    lock.acquire(timeout=5)
    serv.restart()
    status = serv.check_status()
    print(f"status: {status}")


def get_system_metrics():
    system = sysinfo.System
    cpu = system.get_cpu_load()
    mem = system.get_memory()
    steam = system.get_part_usage("/home/steam")
    print(f"cpu: {cpu}\nmem: {mem}Gb\npartition usage: {steam}%")


def main():
    valheim = service.Service(VALHEIM_SERVICE)
    check_status(valheim)
    restart_service(valheim)
    get_system_metrics()

if __name__ == "__main__":
    main()
