#!/usr/bin/env python3
from filelock import FileLock
from systemd import service
import sysinfo
import os
from tempfile import gettempdir
from discord.ext import commands
from dotenv import load_dotenv

VALHEIM_SERVICE = "bluetooth"
valheim = service.Service(VALHEIM_SERVICE)

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
bot = commands.Bot(command_prefix='!')


def create_lock(lock_type: str) -> FileLock:
    lock_path = os.path.join(gettempdir(), lock_type + ".lock")
    lock = FileLock(lock_path)
    return lock


def check_status(serv: service.Service):
    lock = create_lock("status")
    lock.acquire(timeout=5)
    stat = serv.check_status()
    lock.release()
    return stat


def restart_service(serv: service.Service):
    print(f"restarting {VALHEIM_SERVICE}")
    lock = create_lock("restart")
    lock.acquire(timeout=5)
    serv.restart()
    stat = serv.check_status()
    print(f"status: {stat}")


def get_system_metrics() -> sysinfo.Info:
    system = sysinfo.System
    cpu = system.get_cpu_load()
    mem = system.get_memory()
    steam = system.get_part_usage("/home/steam")
    x = sysinfo.Info(cpu, mem, steam)
    return x


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='status')
async def status(ctx):
    await ctx.send(f"checking the status of {VALHEIM_SERVICE}")
    resp = check_status(valheim)
    await ctx.send(resp)


@bot.command(name='system')
async def status(ctx):
    met = get_system_metrics()
    resp = f"System metrics for the valheim server:\n" \
           f"cpu: {met.cpu}\n" \
           f"mem: {met.mem}Gb\n" \
           f"disk: {met.per}%"
    await ctx.send(resp)


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
