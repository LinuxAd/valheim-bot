#!/usr/bin/env python3

import subprocess
import time


class Status:
    def __init__(self,description, active, loaded, restart, substate):
        self.description = description
        self.active = active
        self.loaded = loaded
        self.restart = restart
        self.substate = substate

    def __str__(self):
        return f"{self.description}\n\n" \
               f"Active: {self.active}\n" \
               f"Loaded: {self.loaded}\n" \
               f"Restart: {self.restart}\n" \
               f"State: {self.substate}"

class Service:
    def __init__(self, name):
        self.service_name = name + ".service"
        self.name = name

    def __build_command(self, cmd: str) -> str:
        return f"sudo systemctl {cmd} {self.service_name}"

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

    def stop(self) -> str:
        cmd = self.__build_command("stop")
        self.__sub_run(cmd)
        time.sleep(1)
        return self.check_status()

    def start(self) -> str:
        cmd = self.__build_command("start")
        out = self.__sub_check_output(cmd)
        return out.decode()

    def check_status(self) -> str:

        run = self.__sub_check_output(f"systemctl show {self.name} --no-page")
        out = run.decode()
        out_dict = {}
        for line in out:
            kv = line.split("=", 1)
            if len(kv) == 2:
                out_dict[kv[0]] = kv[1]

        s = Status(
            out_dict["Description"],
            out_dict["ActiveState"],
            out_dict["LoadState"],
            out_dict["Restart"],
            out_dict["SubState"],
        )

        return f"Status Report:\n\n{s}"
