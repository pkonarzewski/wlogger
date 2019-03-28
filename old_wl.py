# TODO
# odpalanie z autostartu i rozpoczecie logowania (flaga)
# dodawanie pauzy
# dodanie logowania czasu juz i kiedy koniec
# grupowanie wpisow po jednym dniu
# konczenie logowania przy zamknieciu programu https://docs.python.org/2/library/atexit.html
from pathlib import Path
import numpy as np
import pandas as pd
import datetime


while True:
    command = input('(S)tart or s(t)op or (q)uit: ')
    if command.lower() == 's':

        name = f'worklog_{datetime.date.today().year}.xlsx'
        columns=['start', 'stop', 'duration', 'overtime', 'cumulative']
        exists = Path(name)
        if exists.is_file():
            df = pd.read_excel(name, sheet_name='worklog', index_col=0, dtype={k:str for k in columns})
        else:
            df = pd.DataFrame(columns=columns)

        start = datetime.datetime.now()

        new = {}
        new['start'] = start.strftime('%Y-%m-%d %H:%M')
        print(f'------------------------------ Start: {datetime.datetime.now().hour:02d}:{datetime.datetime.now().minute:02d}')

    elif command.lower() == 't':
        stop = datetime.datetime.now()
        new['stop'] = stop.strftime('%Y-%m-%d %H:%M')
        duration = datetime.datetime.strptime(new['stop'], '%Y-%m-%d %H:%M')-datetime.datetime.strptime(new['start'], '%Y-%m-%d %H:%M')
        overtime = duration-pd.Timedelta(8, unit='h')
        positive = f'{overtime.days*24+overtime.seconds//3600}:{(overtime.days*24*60+overtime.seconds//60)%60:02d}'
        negative = f'-{(-overtime).days*24+(-overtime).seconds//3600}:{(((-overtime).days*24+(-overtime).seconds)//60)%60:02d}'
        if exists.is_file():
            cumulative = pd.to_timedelta(df.iloc[-1,-1]+':00') + overtime
        else:
            cumulative = overtime

        cum_pos = f'{cumulative.days*24+cumulative.seconds//3600}:{(cumulative.days*24*60+cumulative.seconds//60)%60:02d}'
        cum_neg = f'-{(-cumulative).days*24+(-cumulative).seconds//3600}:{(((-cumulative).days*24+(-cumulative).seconds)//60)%60:02d}'
        if cumulative >= pd.Timedelta(0):
            new['cumulative'] = cum_pos
        else:
            new['cumulative'] = cum_neg

        new['duration'] = f'{duration.days*24+duration.seconds//3600}:{(duration.days*24*60+duration.seconds//60)%60:02d}'
        if overtime >= pd.Timedelta(0):
            new['overtime'] = positive
        else:
            new['overtime'] = negative
        df = df.append(new, ignore_index=True)
        df.index = df.start.apply(lambda x: x[:10])
        df.index.name = ''
        df.to_excel(name, sheet_name='worklog')

    elif command.lower() == 't':
        # pause
        pass

    elif command.lower() == 'l':
        # log time
        pass

    elif command.lower() == 'q':
        break
