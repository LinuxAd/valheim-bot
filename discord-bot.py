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
bot = commands.Bot(command_prefix='!')


def emoji_percent_thresholds(num: float) -> str:
    color = "green"
    emoji = "circle"

    if num < 30.0:
        color = "green"
    elif 30.0 < num < 70.0:
        color = "yellow"
    elif num > 70:
        color = "red"

    return f":{color}_{emoji}:"


class Valheim(commands.Cog):

    def __init__(self, b: commands.Bot, serv: service.Service):
        self.bot = b
        self.__serv = serv

    @staticmethod
    def backup():
        out = subprocess.run("/home/steam/backup.sh".split(), shell=True, capture_output=True, text=True)
        return out

    @commands.command(pass_context=True, help="Updates and restarts the valheim server")
    async def update(self, ctx):
        m = ctx.message
        await ctx.send(f"ok {m.author.mention} updating the valheim server service, I'll report back when done")
        await ctx.send("stopping server...")
        self.__serv.stop()
        s = self.__serv.check_status()
        await ctx.send(f"{s.description} is {s.active}")
        time.sleep(5)
        await ctx.send("backing up important server files")
        backup = self.backup()
        if backup.returncode != 0:
            await ctx.send("backup went horribly wrong")
            logging.info(f"return code from backup: {backup.returncode}")
            logging.info(f"output from backup: {backup.stdout} {backup.stderr}")
            await ctx.send(f"result: {backup.stdout} {backup.stderr}")
            return

        for line in backup.stdout:
            await ctx.send(line)

        await self.status(ctx)
        await ctx.send("starting valheim server")
        resp = self.__serv.start
        await ctx.send(resp)
        fin_status = self.__serv.check_status()
        await ctx.send(f"{fin_status.description} is {fin_status.active}")

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
        msg = f"{s.description}\n\n" \
              f"Active: {s.active}\n" \
              f"Loaded: {s.loaded}\n" \
              f"Restart: {s.restart}\n" \
              f"State: {s.substate}"
        await ctx.send(msg)


def main():
    valheim = service.Service(VALHEIM_SERVICE)

    @bot.event
    async def on_ready():
        logging.info(f'{bot.user.name} has connected to Discord!')

    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot.add_cog(Valheim(bot, valheim))
    bot.run(token)


if __name__ == "__main__":
    main()
