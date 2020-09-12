from math import floor, ceil


def strategy_1(df, df_y, commission):

    commission /= 10000
    # hj = Sheet2.Cells(35, 1) + 2

    df = color(df)
    c1 = df_y['1.Profit Dec.']
    c2 = df_y['1.Stop Dec.']
    c3 = df_y['1.Profit Inc.']
    c4 = df_y['1.Stop Inc.']

    net_kar1 = 0
    net_kar2 = 0
    kar = 0
    isl_say = 0
    k = 0
    # te = 0

    for i in range(len(df)-1):

        print(i)

        if (i == 0) or (df.Date[i] != df.Date[i + 1] and (k == 1 or k == 2)):
            k = 0
            # te = 1
            a1 = df.Close[i]
            df.Position[i] = f'{str(a1)} / buy'

            if df.Color[i+1] == 'K':
                df.Code[i] = 'K-' + str(k)
            else:
                df.Code[i] = 'S-' + str(k)

            df.Profit[i] = 0
            df['Net Profit'][i] = 0

            b1, b2, b1s, b2s = selling_price(a1, c1, c2, c3, c4)

        elif k == 0:

            df.Position[i], df.Profit[i], k = results_transaction(df,b1,b2,b1s,b2s,i,a1)

            if k == 1 or k == 2:
                if df.Color[i] == 'K':
                    df.Code[i] = 'K-' + str(k)                      # yukaridakinden farkli olarak i oldu cunku son islem saatinde yaparsa yanlis renk vermesin
                    net_kar1 += (df.Profit[i] - 200 * commission)
                    isl_say += 1
                    df['Net Profit'][i] = (df.Profit[i] - 200 * commission)
                else:
                    df.Code[i] = 'S-' + str(k)
                    net_kar2 += (df.Profit[i] - 200 * commission)
                    isl_say += 1
                    df['Net Profit'][i] = (df.Profit[i] - 200 * commission)

        elif (k == 1 or k == 2) and df.Date[i] == df.Date[i+1]:

            df.Position[i] = '---'
            df.Code[i] = '---'
            df.Profit[i] = 0
            df['Net Profit'][i] = 0

        kar += df.Profit[i]

    kar = rounder(kar, True)
    net_kar1 = rounder(net_kar1, True)
    net_kar2 = rounder(net_kar2, True)
    net_kar = net_kar1+net_kar2
    pro_trans = rounder(net_kar/isl_say, True)


    return kar, net_kar, net_kar1, net_kar2, isl_say, pro_trans, df


def selling_price(a1, c1, c2, c3, c4):

    b2 = rounder(a1 * (1 + c1), True)
    b1 = rounder(a1 * (1 + c2), False)

    b2s = rounder(a1 * (1 + c3), True)
    b1s = rounder(a1 * (1 + c4), False)

    return b1,b2,b1s,b2s

def results_transaction(df,b1,b2,b1s,b2s,i,a1):

    if df.Low[i] > b1 and df.High[i] < b2:
        statement = '+++'
        cell_profit = 0
        k = 0
    elif df.Date[i] != df.Date[i-1] and df.Open[i] <= b1:
        statement = str(df.Open[i])+' - ekstra sell'
        cell_profit = 100*(df.Open[i]-a1)/a1
        k = 1
    elif df.Date[i] != df.Date[i-1] and df.Open[i] >= b2:
        statement = str(df.Open[i])+' - ekstra sell'
        cell_profit = 100*(df.Open[i]-a1)/a1
        k = 2
    elif df.Low[i] <= b1:
        statement = str(b1) + ' - 1.stop'
        cell_profit = 100 * (b1 - a1) / a1
        k = 1
    elif df.High[i] >= b2:
        statement = str(b2) + ' - 1.profit'
        cell_profit = 100 * (b2 - a1) / a1
        k = 2
    return statement, cell_profit,k



def rounder(num, up=True):
    digits = 2
    mul = 10**digits
    if up:
        return ceil(num * mul)/mul
    else:
        return floor(num * mul)/mul

def color(df):

    for i in range(len(df)-1):
        if df.Date[i] != df.Date[i+1] and df.Close[i] <= df.MA[i]:
            df.Color[i+1]='K'
        elif (df.Date[i] != df.Date[i+1]) and (df.Close[i] > df.MA[i]):
            df.Color[i+1]='S'
        elif (df.Date[i] == df.Date[i+1]) and (df.Color[i] == 'K'):
            df.Color[i + 1] = 'K'
        elif (df.Date[i] == df.Date[i+1]) and (df.Color[i] == 'S'):
            df.Color[i + 1] = 'S'
    return df

# def simulation():
