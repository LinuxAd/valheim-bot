#!/usr/bin/env python3

import subprocess


class Service:
    def __init__(self, name):
        self.name = name+".service"

    def check_status(self):
        cmd = subprocess.run(f"systemctl status {self.name}", capture_output=True, text=True)
        print(cmd.stdout)
