#!/usr/bin/env python3

import pydbus as dbus


class Service:
    def __init__(self, name):
        self.name = name+".service"
        self.bus = dbus.SystemBus()
        self.systemd = self.bus.get(".systemd1")

    def check_status(self):
        self.systemd.StatusUnit(self.name)