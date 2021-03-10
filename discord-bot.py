#!/usr/bin/env python3
from systemd import service
import sysinfo
import os
import time
from discord.ext import commands
import logging
from dotenv import load_dotenv
import subprocess

logging.basicConfig(level=logging.INFO)

VALHEIM_SERVICE = "valheimserver"
bot = commands.Bot(command_prefix='odin ')


def emoji_percent_thresholds(num: float) -> str:
    color = "green"
    emoji = "circle"

    if num < 70.0:
        color = "green"
    elif 70.0 < num < 90.0:
        color = "yellow"
    elif num > 90:
        color = "red"

    return f":{color}_{emoji}:"


def emoji_status(status: str, good: str) -> str:
    if status == good:
        return ":white_check_mark:"
    else:
        return ":bangbang:"


class Valheim(commands.Cog):

    def __init__(self, b: commands.Bot, serv: service.Service):
        self.bot = b
        self.__serv = serv

    @commands.command(pass_context=True, help="Backup the Valheim server before you do something stupid")
    async def backup(self, ctx) -> int:
        out = subprocess.run("/home/steam/backup.sh".split(), shell=True, capture_output=True, text=True)
        if out.returncode != 0:
            await ctx.send(":fire: backup went horribly wrong! :fire:")
            logging.info(f"return code from backup: {out.returncode}")
            logging.info(f"output from backup: {out.stdout} {out.stderr}")
            await ctx.send(f"result: {out.stdout} {out.stderr}")
            return
        else:
            await ctx.send(":100: Backed up successfully :100:")
        return out.returncode

    @commands.command(pass_context=True, help="Updates and restarts the valheim server")
    async def update(self, ctx):
        m = ctx.message
        logging.info(f"update started by {m.author}")
        await ctx.send(f"Starting an update of the valheim server service, I'll report back when done")
        await ctx.send("Stopping server...")
        self.__serv.stop()
        self.status(ctx)
        time.sleep(2)
        s = self.__serv.check_status()
        if s.active == "active":
            await ctx.send(f"Could not stop server process, :cry: status is: {s.active}")
            return
        await ctx.send("backing up important server files")

        b = self.backup()
        if b == 0:
            return

        self.status(ctx)
        await ctx.send(":100: Updating valheim server :100:")
        resp = self.__serv.start
        await ctx.send(resp)
        self.status(ctx)

    @commands.command(pass_context=True, help='Gets basic OS system metrics for the valheim server')
    async def system(self, ctx):
        met = sysinfo.Info()
        cpu_e = emoji_percent_thresholds(met.cpu)
        mem_e = emoji_percent_thresholds(met.mem_per)
        root_e = emoji_percent_thresholds(met.root)
        v_e = emoji_percent_thresholds(met.steam)

        resp = f"System metrics for the valheim server:\n" \
               f"{cpu_e} cpu: {met.cpu}%\n" \
               f"{mem_e} mem: {met.mem_per}% {met.mem}Gb\n" \
               f"{root_e} root: {met.root}%\n" \
               f"{v_e} valheim disk: {met.steam}%"
        await ctx.send(resp)

    @commands.command(pass_context=True, help="Gets the status of the Valheim server process")
    async def status(self, ctx):
        s = self.__serv.check_status()
        substate_emoji = emoji_status(s.substate, "running")
        active_emoji = emoji_status(s.active, "active")

        msg = f"Valheim Server\n\n" \
              f"{active_emoji} Status: {s.active}\n" \
              f"{substate_emoji}State: {s.substate}"
        await ctx.send(msg)


def main():
    valheim = service.Service(VALHEIM_SERVICE)

    @bot.event
    async def on_ready():
        logging.info(f'{bot.user.name} has connected to Discord!')

    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    if token == "":
        logging.error("token value was nil")
        exit(1)

    bot.add_cog(Valheim(bot, valheim))
    bot.run(token)


if __name__ == "__main__":
    main()
