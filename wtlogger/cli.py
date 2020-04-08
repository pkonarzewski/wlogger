"""Command line interface."""

import argparse
from pathlib import Path
from datetime import datetime, timedelta

from wtlogger.app import WorkLogger
import wtlogger.config as conf
from wtlogger.utils import normalize_time, system_shutdown
from wtlogger.db import initdb, upgradedb


parser = argparse.ArgumentParser(description="Worklog script")
parser.add_argument(
    "action",
    choices=["start", "stop", "status", "log", "test", "version", "initdb"],
    type=str,
)
parser.add_argument(
    "-d",
    "--date",
    required=False,
    type=str,
    default=datetime.now(),
    help="set time of action, default is now",
)
parser.add_argument(
    "--bye", action="store_true", help='shutdown system after "stop" action'
)
parser.add_argument(
    "-dr", "--duration", required=False, type=int, help="event duration (in minutes)"
)


def main():
    """Main."""

    args = parser.parse_args()
    script_date = normalize_time(args.date)
    worklog = WorkLogger()

    conf.LOGGER.info(args.action)
    if args.action == "start":
        worklog.start_work(script_date)

    elif args.action == "stop":
        worklog.stop_work(script_date)

        if args.bye:
            system_shutdown()

    elif args.action == "status":
        worklog.workday_status(script_date)

    elif args.action == "log":
        worklog.show_last_intervals()

    elif args.action == "test":
        print("TEST")

    elif args.action == "version":
        print(f"version: {conf.VERSION_STR}")

    elif args.action == "initdb":
        initdb()

    elif args.action == "upgradedb":
        upgradedb()

    elif args.action == "import":
        pass

    elif args.action == "export":
        pass
