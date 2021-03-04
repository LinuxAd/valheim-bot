#!/usr/bin/env python3

import subprocess


class Service:
    def __init__(self, name):
        self.service_name = name + ".service"
        self.name = name

    def __build_command(self, cmd: str) -> str:
        return f"systemctl {cmd} {self.service_name}"

    @staticmethod
    def __sub_run(cmd: str):
        return subprocess.run(cmd.split(),
                              shell=True, capture_output=True, text=True)

    @staticmethod
    def __sub_check_output(cmd: str) -> bytes:
        try:
            out = subprocess.check_output(cmd.split())
        except subprocess.CalledProcessError as err:
            out = err.stdout
        return out

    def restart(self):
        cmd = self.__build_command("restart")
        out = self.__sub_check_output(cmd)
        print(out.decode())

    def check_status(self) -> str:

        cmd = self.__build_command("status")
        run = self.__sub_check_output(cmd)

        out = run.decode()
        out_str = out.split()
        x = 0
        y = 0
        i = 0
        while i < len(out_str):

            if out_str[i] == "Active:":
                x = i
            if out_str[i] == "Docs:":
                y = i
            i += 1

        strings = out_str[x:y-1]

        return f"The {self.name} service status is:\n{' '.join(strings)}"
