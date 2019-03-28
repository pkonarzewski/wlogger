"""
Worklog time.
"""

import argparse
import logging
from pathlib import Path
from datetime import datetime, timedelta
from collections import namedtuple


logger = logging.getLogger('worklogger')
hdlr = logging.FileHandler(Path('~').expanduser() / 'work_logger.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

Row = namedtuple('row', ['date', 'action'])

date_format = '%Y-%m-%d %H:%M:%S'

parser = argparse.ArgumentParser(description='Worklog script')
parser.add_argument('action', choices=['start', 'stop', 'status', 'report', 'bye'], type=str)
parser.add_argument('-d', '--date', required=False, type=str, default=datetime.now())
# parser.add_argument('-b', '--break', required=False, type=bool, default=False)
# parser.add_argument('-t', '--test')
# parser.add_argument('--shutdown')


def generate_excel_report(log_path):

    import pandas as pd

    df = (
        pd.read_csv(log_path, delimiter=';', parse_dates=['time'])
        .assign(date=lambda x: x.time.dt.strftime('%Y-%m-%d'))
        .pivot(index='date', columns='action', values='time')
        .assign(diffz=lambda x: x.stop - x.start)
        .assign(overtime=lambda x: x.diffz - pd.Timedelta('8 hours'))
        .assign(cum_overtime=lambda x:x.overtime.cumsum())
        .loc[:,['start', 'stop', 'overtime', 'cum_overtime']]
    )

    return df

# iterator - generator
# find today rows
def seek_row():
    pass


def normalize_time(dtime):
    dt = dtime.replace(microsecond=0)
    return dt


if __name__ == '__main__':

    args = parser.parse_args()
    script_date = normalize_time(args.date)

    report_file = Path.home() / 'work_log.csv'

    if report_file.exists() is False:
        with report_file.open(mode='w', encoding='utf8') as f:
            f.write('date;action\n')

    if args.action in ['start', 'stop']:

        logging.warning(args.action)

        # if args.b is True:
        #     action = 'break_'+args.action

        with open(report_file) as myfile:
            last_raw = Row(*list(myfile)[-1].split(';'))

        # if args.action == last_raw.action:
        #     raise ValueError('Last action: {}, now you want {}. start or stop previous block first.'.format(args.action, last_line_action))

        with report_file.open(mode='a', encoding='utf8') as f:
            f.write("{};{}\n".format(script_date.strftime(date_format), args.action))

    elif args.action == 'status':

        with open(report_file) as myfile:
            last_line = Row(*list(myfile)[-1].strip().split(';'))
            ddd = datetime.strptime(last_line.date, date_format)

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

    elif args.action == 'report':
        df = generate_excel_report(report_file)
        df.to_excel((report_file.parent / 'wlog_report.xlsx'))
