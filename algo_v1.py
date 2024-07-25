import pandas as pd
import numpy as np
from py5paisa import FivePaisaClient
import matplotlib.pyplot as plt
import mplfinance as mpf
import os
from matplotlib import animation
from py5paisa.order import Order, OrderType, Exchange, bo_co_order
import datetime
from datetime import datetime, timedelta
import time
from py5paisa.strategy import *


def login_(dayf):
    df1 = None
    try:
        cred = {
            "APP_NAME": "5P56798712",
            "APP_SOURCE": "7311",
            "USER_ID": "beTMrRQlrqg",
            "PASSWORD": "IBMfbkUlj65",
            "USER_KEY": "maNpelRf7OS2yzGI8ToIV5zMgBWmouNA",
            "ENCRYPTION_KEY": "UEjzxjrpwi2DVWfOa3GM4L454tH5SYwp"
        }
        global client
        client = FivePaisaClient(email="yewuiuwi@Gmail.com", passwd="Pass@11231",
                                 dob="456186", cred=cred)

        client.login()

        df1 = client.historical_data('N', 'C', 999920005, '5m', f'2021-{mon}-{dayf}', f'2021-{mon}-{dayf}')
        print(df1)
    except Exception as e:
        print(e)
    return df1


def buy_sell(date):
    df = login_(date)
    if df is not None:

        df['Highv1'] = np.nan
        df['Lowv1'] = np.nan
        df['Openv1'] = np.nan

        df['sell'] = np.nan
        df['buy'] = np.nan

        '''
        stop-loss-sl2
        stop-loss-sl2-sell
        '''

        df['stop_loss_sl2'] = np.nan
        df['stop_loss_sl2_sell'] = np.nan

        df['stop_loss_sl2'] = np.nan
        df['stop_loss_sl2-sell'] = np.nan

        df['3:15-buy'] = np.nan
        df['3:15-sell'] = np.nan

        df['Highv1'].iloc[df['High'][0:6].idxmax()] = df['High'][0:6].max() + 10
        df['Lowv1'].iloc[df['Low'][0:6].idxmin()] = df['Low'][0:6].min() - 10

        df['Highv1'].fillna(method='ffill', inplace=True)
        df['Lowv1'].fillna(method='ffill', inplace=True)
        print(df['High'][0:6].max() - df['Low'][0:6].min(), 'high low')

        global buyid
        buyid = None
        global sellid
        sellid = None

        global buyflag
        buyflag = None
        global sellflag
        sellflag = None
        global putli
        putli = []
        global callli
        callli = []

        for i in range(len(df)):
            if df["Highv1"][i] < df['Close'][i] and df['Close'][i - 1] < df['Close'][i]:
                df['buy'].iloc[i] = df['Open'].iloc[i]
                buyid = df.loc[(df['buy'] == df['buy'][i])].index[0]
                print('buyid', buyid)
                buyflag = True
                callli.append(1)
                dts = [dt.strftime('%Y-%m-%dT%H:%M:00') for dt in
                       datetime_range(datetime(2021, 11, cday, 9), datetime.now(),
                                      timedelta(minutes=5))]

                break
        for i in range(len(df)):
            if df["Lowv1"][i] > df['Close'][i] and df['Close'][i - 1] > df['Close'][i]:
                df['sell'].iloc[i] = df['Open'].iloc[i]
                sellid = df.loc[(df['sell'] == df['sell'][i])].index[0]
                print('sellid:', sellid)
                sellflag = True
                putli.append(0)
                dts = [dt.strftime('%Y-%m-%dT%H:%M:00') for dt in
                       datetime_range(datetime(2021, 11, cday, 9), datetime.now(),
                                      timedelta(minutes=5))]

                break

        print('first---list ', f'put: {putli}, call: {callli}')
        # Second StopLoss Condition
        '''
                df['Put'] = np.nan
        df['Put'].iloc[i] = df['Open'][i]
        '''

        for i in range(len(df)):
            try:
                if buyid is not None and i >= buyid:
                    if df['Close'][i - 1] < df['Close'][i]:
                        df['stop_loss_sl2'].iloc[i] = df["Open"][i] - 25

                if sellid is not None and i >= sellid:
                    if df['Close'][i - 1] > df['Close'][i]:
                        df['stop_loss_sl2_sell'].iloc[i] = df["Open"][i] + 25

            except Exception as e:
                print('buy Exception:', e)

        df['stop_loss_sl2'].fillna(method='ffill', inplace=True)
        df['stop_loss_sl2_sell'].fillna(method='ffill', inplace=True)

        # df.to_csv(f'{day}NIftyBank.csv')
        return df
    return df


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


def backtest(date):
    df = buy_sell(date)

    # -----------------------------------------------------------------------------------------------#
    # ----------------------------------------- BUY -------------------------------------------------#
    # -----------------------------------------------------------------------------------------------#

    if df is not None:
        putlist = []
        calllist = []
        flags = None
        flagsputid = None
        flagscallid = None
        df['Put'] = np.nan
        df['Put-stoploss'] = np.nan

        df['call'] = np.nan
        df['call-stoploss'] = np.nan


        putid = None
        callid = None
        # Second StopLoss buy
        '''
        stop-loss-sl2
        stop-loss-sl2-sell
        '''
        # for i in range(len(df)):
        #         if df['stop_loss_sl2'][i] > df['Open'][i] or df['stop_loss_sl2_sell'][i] < df['Open'][i]:
        #             slid =1
        df.reset_index(inplace=True)
        df['3:15'] = np.nan
        df['points-put'] = np.nan
        df['points-call'] = np.nan
        df['points'] = np.nan
        df['buy-points-sl2-hit'] = np.nan
        putcalllist = []
        for i in range(len(df)):

            try:
                if df['stop_loss_sl2'][i] > df['Open'][i] or df['stop_loss_sl2_sell'][i] < df['Open'][i]:
                    slid = [i]

                    if df['Open'][i] - df['Close'][slid[0] + 1] >= 25:

                        df['Put'].iloc[i + 1] = df['Open'][i + 1]
                        dts = [dt.strftime('%Y-%m-%dT%H:%M:00') for dt in
                               datetime_range(datetime(2021, 11, cday, 9), datetime.now(),
                                              timedelta(minutes=5))]



                        # client.place_order(test_order1)

                        putid = i + 1
                        putcalllist.append(0)

                        if sellid is not None and putid < sellid:
                            df['sell'][i:] = np.nan

                        for i1 in range(len(df)):
                            try:
                                if i1 >= putid:
                                    if df['Close'][i1 - 1] > df['Close'][i1]:
                                        df['stop_loss_sl2_sell'].iloc[i1] = df['Open'][i1] + 25
                                        df['stop_loss_sl2_sell'].fillna(limit=1, method='ffill', inplace=True)
                                        df['stop_loss_sl2'][i1:] = np.nan


                                        # client.mod_bo_order(test_order)

                            except Exception as e:
                                print(e)

                    if df['Close'][slid[0] + 1] - df['Open'][i] >= 25:

                        df['call'].iloc[i + 1] = df['Open'][i + 1]

                        # if df['Datetime'][i] == datetime.datetime.strftime( e, f"%Y-%m-%dT%H:{str(sda).split(':')[-2]}:00"):
                        dts = [dt.strftime('%Y-%m-%dT%H:%M:00') for dt in
                               datetime_range(datetime(2021, 11, cday, 9), datetime.now(),
                                              timedelta(minutes=5))]



                        # client.place_order(test_order1)

                        callid = i + 1
                        putcalllist.append(1)
                        print('buy-callid', callid, i)

                        if buyid is not None and callid < buyid:
                            df['buy'][i:] = np.nan

                        for i2 in range(len(df)):
                            try:
                                if i2 >= callid:
                                    if df['Close'][i2 - 1] < df['Close'][i2]:
                                        df['stop_loss_sl2'].iloc[i2] = df["Open"][i2] - 25
                                        df['stop_loss_sl2'].fillna(limit=1, method='ffill', inplace=True)
                                        df['stop_loss_sl2_sell'][i2:] = np.nan


                            except Exception as e:
                                print(e)
                else:
                    pass

            except Exception as e:
                print(e)
        # df.to_csv(
        #     f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\{mon} {yr1} Bank Nifty\\{date}-{mon}-{yr1} Nifty Bank.csv')
        df.to_csv('put-call-BankNifty1.csv')
        # plot2(df)
        return df


def plot2(frame):
    frame = frame
    fig = plt.figure(figsize=(8, 4))
    ax1 = fig.add_subplot(1, 1, 1)
    ax1.clear()

    # frame.reset_index(inplace=True)
    # print(df)
    frame = frame.set_index(pd.DatetimeIndex(frame['Datetime']))

    apd = [
        # mpf.make_addplot(frame['Close'], ax=ax1),
        mpf.make_addplot(frame['Lowv1'], ax=ax1),
        mpf.make_addplot(frame['Highv1'], ax=ax1),
        mpf.make_addplot(frame['Openv1'], ax=ax1),
        mpf.make_addplot(frame['stop_loss_sl2'], ax=ax1),
        mpf.make_addplot(frame['stop_loss_sl2_sell'], ax=ax1),
        # mpf.make_addplot(frame['call-stoploss'], ax=ax1),
        # mpf.make_addplot(frame['Put-stoploss'], ax=ax1),
        mpf.make_addplot(frame['sell'], ax=ax1, type='scatter', markersize=280, marker='v'),
        mpf.make_addplot(frame['Put'], ax=ax1, type='scatter', markersize=280, marker='v'),
        mpf.make_addplot(frame['call'], ax=ax1, type='scatter', markersize=280, marker='^'),
        mpf.make_addplot(frame['buy'], ax=ax1, type='scatter', markersize=280, marker='^'),
    ]
    try:
        os.mkdir(
            f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\Plot Images {mon} {yr1} Bank Nifty')
    except Exception as e:
        pass

    mpf.plot(frame, ax=ax1, addplot=apd, type='candle', style='yahoo', savefig='tsave100.jpg')
    # plt.savefig(
    #     f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\Plot Images {mon} {yr1} Bank Nifty\\Plot Image {next(n_month_iters)} {mon} {yr1} Bank Nifty')
    # plt.savefig(
    #         f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\Plot Images {mon} {yr1} Bank Nifty\\Plot Image {cday} {mon} {yr1} Bank Nifty')

    mpf.show()


'''

io = 1
while True:
    if io>13:
        break
    list11 = []

    yr1 = 2021
    mon = io
    os.mkdir(f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\{mon} {yr1} Bank Nifty')

    for i in range(1, 13):
        a = monthrange(yr1, i)
        list11.append(f'{a[1]}')

    n_month = list(range(1, int(list11[mon-1])+1))
    n_month_iters = iter(n_month)

    x = map(backtest,n_month)

    print(list(x))

    backtest_compile()
    io+=1
 '''

# For animation
fig = plt.figure(figsize=(8, 4))
ax1 = fig.add_subplot(1, 1, 1)


def animate(ival):
    df = backtest(cday)
    # df = pd.read_csv('put-call-BankNifty1.csv')

    frame = df.set_index(pd.DatetimeIndex(df['Datetime']))

    # frame = frame.iloc[0:(20 + ival)]
    ax1.clear()
    # print(df)

    apd = [
        # mpf.make_addplot(frame['Close'], ax=ax1),
        mpf.make_addplot(frame['Lowv1'], ax=ax1),
        mpf.make_addplot(frame['Highv1'], ax=ax1),
        mpf.make_addplot(frame['Openv1'], ax=ax1),
        mpf.make_addplot(frame['stop_loss_sl2'], ax=ax1),
        mpf.make_addplot(frame['stop_loss_sl2_sell'], ax=ax1),
        # mpf.make_addplot(frame['call-stoploss'], ax=ax1),
        # mpf.make_addplot(frame['Put-stoploss'], ax=ax1),
        mpf.make_addplot(frame['sell'], ax=ax1, type='scatter', markersize=280, marker='v'),
        mpf.make_addplot(frame['Put'], ax=ax1, type='scatter', markersize=280, marker='v'),
        mpf.make_addplot(frame['call'], ax=ax1, type='scatter', markersize=280, marker='^'),
        mpf.make_addplot(frame['buy'], ax=ax1, type='scatter', markersize=280, marker='^'),
    ]
    # mpf.plot(frame, ax=ax1, addplot=apd)
    mpf.plot(frame, ax=ax1, addplot=apd, type='candle', style='yahoo')
    try:
        os.mkdir(
            f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\Plot Images {mon} {yr1} Bank Nifty')
    except Exception as e:
        pass
    mi = 1
    # plt.savefig(
    #     f'C:\\Users\\Durgesh\\PycharmProjects\\stockdata_py\\low-high-backtest\\Plot Images {mon} {yr1} Bank Nifty\\Plot Image {mon} {yr1}_{mi} Bank Nifty')
    # mi += 1
    font = {'family': 'serif',
            'color': 'darkred',
            'weight': 'normal',
            'size': 20,
            }
    # plt.title(f"Bank Nifty {cday}/{mon}/{yr1}", fontdict=font, y=1.07)

    # mpf.plot(frame, ax=ax1, addplot=apd, type='line')
    # mpf.plot(frame, ax=ax1, type='candle',style='yahoo')


yr1 = 2021
mon = 11
# cday = int(input('cday: '))
cday = 12


if input('input: ') == 'start':
    # while True:
    #     backtest(cday)
    #     second = datetime.now().second
    #     # time.sleep(300 - second)
    #     time.sleep(60 - second)
    while True:
        ani = animation.FuncAnimation(fig, animate, interval=60000)
        # ani = animation.FuncAnimation(fig, animate, interval=1000)
        mpf.show()



