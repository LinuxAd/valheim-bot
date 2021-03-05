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
valheim = service.Service(VALHEIM_SERVICE)


def check_status(serv: service.Service):
    stat = serv.check_status()
    return stat


def valheim_backup():
    out = subprocess.run("/home/steam/backup.sh".split(), shell=True, capture_output=True, text=True)
    return out


def get_system_metrics() -> sysinfo.Info:
    return sysinfo.Info()


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


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='update', help="Updates and restarts the valheim server")
async def update_valheim_server(ctx):
    m = ctx.message
    await ctx.send(f"ok {m.author.mention} updating the valheim server service, I'll report back when done")
    await ctx.send("stopping server...")
    stop = valheim.stop()
    await ctx.send(f"stop output: {stop}")
    time.sleep(5)
    await ctx.send("backing up important server files")
    backup = valheim_backup()
    await ctx.send(f"backup script result: {backup}")
    await status(ctx)
    await ctx.send("starting valheim server")
    resp = valheim.start
    await ctx.send(resp)
    await ctx.send(valheim.check_status())


@bot.command(name='status', help="Gets the status of the Valheim server process")
async def status(ctx):
    resp = check_status(valheim)
    await ctx.send(resp)


@bot.command(name='system', help='Gets basic OS system metrics for the valheim server')
async def status(ctx):
    met = get_system_metrics()
    cpu_e = emoji_percent_thresholds(met.cpu)
    mem_e = emoji_percent_thresholds(met.mem_per)
    root_e = emoji_percent_thresholds(met.root)
    v_e = emoji_percent_thresholds(met.steam)

    resp = f"System metrics for the valheim server:\n" \
           f"{cpu_e} cpu: {met.cpu}%\n" \
           f"mem:{mem_e} {met.mem_per} {met.mem}Gb\n" \
           f"{root_e} root: {met.root}%\n" \
           f"{v_e} valheim disk: {met.steam}%"
    await ctx.send(resp)


def main():
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    bot.run(token)


if __name__ == "__main__":
    main()
