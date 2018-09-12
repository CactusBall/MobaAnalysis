import time
from datetime import date

import pandas as pd
import simplejson

hour = {
    '00': [],
    '01': [],
    '02': [],
    '03': [],
    '04': [],
    '05': [],
    '06': [],
    '07': [],
    '08': [],
    '09': [],
    '10': [],
    '11': [],
    '12': [],
    '13': [],
    '14': [],
    '15': [],
    '16': [],
    '17': [],
    '18': [],
    '19': [],
    '20': [],
    '21': [],
    '22': [],
    '23': []
}

week = {
    '0': [],
    '1': [],
    '2': [],
    '3': [],
    '4': [],
    '5': [],
    '6': [],
}


def read_csv(file_path):
    csv_data = pd.read_csv(file_path)
    battle_times = csv_data['dt_event_time']
    for battle_time in battle_times:
        get_week_day_from_timestamp(battle_time)
        get_hour_from_timestamp(battle_time)


def get_week_day_from_timestamp(timestamp):
    week_day = date.fromtimestamp(timestamp).weekday()
    week[str(week_day)].append(week_day)
    week['6'].append(week_day)


def get_hour_from_timestamp(timestamp):
    timestruct = time.localtime(timestamp)
    battle_hour = time.strftime('%H', timestruct)
    hour[battle_hour].append(battle_hour)
    hour[battle_hour].append(battle_hour)


def write_file(hour, week):
    hours = hour.keys()
    for h in hours:
        hour[h] = len(hour[h])
    weeks = week.keys()
    for w in weeks:
        week[w] = len(week[w])
    with open('./battle_hours.json', 'w', encoding='utf-8') as f:
        f.write(simplejson.dumps(hour, indent=2, sort_keys=True, ensure_ascii=False))
    with open('./battle_weeks.json', 'w', encoding='utf-8') as f:
        f.write(simplejson.dumps(week, indent=2, sort_keys=True, ensure_ascii=False))


read_csv('/Users/emrys/Documents/BattleList.csv')
write_file(hour, week)
