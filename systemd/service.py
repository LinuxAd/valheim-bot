#!/usr/bin/env python3

import subprocess


class Service:
    def __init__(self, name):
        self.name = name

    def __build_command(self, command: str) -> str:
        return f"systemctl {command} {self.name}.service"

    def check_status(self) -> bytes:
        cmd = self.__build_command("status").split()
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=2)
        return res.stdout
