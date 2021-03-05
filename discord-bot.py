#!/usr/bin/env python3
from systemd import service
import sysinfo
import os
import time
from discord.ext import commands
import logging
from dotenv import load_dotenv

VALHEIM_SERVICE = "valheimserver"
valheim = service.Service(VALHEIM_SERVICE)
logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


def check_status(serv: service.Service):
    stat = serv.check_status()
    return stat


def restart_service(serv: service.Service):
    print(f"restarting {VALHEIM_SERVICE}")
    serv.restart()
    stat = serv.check_status()
    print(f"status: {stat}")


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


@bot.command(name='restart', help="Restarts the valheim server")
async def restart_valheim(ctx):
    await ctx.send(f"yes master {0.author.mention}")
    await ctx.send(f"powered by {0.author}")
    await ctx.send("restarting the valheim server service, I'll report back when done")
    time.sleep(5)
    await ctx.send("Just pretending - I don't trust you with this kind of power yet")


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
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
