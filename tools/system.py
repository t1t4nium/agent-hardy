"""System inspection tool: hostname, OS, date, load, and memory usage."""

import platform
from datetime import datetime

from agent.tools import tool


@tool
def system_info():
    """show system information"""  # First line is the tool's prompt description.
    uname = platform.uname()
    hostname = uname.node
    os = f"{uname.system} {uname.release} {uname.version} {uname.machine}"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z").strip()

    # /proc is Linux-only; report "unavailable" on other systems.
    load = ""
    try:
        with open("/proc/loadavg") as f:
            load = f.read().strip()
    except OSError:
        load = "unavailable"

    mem = swap = ""
    try:
        # /proc/meminfo values are in KiB.
        with open("/proc/meminfo") as f:
            info = {}
            for line in f:
                key, _, rest = line.partition(":")
                parts = rest.split()
                if parts:
                    info[key.strip()] = int(parts[0])
        total = info.get("MemTotal", 0)
        avail = info.get("MemAvailable", 0)
        used = total - avail
        mem = f"{used // 1024} MiB used / {total // 1024} MiB total"
        stotal = info.get("SwapTotal", 0)
        sfree = info.get("SwapFree", 0)
        sused = stotal - sfree
        swap = f"{sused // 1024} MiB used / {stotal // 1024} MiB total"
    except (OSError, ValueError):
        mem = swap = "unavailable"

    return (
        "system information:\n"
        f"hostname: {hostname}\n"
        f"os: {os}\n"
        f"date: {now}\n"
        f"load: {load}\n"
        f"mem usage: {mem}\n"
        f"swap usage: {swap}"
    )
