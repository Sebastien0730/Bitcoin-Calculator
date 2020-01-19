import math
import os
import webbrowser
import requests
import pandas as pd
from bokeh.layouts import row
from bokeh.plotting import figure, output_file, show
from bokeh.models import HoverTool, ColumnDataSource
from datetime import datetime


clear = lambda: os.system('cls') #on Windows System
clear()


def calculate_hash_rate(dif):
    hash_rate = dif * (2**32)/600
    return hash_rate

def calculate_difficulty(hash):
    dif = 600 * hash /(2**32)
    return dif

def represent_in(H, last):
    return H * (10**(-last))

def calculate_quant(user, global_hash, reward):
    return (user/global_hash)*reward


def title():
    clear()
    print('**********************************************')
    print('*   WELCOME TO MY SUPER BITCOIN CALCULATOR   *')
    print('**********************************************')
    print()
    print()
    print('OPTION 1: CALCULATE HASH RATE WITH DIFFICULTY')
    print('OPTION 2: CALCULATE DIFFICULTY WITH HASH RATE')
    print('OPTION 3: SEE REAL-TIME GRAPH OF BITCOINS IN THE WEB')
    print('OPTION 4: WHAT CAN YOU MINE WITH YOUR CURRENT SETUP WITH THE CURRENT DIFFICULTY!!')
    print('OPTION 5: HOW MANY WILL IT TAKES TO MINE 1 FULL BITCOIN WITH MY SETUP?')
    print('OPTION 6: GENERATE GRAPHS (HASH RATE AND DIFFICULTY) WITH WEB DATA')
    print()
    choice = input('Choose an option (1, 2, 3, 4, 5, 6): ')
    if choice not in ['1', '2', '3','4', '5', '6']:
        while choice not in ['1', '2', '3', '4', '5', '6']:
            choice = input('WRONG OPTION! Choose an option (1, 2, 3, 4, 5, 6): ')

    if choice is '1':
        choice_1()
    elif choice is '2':
        choice_2()
    elif choice is '3':
        choice_3()
    elif choice is '4':
        choice_4()
    elif choice is '5':
        choice_5()
    elif choice is '6':
        choice_6()

def choice_1():
    clear()
    print('OPTION 1: CALCULATE HASH RATE WITH DIFFICULTY')
    print()
    dif = input('ENTER THE BLOCK DIFFICULTY (D): ')
    not_good = True
    while (not_good):
        try:
            dif = float(dif)
            not_good = False
        except:
            dif = input('WRONG INPUT: ENTER THE BLOCK DIFFICULTY (D): ')

    hash_power = represent_in(calculate_hash_rate(dif), 9)

    l = len(str(round(hash_power)))
    end = ['GH', 'TH', 'PH', 'EH']
    count = 0
    while l > 3:
        hash_power = represent_in(hash_power, 3)
        count += 1
        l = len(str(round(hash_power)))

    print('WITH THIS BLOCK DIFFICULTY, THE HASH POWER REQUIRED IS ' + str(
        hash_power) + ' ' + end[count] + '/s')
    input()

def choice_2():
    clear()
    print('OPTION 2: CALCULATE DIFFICULTY WITH HASH RATE')
    print()

    hash = input('ENTER THE HASH RATE IN GH, TH, PH or EH : ')
    hash = hash.split(' ')
    while len(hash) == 1 or hash[1] not in ['GH', 'TH', 'PH', 'EH']:
        hash = input('ERROR - ENTER THE HASH RATE IN GH, TH, PH or EH : ')
        hash = hash.split()

    final = 123456789
    if hash[1] == 'GH':
        final = calculate_difficulty(float(hash[0]) * 10**9)
    elif hash[1] == 'TH':
        final = calculate_difficulty(float(hash[0]) * 10**12)
    elif hash[1] == 'PH':
        final = calculate_difficulty(float(hash[0]) * 10**15)
    elif hash[1] == 'EH':
        final = calculate_difficulty(float(hash[0]) * 10**18)

    print('THE DIFFICULTY OF THIS HASH RATE IS: ' + str(int(final)))
    input()

def choice_3():
    print('OPTION 3: SEE REAL-TIME GRAPH OF BITCOINS IN THE WEB')

    webbrowser.open('https://btc.com/stats/diff')
    input()

def choice_4():
    clear()
    print('OPTION 4: WHAT CAN YOU MINE WITH YOUR CURRENT SETUP WITH THE CURRENT DIFFICULTY!!')
    url = 'https://blockexplorer.com/api/status?q=getDifficulty'
    r = requests.get(url=url)
    data = r.json()
    dif = data['difficulty']
    current_hash_rate = calculate_hash_rate(dif)
    hash_power = represent_in(current_hash_rate, 9)
    l = len(str(round(hash_power)))
    end = ['GH', 'TH', 'PH', 'EH']
    count = 0
    while l > 3:
        hash_power = represent_in(hash_power, 3)
        count += 1
        l = len(str(round(hash_power)))

    print()
    print('THE CURRENT HASH RATE POWER NEEDED FOR THE NEXT BLOCK IS ' + str(hash_power) + ' ' + end[count] + ' WITH A DIFFIULTY OF ' + str(dif))
    print('')
    user_hash_rate = input('WHAT IS THE CURRENT HASH POWER OF YOUR MACHINE IN HASHES PER SECOND: ')

    current_reward = 12.5

    quantity = calculate_quant(float(user_hash_rate), current_hash_rate, current_reward)

    print('')
    print('WITH THE CURRENT REWARD OF 12.5 BITCOINS FOR 2016 BLOCKS, YOU WILL GAIN: ' + str(quantity) + ' BITCOIN')
    input()

def choice_5():
    clear()
    print('OPTION 5: HOW MANY DAYS WILL IT TAKES ME TO MINE 1 FULL BITCOIN WITH MY SETUP?')
    print()
    current_hash = input('ENTER YOUR CURRENT HASHPOWER IN H/s: ')
    url = 'https://blockexplorer.com/api/status?q=getDifficulty'
    r = requests.get(url=url)
    data = r.json()
    dif = data['difficulty']
    time = (dif * (2**32)) / float(current_hash)
    print()
    print('WITH YOUR CURRENT SETUP, IT WILL TAKE YOU ' + str(time) + ' DAYS TO MINE 1 FULL BITCOIN')
    input()


def choice_6():
    clear()
    data = pd.read_csv('bitcoin.csv')
    data = data[['timestamp', 'average_hashrate', 'diff']]
    date = []
    hash = []
    dif = []
    timestamp = data['timestamp'].tolist()
    count = 0
    for item in timestamp:
        cur = datetime.fromtimestamp(item)
        if cur.year == 2018 or cur.year == 2019 or cur.year == 2020:
            date.append(cur)
            hash.append(represent_in(float(data['average_hashrate'].tolist()[count]), 12))
            dif.append(data['diff'].tolist()[count])
        count += 1
    output_file('graph.html')
    source = ColumnDataSource(data=dict(
        date=date,
        hashrate=hash,
    ))
    source2 = ColumnDataSource(data=dict(
        date=date,
        dif=dif,
    ))
    p = figure(title="Hashrate in the last 2 years", x_axis_label='Datetime', x_axis_type='datetime', y_axis_label='Hashrate', width=840, height=550)
    p.line('date', 'hashrate', legend_label="Hashrate TH/s", line_width=2, color="#00CED1", source=source)
    s = figure(title="Difficulty in the last 2 years", x_axis_label='Datetime',x_axis_type='datetime', y_axis_label='Difficulty', width=840, height=550)
    s.line('date', 'dif', legend_label="Difficulty", line_width=2, color="#00CED1", source=source2)
    hover = HoverTool(
        tooltips=[
            ('date', '@date{%F}'),
            ('hashrate', '@hashrate{000,00 TH}')
        ],
        formatters={
            'date': 'datetime',
        },
        mode = 'vline'
    )
    p.add_tools(hover)
    hover2 = HoverTool(
        tooltips=[
            ('date', '@date{%F}'),
            ('difficulty', '@dif')
        ],
        formatters={
            'date': 'datetime',
        },
        mode='vline'
    )
    s.add_tools(hover2)
    show(row(p, s))

    input()

if __name__ == '__main__':
    while True:
        title()







