"""Command line interface."""

import argparse
from pathlib import Path
from datetime import datetime, timedelta

import wtl.config as conf
from wtl.utils import normalize_time, system_shutdown


parser = argparse.ArgumentParser(description='Worklog script')
parser.add_argument('action', choices=['start', 'stop', 'pause', 'event', 'status', 'log'], type=str)
parser.add_argument('-d', '--date', required=False, type=str, default=datetime.now())
parser.add_argument('--bye', action='store_true')


def main():
    """Main."""

    args = parser.parse_args()
    script_date = normalize_time(args.date)

    worklog = Path(conf.WORKLOG_FILE)


    if args.action in ['start', 'stop']:

        conf.LOGGER.warning(args.action)

        with worklog.open(mode='a', encoding='utf8') as f:
            f.write("{};{};{}\n".format(script_date.strftime(conf.DATE_FORMAT), args.action, ''))

        if args.action == 'stop' and args.bye is True:
            system_shutdown()

    elif args.action == 'status':

        with open(worklog) as myfile:
            last_line = conf.ROW(*list(myfile)[-1].strip().split(';'))
            ddd = datetime.strptime(last_line.date, conf.DATE_FORMAT)

            end_dd = ddd + timedelta(hours=8)

        start_date = ddd.time()
        planed_end_date = end_dd.time()

        wee_text = 'Pozostało'
        remaining = end_dd - script_date

        if remaining.total_seconds() < 0:
            remaining = abs(remaining)
            wee_text = 'Nadgodziny'

        print('W pracy od:\t', start_date,
            '\nKoniec o:\t', planed_end_date,
            '\n{}:\t {}'.format(wee_text, remaining)
        )

    elif args.action == 'log':
        with worklog.open(mode='r', encoding='utf8') as f:
            lines = f.readlines()
            for n in lines[-5:]:
                print(n, end='')
