import requests
import pandas as pd
import json
import xlwings as xw
import time
import datetime
import openpyxl
import matplotlib.pyplot as plt
from pprint import pprint
from threading import Thread

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
import pandas as pd
import json
from pyqtgraph import TextItem
from pyqtgraph.exporters import ImageExporter
from pyqtgraph import mkPen
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QThread, pyqtSignal

tdate = datetime.datetime.now().date()


try:
    with open(f'data/{tdate}_access_code.json', 'r') as file_read:
        access = json.load(file_read)
except:
    api_key = '061ca76c-53f6-4d77-8f1a-01a3e34b3a01'
    api_secret = 'wurhexh7lo'
    uri = 'https://www.google.com/'
    url1 = f'https://api.upstox.com/v2/login/authorization/dialog?response_type=code&client_id={api_key}&redirect_uri={uri}'
    print(url1)

    code = input('Enter the Code')
    url = 'https://api.upstox.com/v2/login/authorization/token'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    data = {
        'code': code,
        'client_id': api_key,
        'client_secret': api_secret,
        'redirect_uri': uri,
        'grant_type': 'authorization_code',
    }

    response = requests.post(url, headers=headers, data=data)
    access = response.json()['access_token']
    print(response.status_code)
    print(response.json())

    with open(f'data/{tdate}_access_code.json', 'w') as file_write:
        json.dump(access, file_write)

#############################################################################

def instrument():
    inst_url = 'https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz'
    instrument = pd.read_csv(inst_url)
    instrument.to_csv('instrument.csv')

yn = int(input('Do you Want to Update Instrument : 0 / 1 : '))

if yn==1:
    instrument()
    print("Instrument Data Updated Successfully")


df = pd.read_csv('instrument.csv', index_col=0)

df_niftyoptions = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTIDX') & (df['name'] == 'NIFTY')]
expiry_list_nifty = df_niftyoptions['expiry'].unique().tolist()
expiry_list_nifty.sort()

df_bnf = df[(df['exchange'] == 'NSE_FO') & (df['instrument_type'] == 'OPTIDX') & (df['name'] == 'BANKNIFTY')]
expiry_list_bnf = df_bnf['expiry'].unique().tolist()
expiry_list_bnf.sort()

df_sensex = df[(df['exchange'] == 'BSE_FO') & (df['instrument_type'] == 'OPTIDX') & (df['name'] == 'SENSEX')]
expiry_list_sensex = df_sensex['expiry'].unique().tolist()
expiry_list_sensex.sort()

wb = xw.Book('Analysis.xlsm')
summary = wb.sheets('summary')
nifty_0 = wb.sheets('nifty_0')
nifty_1 = wb.sheets('nifty_1')
nifty_3 = wb.sheets('nifty_3')
bnf_0 = wb.sheets('bnf_0')
sensex_0 = wb.sheets('sensex_0')

instrument_key_nifty = 'NSE_INDEX|Nifty 50'
instrument_key_bnf = 'NSE_INDEX|Nifty Bank'
instrument_key_sensex = 'BSE_INDEX|SENSEX'

structure_initial = {}
structure_current = {}
past_data={}

a=b=c=d=e=f=1
initialize=1

t_date = datetime.datetime.now().date()

# Function to convert time strings to timestamps
def format_time_ticks(values, scale, spacing):
    """Convert timestamp values to formatted time strings"""
    result = []
    for val in values:
        try:
            if val > 0:  # Make sure it's a positive timestamp
                dt = datetime.datetime.fromtimestamp(val)
                result.append(dt.strftime('%H:%M:%S'))
            else:
                result.append('')
        except (ValueError, OSError, OverflowError) as e:
            # print(f"Error with timestamp {val}: {e}")
            result.append('')
    return result

# Function to format timestamps as time strings for the axis
def time_string_to_timestamp(time_str):
    """Convert a time string to Unix timestamp"""
    try:
        # Assuming time_str format is something like "09:30:15"
        today = datetime.datetime.now().date()
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S').time()
        dt = datetime.datetime.combine(today, time_obj)
        ts = time.mktime(dt.timetuple())
        
        # Debug print
        # print(f"Converted '{time_str}' to timestamp {ts}")
        
        return ts
    except (ValueError, TypeError) as e:
        # print(f"Error converting time: {time_str}, Error: {e}")
        # Instead of returning 0, which could be an invalid timestamp
        # Return the current time's timestamp as a fallback
        return time.time()


def check_data(initial_data, current_data):

    global expiry_name_0, expiry_name_1, expiry_name_2, expiry_name_3, expiry_name_4
    
    initial_df = pd.DataFrame(initial_data).reset_index(drop=True)
    current_df = pd.DataFrame(current_data).reset_index(drop=True)

    df_concat = pd.concat([initial_df, current_df], axis=1)
    re_order = df_concat.columns.to_list()
    column_index = [0,5,1,6,2,7,3,8,4,9]
    column_index_order = [re_order[i] for i in column_index]
    df_concat = df_concat[column_index_order]
    df_concat.index = ['CE Side LTP', 'PE Side LTP', 'CE Side Theta', 'PE Side Theta', 'CE Side Vega', 'PE Side Vega', 'CE Side IV', 'PE Side IV', 'CE Side OI', 'PE Side OI', 'CE ATM LTP', 'PE ATM LTP', 'ATM Straddle', 'Spot Price', 'India VIX']

    df_concat.columns = ['1_Initial', '1_Current', '2_Initial', '2_Current', '3_Initial', '3_Current', '4_Initial', '4_Current', '5_Initial', '5_Current']

    den_zero = [(df_concat.iloc[8,1] - df_concat.iloc[8,0]), (df_concat.iloc[9,1] - df_concat.iloc[9,0]), (df_concat.iloc[8,3] - df_concat.iloc[8,2]), (df_concat.iloc[9,3] - df_concat.iloc[9,2]), (df_concat.iloc[8,5] - df_concat.iloc[8,4]), (df_concat.iloc[9,5] - df_concat.iloc[9,4])]

    if all(val != 0 and pd.notna(val) for val in den_zero): # pd.notna(val) is True if val is not NaN &&&&& False is val is NaN
        ab = round((df_concat.iloc[8,1] - df_concat.iloc[8,0]) / (df_concat.iloc[9,1] - df_concat.iloc[9,0]),2)
        ba = round((df_concat.iloc[9,1] - df_concat.iloc[9,0]) / (df_concat.iloc[8,1] - df_concat.iloc[8,0]),2)

        bc = round((df_concat.iloc[8,3] - df_concat.iloc[8,2]) / (df_concat.iloc[9,3] - df_concat.iloc[9,2]),2)
        cb = round((df_concat.iloc[9,3] - df_concat.iloc[9,2]) / (df_concat.iloc[8,3] - df_concat.iloc[8,2]),2)

        cd = round((df_concat.iloc[8,5] - df_concat.iloc[8,4]) / (df_concat.iloc[9,5] - df_concat.iloc[9,4]),2)
        dc = round((df_concat.iloc[9,5] - df_concat.iloc[9,4]) / (df_concat.iloc[8,5] - df_concat.iloc[8,4]),2)

        de = round((df_concat.iloc[8,7] - df_concat.iloc[8,6]) / (df_concat.iloc[9,7] - df_concat.iloc[9,6]),2)
        ed = round((df_concat.iloc[9,7] - df_concat.iloc[9,6]) / (df_concat.iloc[8,7] - df_concat.iloc[8,6]),2)

        ef = round((df_concat.iloc[8,9] - df_concat.iloc[8,8]) / (df_concat.iloc[9,9] - df_concat.iloc[9,8]),2)
        fe = round((df_concat.iloc[9,9] - df_concat.iloc[9,8]) / (df_concat.iloc[8,9] - df_concat.iloc[8,8]),2)

    else:
        ab=ba=bc=cb=cd=dc=de=ed=ef=fe=None

    df_concat['1_Diff'] = [df_concat.iloc[0,1] - df_concat.iloc[0,0], 
                           df_concat.iloc[1,1] - df_concat.iloc[1,0], 
                           df_concat.iloc[2,0] - df_concat.iloc[2,1], 
                           df_concat.iloc[3,0] - df_concat.iloc[3,1], 
                           df_concat.iloc[4,1] - df_concat.iloc[4,0], 
                           df_concat.iloc[5,1] - df_concat.iloc[5,0], 
                           df_concat.iloc[6,1] - df_concat.iloc[6,0], 
                           df_concat.iloc[7,1] - df_concat.iloc[7,0], 
                           f'{df_concat.iloc[8,1] - df_concat.iloc[8,0]}  ({ab})', 
                           f'{df_concat.iloc[9,1] - df_concat.iloc[9,0]}  ({ba})',
                           df_concat.iloc[10,1] - df_concat.iloc[10,0], 
                           df_concat.iloc[11,1] - df_concat.iloc[11,0],
                           df_concat.iloc[12,1] - df_concat.iloc[12,0], 
                           df_concat.iloc[13,1] - df_concat.iloc[13,0],
                           df_concat.iloc[14,1] - df_concat.iloc[14,0]]


    df_concat['2_Diff'] = [df_concat.iloc[0,3] - df_concat.iloc[0,2], 
                           df_concat.iloc[1,3] - df_concat.iloc[1,2], 
                           df_concat.iloc[2,2] - df_concat.iloc[2,3], 
                           df_concat.iloc[3,2] - df_concat.iloc[3,3], 
                           df_concat.iloc[4,3] - df_concat.iloc[4,2], 
                           df_concat.iloc[5,3] - df_concat.iloc[5,2], 
                           df_concat.iloc[6,3] - df_concat.iloc[6,2], 
                           df_concat.iloc[7,3] - df_concat.iloc[7,2], 
                           f'{df_concat.iloc[8,3] - df_concat.iloc[8,2]}  ({bc})',
                           f'{df_concat.iloc[9,3] - df_concat.iloc[9,2]}  ({cb})',
                           df_concat.iloc[10,3] - df_concat.iloc[10,2], 
                           df_concat.iloc[11,3] - df_concat.iloc[11,2],
                           df_concat.iloc[12,3] - df_concat.iloc[12,2], 
                           df_concat.iloc[13,3] - df_concat.iloc[13,2],
                           df_concat.iloc[14,3] - df_concat.iloc[14,2]]

    df_concat['3_Diff'] = [df_concat.iloc[0,5] - df_concat.iloc[0,4], 
                           df_concat.iloc[1,5] - df_concat.iloc[1,4], 
                           df_concat.iloc[2,4] - df_concat.iloc[2,5], 
                           df_concat.iloc[3,4] - df_concat.iloc[3,5], 
                           df_concat.iloc[4,5] - df_concat.iloc[4,4], 
                           df_concat.iloc[5,5] - df_concat.iloc[5,4], 
                           df_concat.iloc[6,5] - df_concat.iloc[6,4], 
                           df_concat.iloc[7,5] - df_concat.iloc[7,4], 
                           f'{df_concat.iloc[8,5] - df_concat.iloc[8,4]}  ({cd})',
                           f'{df_concat.iloc[9,5] - df_concat.iloc[9,4]}  ({dc})',
                           df_concat.iloc[10,5] - df_concat.iloc[10,4], 
                           df_concat.iloc[11,5] - df_concat.iloc[11,4],
                           df_concat.iloc[12,5] - df_concat.iloc[12,4], 
                           df_concat.iloc[13,5] - df_concat.iloc[13,4],
                           df_concat.iloc[14,5] - df_concat.iloc[14,4]]

    df_concat['4_Diff'] = [df_concat.iloc[0,7] - df_concat.iloc[0,6], 
                           df_concat.iloc[1,7] - df_concat.iloc[1,6], 
                           df_concat.iloc[2,6] - df_concat.iloc[2,7], 
                           df_concat.iloc[3,6] - df_concat.iloc[3,7], 
                           df_concat.iloc[4,7] - df_concat.iloc[4,6], 
                           df_concat.iloc[5,7] - df_concat.iloc[5,6], 
                           df_concat.iloc[6,7] - df_concat.iloc[6,6], 
                           df_concat.iloc[7,7] - df_concat.iloc[7,6], 
                           f'{df_concat.iloc[8,7] - df_concat.iloc[8,6]}  ({de})',
                           f'{df_concat.iloc[9,7] - df_concat.iloc[9,6]}  ({ed})',
                           df_concat.iloc[10,7] - df_concat.iloc[10,6], 
                           df_concat.iloc[11,7] - df_concat.iloc[11,6],
                           df_concat.iloc[12,7] - df_concat.iloc[12,6], 
                           df_concat.iloc[13,7] - df_concat.iloc[13,6],
                           df_concat.iloc[14,7] - df_concat.iloc[14,6]]

    df_concat['5_Diff'] = [df_concat.iloc[0,9] - df_concat.iloc[0,8], 
                           df_concat.iloc[1,9] - df_concat.iloc[1,8], 
                           df_concat.iloc[2,8] - df_concat.iloc[2,9], 
                           df_concat.iloc[3,8] - df_concat.iloc[3,9], 
                           df_concat.iloc[4,9] - df_concat.iloc[4,8], 
                           df_concat.iloc[5,9] - df_concat.iloc[5,8], 
                           df_concat.iloc[6,9] - df_concat.iloc[6,8], 
                           df_concat.iloc[7,9] - df_concat.iloc[7,8], 
                           f'{df_concat.iloc[8,9] - df_concat.iloc[8,8]}  ({ef})',
                           f'{df_concat.iloc[9,9] - df_concat.iloc[9,8]}  ({fe})',
                           df_concat.iloc[10,9] - df_concat.iloc[10,8], 
                           df_concat.iloc[11,9] - df_concat.iloc[11,8],
                           df_concat.iloc[12,9] - df_concat.iloc[12,8], 
                           df_concat.iloc[13,9] - df_concat.iloc[13,8],
                           df_concat.iloc[14,9] - df_concat.iloc[14,8]]


    df_concat = df_concat[['1_Initial', '1_Current', '1_Diff', '2_Initial', '2_Current', '2_Diff', '3_Initial', '3_Current', '3_Diff', '4_Initial', '4_Current', '4_Diff', '5_Initial', '5_Current', '5_Diff']]
    df_concat = df_concat.rename(columns={'1_Diff':expiry_name_0, '2_Diff':expiry_name_1, '3_Diff':expiry_name_2, '4_Diff':expiry_name_3, '5_Diff':expiry_name_4})
    return df_concat

################################################################################################

counter = 1
last_triggered_minute = None

def chain(instrument_key,expiry_date,counter):

        global structure_initial, structure_current, past_data, initialize
        
        url1 = 'https://api.upstox.com/v2/option/chain'
        url2 = 'https://api.upstox.com/v2/market-quote/ltp?instrument_key=NSE_INDEX|India VIX'

        params = {
                'instrument_key': instrument_key,
                'expiry_date': expiry_date
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {access}'
        }

        response = requests.get(url1, params=params, headers=headers)
        time.sleep(1)

        response2 = requests.get(url2, headers=headers)
        response2 = response2.json()
        india_vix = response2['data']['NSE_INDEX:India VIX']['last_price']

        time_stamp = datetime.datetime.now().strftime("%H:%M:%S")
        option = response.json()
        option_df = pd.json_normalize(option['data'])

        option_df = option_df[['expiry', 'pcr', 'strike_price', 'underlying_spot_price', 'call_options.instrument_key', 'call_options.market_data.ltp', 'call_options.market_data.oi', 'call_options.option_greeks.vega', 'call_options.option_greeks.theta', 'call_options.option_greeks.gamma', 'call_options.option_greeks.delta', 'call_options.option_greeks.iv', 'put_options.instrument_key', 'put_options.market_data.ltp', 'put_options.market_data.oi', 'put_options.option_greeks.vega', 'put_options.option_greeks.theta', 'put_options.option_greeks.gamma', 'put_options.option_greeks.delta', 'put_options.option_greeks.iv']]
        option_df = option_df.rename(columns={'call_options.instrument_key' : 'CE_instrument_key', 'call_options.market_data.ltp' : 'CE_ltp', 'call_options.market_data.oi' : 'CE_oi', 'call_options.option_greeks.vega' : 'CE_vega', 'call_options.option_greeks.theta' : 'CE_theta', 'call_options.option_greeks.gamma' : 'CE_gamma', 'call_options.option_greeks.delta' : 'CE_delta', 'call_options.option_greeks.iv' : 'CE_iv', 'put_options.instrument_key' : 'PE_instrument_key', 'put_options.market_data.ltp' : 'PE_ltp', 'put_options.market_data.oi' : 'PE_oi', 'put_options.option_greeks.vega' : 'PE_vega', 'put_options.option_greeks.theta' : 'PE_theta', 'put_options.option_greeks.gamma' : 'PE_gamma', 'put_options.option_greeks.delta' : 'PE_delta', 'put_options.option_greeks.iv' : 'PE_iv', 'underlying_spot_price' : 'spot_price'})
        option_df = option_df[['expiry','pcr','CE_instrument_key','CE_delta','CE_oi','CE_iv','CE_vega','CE_theta','CE_ltp','strike_price','PE_ltp','PE_theta','PE_vega','PE_iv','PE_oi','PE_delta','PE_instrument_key','spot_price']]

        option_df['diff'] = abs(option_df['spot_price'] - option_df['strike_price'])
        ce = option_df.loc[option_df['diff'].idxmin(),'CE_ltp']
        strike = option_df.loc[option_df['diff'].idxmin(),'strike_price']
        pe = option_df.loc[option_df['diff'].idxmin(),'PE_ltp']

        fut_spot_price = ce-pe+strike

        option_df['spot_price'] = fut_spot_price
        option_df['diff'] = abs(option_df['spot_price'] - option_df['strike_price'])
        option_df['prem_diff'] = option_df['CE_ltp'] - option_df['PE_ltp']
        option_df['CE/PE'] = round((option_df['CE_ltp'] / option_df['PE_ltp']),2)
        atm_strike = option_df.loc[option_df['diff'].idxmin(), 'strike_price']

        ce_atm_ltp = option_df[option_df['strike_price'] == atm_strike].iloc[0]['CE_ltp']
        pe_atm_ltp = option_df[option_df['strike_price'] == atm_strike].iloc[0]['PE_ltp']

        x = option_df['strike_price'].diff().mode()[0]
        upper_limit = atm_strike + 15*x
        lower_limit = atm_strike - 15*x
        option_df = option_df[(option_df['strike_price'] >= lower_limit) & (option_df['strike_price'] <= upper_limit)]

        ce_df = option_df[option_df['strike_price'] >= atm_strike]
        pe_df = option_df[option_df['strike_price'] <= atm_strike]

        ce_ltp_sum = round(ce_df['CE_ltp'].sum(),2)
        pe_ltp_sum = round(pe_df['PE_ltp'].sum(),2)
        ce_theta_sum = round(ce_df['CE_theta'].sum(),2)
        pe_theta_sum = round(pe_df['PE_theta'].sum(),2)
        ce_vega_sum = round(ce_df['CE_vega'].sum(),2)
        pe_vega_sum = round(pe_df['PE_vega'].sum(),2)
        ce_iv_sum = round(ce_df['CE_iv'].sum(),2)
        pe_iv_sum = round(pe_df['PE_iv'].sum(),2)
        ce_oi_sum = round(ce_df['CE_oi'].sum(),2)
        pe_oi_sum = round(pe_df['PE_oi'].sum(),2)

        try:
            with open(f'data/{tdate}_initial_values.json', 'r') as file_read:
                structure_initial = json.load(file_read)
        except:
            if counter<=3:

                structure_initial[f'{instrument_key}_{expiry_date}_initial'] = {'ce_ltp_init' : ce_ltp_sum,
                                                                                'pe_ltp_init' : pe_ltp_sum,
                                                                                'ce_theta_init' : ce_theta_sum,
                                                                                'pe_theta_init' : pe_theta_sum,
                                                                                'ce_vega_init' : ce_vega_sum,
                                                                                'pe_vega_init' : pe_vega_sum,
                                                                                'ce_iv_init' : ce_iv_sum,
                                                                                'pe_iv_init' : pe_iv_sum,
                                                                                'ce_oi_init' : ce_oi_sum,
                                                                                'pe_oi_init' : pe_oi_sum,
                                                                                'ce_atm_ltp' : ce_atm_ltp,
                                                                                'pe_atm_ltp' : pe_atm_ltp,
                                                                                'atm_straddle' : (ce_atm_ltp + pe_atm_ltp),
                                                                                'spot price' : fut_spot_price,
                                                                                'india vix' : india_vix
                                                                                }

        structure_current[f'{instrument_key}_{expiry_date}_Current'] = {'ce_ltp_current' : ce_ltp_sum,
                                                                        'pe_ltp_current' : pe_ltp_sum,
                                                                        'ce_theta_current' : ce_theta_sum,
                                                                        'pe_theta_current' : pe_theta_sum,
                                                                        'ce_vega_current' : ce_vega_sum,
                                                                        'pe_vega_current' : pe_vega_sum,
                                                                        'ce_iv_current' : ce_iv_sum,
                                                                        'pe_iv_current' : pe_iv_sum,
                                                                        'ce_oi_current' : ce_oi_sum,
                                                                        'pe_oi_current' : pe_oi_sum,
                                                                        'ce_atm_ltp' : ce_atm_ltp,
                                                                        'pe_atm_ltp' : pe_atm_ltp,
                                                                        'atm_straddle' : (ce_atm_ltp + pe_atm_ltp),
                                                                        'spot price' : fut_spot_price,
                                                                        'india vix' : india_vix
                                                                        }

        ce_ltp_diff = round((ce_ltp_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_ltp_init']),2)
        pe_ltp_diff = round((pe_ltp_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_ltp_init']),2)
        ce_theta_diff = round((structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_theta_init'] - ce_theta_sum),2)
        pe_theta_diff = round((structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_theta_init'] - pe_theta_sum),2)
        ce_vega_diff = round((ce_vega_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_vega_init']),2)
        pe_vega_diff = round((pe_vega_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_vega_init']),2)
        ce_iv_diff = round((ce_iv_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_iv_init']),2)
        pe_iv_diff = round((pe_iv_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_iv_init']),2)
        ce_oi_diff = round((ce_oi_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_oi_init']),2)
        pe_oi_diff = round((pe_oi_sum - structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_oi_init']),2)
        ce_atm_diff = round((ce_atm_ltp - structure_initial[f'{instrument_key}_{expiry_date}_initial']['ce_atm_ltp']),2)
        pe_atm_diff = round((pe_atm_ltp - structure_initial[f'{instrument_key}_{expiry_date}_initial']['pe_atm_ltp']),2)
        atm_straddle_diff = round(((ce_atm_ltp + pe_atm_ltp) - structure_initial[f'{instrument_key}_{expiry_date}_initial']['atm_straddle']),2)
        spot_price_diff = round((fut_spot_price - structure_initial[f'{instrument_key}_{expiry_date}_initial']['spot price']),2)
        india_vix_diff = round((india_vix - structure_initial[f'{instrument_key}_{expiry_date}_initial']['india vix']),2)

        main = {'CE Side LTP':ce_ltp_diff, 'PE Side LTP':pe_ltp_diff, 'CE Side Theta':ce_theta_diff, 'PE Side Theta':pe_theta_diff, 'CE Side Vega':ce_vega_diff, 'PE Side Vega':pe_vega_diff, 'CE Side IV':ce_iv_diff, 'PE Side IV':pe_iv_diff, 'CE Side OI':ce_oi_diff, 'PE Side OI':pe_oi_diff, 'CE ATM LTP':ce_atm_diff, 'PE ATM LTP':pe_atm_diff, 'Atm Straddle':atm_straddle_diff, 'Spot Price': spot_price_diff, 'India Vix': india_vix_diff, 'Time': time_stamp}

        expiry_name = option_df.iloc[0,0]

        main_df = pd.DataFrame([main], index=[expiry_name]).T

        try:
            if (instrument_key == instrument_key_nifty) and (expiry_date == expiry_list_nifty[0]):
                with open(f'data/{tdate}_past_data.json', 'r') as file_read:
                    past_data = json.load(file_read)
                initialize=2
        except:
            pass

        if initialize==1:
            past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}'] = {'ce_ltp': [], 'pe_ltp': [], 'ce_theta' : [], 'pe_theta' : [], 'ce_vega' : [], 'pe_vega' : [], 'ce_iv' : [], 'pe_iv' : [], 'ce_oi' : [], 'pe_oi' : [], 'ce_atm' : [], 'pe_atm' : [], 'atm_straddle' : [], 'spot_price':[], 'india_vix':[], 'time' : []}
      
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_ltp'].append(main_df.iloc[0,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_ltp'].append(main_df.iloc[1,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_theta'].append(main_df.iloc[2,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_theta'].append(main_df.iloc[3,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_vega'].append(main_df.iloc[4,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_vega'].append(main_df.iloc[5,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_iv'].append(main_df.iloc[6,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_iv'].append(main_df.iloc[7,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_oi'].append(main_df.iloc[8,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_oi'].append(main_df.iloc[9,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['ce_atm'].append(main_df.iloc[10,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['pe_atm'].append(main_df.iloc[11,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['atm_straddle'].append(main_df.iloc[12,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['spot_price'].append(main_df.iloc[13,0])
        # past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['india_vix'].append(main_df.iloc[14,0])
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['india_vix'].append(india_vix)
        past_data[f'Today : {t_date} | {instrument_key} | Expiry : {expiry_date}']['time'].append(main_df.iloc[15,0])
        
        return option_df, main_df, expiry_name

abc=1
de=1

app = QApplication([])

# Create main window
win = pg.GraphicsLayoutWidget(title="Real-Time Plot (1 Subplot)")
win.resize(1500, 1200)
win.show()

###################################################################
# Initialize data for each expiry's time axis
x1, x2, x3 = [], [], []  # Time arrays for each expiry
y0_1, y1_1, y6_1, y7_1, y10_1, y11_1, y12_1, y13_1, y15_1 = [], [], [], [], [], [], [], [], []
y0_2, y1_2, y6_2, y7_2, y10_2, y11_2, y12_2, y13_2, y15_2 = [], [], [], [], [], [], [], [], []
y0_3, y1_3, y6_3, y7_3, y10_3, y11_3, y12_3, y13_3, y15_3 = [], [], [], [], [], [], [], [], []

plot00 = win.addPlot(row=0, col=0, title=f"Nifty - CE/PE OTMs")
plot00.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot00.addLegend()
# plot00.showGrid(x=True, y=True, alpha=0.3)
# Set the x-axis formatting to use time strings
plot00.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_1 = plot00.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_1 = plot00.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot10 = win.addPlot(row=1, col=0, title="Nifty - CE-PE ATM, Straddle")
plot10.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot10.addLegend()
# plot10.showGrid(x=True, y=True, alpha=0.3)
plot10.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_1 = plot10.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_1 = plot10.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_1 = plot10.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot20 = win.addPlot(row=2, col=0, title="Nifty - CE/PE OTMs Implied Volatility")
plot20.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot20.addLegend()
# plot20.showGrid(x=True, y=True, alpha=0.3)
plot20.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_1 = plot20.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_1 = plot20.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_1 = plot20.plot([], pen=mkPen('r', width=3), name='SPOT')

################################################################################## Expiry 2

plot01 = win.addPlot(row=0, col=1, title=f"Bank Nifty - CE/PE OTMs")
plot01.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot01.addLegend()
# plot01.showGrid(x=True, y=True, alpha=0.3)
plot01.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_2 = plot01.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_2 = plot01.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot11 = win.addPlot(row=1, col=1, title="Bank Nifty - CE-PE ATM, Straddle")
plot11.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot11.addLegend()
# plot11.showGrid(x=True, y=True, alpha=0.3)
plot11.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_2 = plot11.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_2 = plot11.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_2 = plot11.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot21 = win.addPlot(row=2, col=1, title="Bank Nifty - CE/PE OTMs Implied Volatility")
plot21.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot21.addLegend()
# plot21.showGrid(x=True, y=True, alpha=0.3)
plot21.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_2 = plot21.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_2 = plot21.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_2 = plot21.plot([], pen=mkPen('r', width=3), name='SPOT')

################################################################################# Expiry 3

plot02 = win.addPlot(row=0, col=2, title=f"Sensex - CE/PE OTMs")
plot02.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot02.addLegend()
# plot02.showGrid(x=True, y=True, alpha=0.3)
plot02.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_0_3 = plot02.plot([], pen=mkPen('g', width=3), name='CE OTMs')
line_1_3 = plot02.plot([], pen=mkPen('y', width=3), name='PE OTMs')

plot12 = win.addPlot(row=1, col=2, title="Sensex - CE-PE ATM, Straddle")
plot12.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot12.addLegend()
# plot12.showGrid(x=True, y=True, alpha=0.3)
plot12.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_10_3 = plot12.plot([], pen=mkPen('g', width=3), name='CE ATM')
line_11_3 = plot12.plot([], pen=mkPen('y', width=3), name='PE ATM')
line_12_3 = plot12.plot([], pen=mkPen('m', width=3), name='ATM Straddle')

plot22 = win.addPlot(row=2, col=2, title="Sensex - CE/PE OTMs Implied Volatility")
plot22.addLine(y=0, pen=pg.mkPen(color='w', width=1.5))
plot22.addLegend()
# plot22.showGrid(x=True, y=True, alpha=0.3)
plot22.getAxis('bottom').setTickStrings = lambda values, scale, spacing: format_time_ticks(values)
line_6_3 = plot22.plot([], pen=mkPen('g', width=3), name='CE IV')
line_7_3 = plot22.plot([], pen=mkPen('y', width=3), name='PE IV')
line_13_3 = plot22.plot([], pen=mkPen('r', width=3), name='SPOT')

for plot in [plot00, plot10, plot20, plot01, plot11, plot21, plot02, plot12, plot22]:
    plot.getAxis('bottom').tickStrings = format_time_ticks

#################################################################################

# For plot20's ViewBox - Create the data item FIRST
line_13_1_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_20 = pg.ViewBox()
plot20.showAxis('right')
plot20.scene().addItem(vb_right_20)
plot20.getAxis('right')#.setLabel("SPOT")  # More descriptive label
plot20.getAxis('right').linkToView(vb_right_20)  # Link right axis to right ViewBox
vb_right_20.setXLink(plot20)  # Keep X-axis linked for alignment
vb_right_20.setYLink(None)  # Explicitly unlink Y-axis
vb_right_20.addItem(line_13_1_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_20 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_20.addItem(zero_line_20)  # Add the zero line to the ViewBox

# For plot20
def updateViews_20():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_20.setGeometry(plot20.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_20.setYLink(None)

def adjust_right_view_20():
    """Dynamically adjust the range of the right Y-axis for plot20."""
    if y13_1:
        # Set explicit Y range based on SPOT data (y13_1)
        min_val = min(y13_1) - abs(min(y13_1) * 0.05)  # 5% padding below
        max_val = max(y13_1) + abs(max(y13_1) * 0.05)  # 5% padding above
        vb_right_20.setYRange(min_val, max_val)

plot20.vb.sigResized.connect(updateViews_20)

# Similarly for plot21
line_13_2_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_21 = pg.ViewBox()
plot21.showAxis('right')
plot21.scene().addItem(vb_right_21)
plot21.getAxis('right')#.setLabel("SPOT")
plot21.getAxis('right').linkToView(vb_right_21)
vb_right_21.setXLink(plot21)
vb_right_21.setYLink(None)
vb_right_21.addItem(line_13_2_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_21 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_21.addItem(zero_line_21)  # Add the zero line to the ViewBox

# For plot21
def updateViews_21():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_21.setGeometry(plot21.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_21.setYLink(None)

def adjust_right_view_21():
    """Dynamically adjust the range of the right Y-axis for plot21."""
    if y13_2:
        # Set explicit Y range based on SPOT data (y13_2)
        min_val = min(y13_2) - abs(min(y13_2) * 0.05)  # 5% padding below
        max_val = max(y13_2) + abs(max(y13_2) * 0.05)  # 5% padding above
        vb_right_21.setYRange(min_val, max_val)

plot21.vb.sigResized.connect(updateViews_21)

# And for plot22
line_13_3_right = pg.PlotDataItem(pen=mkPen('r', width=3), name='SPOT')
vb_right_22 = pg.ViewBox()
plot22.showAxis('right')
plot22.scene().addItem(vb_right_22)
plot22.getAxis('right')#.setLabel("SPOT")
plot22.getAxis('right').linkToView(vb_right_22)
vb_right_22.setXLink(plot22)
vb_right_22.setYLink(None)
vb_right_22.addItem(line_13_3_right)  # Add the data item to the right ViewBox

# Create a horizontal line at y=0 for the right ViewBox
zero_line_22 = pg.InfiniteLine(pos=0, angle=0, pen=pg.mkPen(color='r', width=1.5))
vb_right_22.addItem(zero_line_22)  # Add the zero line to the ViewBox

# For plot22
def updateViews_22():
    """Ensure the right ViewBox is aligned with the left ViewBox geometrically."""
    vb_right_22.setGeometry(plot22.vb.sceneBoundingRect())  # Align geometrically
    # Remove any Y-axis link that might be causing synchronization
    vb_right_22.setYLink(None)

def adjust_right_view_22():
    """Dynamically adjust the range of the right Y-axis for plot22."""
    if y13_3:
        # Set explicit Y range based on SPOT data (y13_3)
        min_val = min(y13_3) - abs(min(y13_3) * 0.05)  # 5% padding below
        max_val = max(y13_3) + abs(max(y13_3) * 0.05)  # 5% padding above
        vb_right_22.setYRange(min_val, max_val)

plot22.vb.sigResized.connect(updateViews_22)

#############################################################

# --------------- Labels ---------------

label_dict = {}

# For plot00
label_0 = TextItem(anchor=(0, 0.5))
label_0.setFont(QFont('Arial', 12))
plot00.addItem(label_0)
label_dict['label_0'] = label_0

label_1 = TextItem(anchor=(0, 0.5))
label_1.setFont(QFont('Arial', 12))
plot00.addItem(label_1)
label_dict['label_1'] = label_1

# For plot10
label_10 = TextItem(anchor=(0, 0.5))
label_10.setFont(QFont('Arial', 12))
plot10.addItem(label_10)
label_dict['label_10'] = label_10

label_11 = TextItem(anchor=(0, 0.5))
label_11.setFont(QFont('Arial', 12))
plot10.addItem(label_11)
label_dict['label_11'] = label_11

label_12 = TextItem(anchor=(0, 0.5))
label_12.setFont(QFont('Arial', 12))
plot10.addItem(label_12)
label_dict['label_12'] = label_12

# For plot20
label_6 = TextItem(anchor=(0, 0.5))
label_6.setFont(QFont('Arial', 12))
plot20.addItem(label_6)
label_dict['label_6'] = label_6

label_7 = TextItem(anchor=(0, 0.5))
label_7.setFont(QFont('Arial', 12))
plot20.addItem(label_7)
label_dict['label_7'] = label_7

label_13 = TextItem(anchor=(0, 0.5))
label_13.setFont(QFont('Arial', 12))
plot20.addItem(label_13)
label_dict['label_13'] = label_13

# For plot01
label_0_2 = TextItem(anchor=(0, 0.5))
label_0_2.setFont(QFont('Arial', 12))
plot01.addItem(label_0_2)
label_dict['label_0_2'] = label_0_2

label_1_2 = TextItem(anchor=(0, 0.5))
label_1_2.setFont(QFont('Arial', 12))
plot01.addItem(label_1_2)
label_dict['label_1_2'] = label_1_2

# For plot11
label_10_2 = TextItem(anchor=(0, 0.5))
label_10_2.setFont(QFont('Arial', 12))
plot11.addItem(label_10_2)
label_dict['label_10_2'] = label_10_2

label_11_2 = TextItem(anchor=(0, 0.5))
label_11_2.setFont(QFont('Arial', 12))
plot11.addItem(label_11_2)
label_dict['label_11_2'] = label_11_2

label_12_2 = TextItem(anchor=(0, 0.5))
label_12_2.setFont(QFont('Arial', 12))
plot11.addItem(label_12_2)
label_dict['label_12_2'] = label_12_2

# For plot21
label_6_2 = TextItem(anchor=(0, 0.5))
label_6_2.setFont(QFont('Arial', 12))
plot21.addItem(label_6_2)
label_dict['label_6_2'] = label_6_2

label_7_2 = TextItem(anchor=(0, 0.5))
label_7_2.setFont(QFont('Arial', 12))
plot21.addItem(label_7_2)
label_dict['label_7_2'] = label_7_2

label_13_2 = TextItem(anchor=(0, 0.5))
label_13_2.setFont(QFont('Arial', 12))
plot21.addItem(label_13_2)
label_dict['label_13_2'] = label_13_2

# For plot02
label_0_3 = TextItem(anchor=(0, 0.5))
label_0_3.setFont(QFont('Arial', 12))
plot02.addItem(label_0_3)
label_dict['label_0_3'] = label_0_3

label_1_3 = TextItem(anchor=(0, 0.5))
label_1_3.setFont(QFont('Arial', 12))
plot02.addItem(label_1_3)
label_dict['label_1_3'] = label_1_3

# For plot12
label_10_3 = TextItem(anchor=(0, 0.5))
label_10_3.setFont(QFont('Arial', 12))
plot12.addItem(label_10_3)
label_dict['label_10_3'] = label_10_3

label_11_3 = TextItem(anchor=(0, 0.5))
label_11_3.setFont(QFont('Arial', 12))
plot12.addItem(label_11_3)
label_dict['label_11_3'] = label_11_3

label_12_3 = TextItem(anchor=(0, 0.5))
label_12_3.setFont(QFont('Arial', 12))
plot12.addItem(label_12_3)
label_dict['label_12_3'] = label_12_3

# For plot22
label_6_3 = TextItem(anchor=(0, 0.5))
label_6_3.setFont(QFont('Arial', 12))
plot22.addItem(label_6_3)
label_dict['label_6_3'] = label_6_3

label_7_3 = TextItem(anchor=(0, 0.5))
label_7_3.setFont(QFont('Arial', 12))
plot22.addItem(label_7_3)
label_dict['label_7_3'] = label_7_3

label_13_3 = TextItem(anchor=(0, 0.5))
label_13_3.setFont(QFont('Arial', 12))
plot22.addItem(label_13_3)
label_dict['label_13_3'] = label_13_3

# Create separate labels for SPOT data - add this after all other label definitions
label_13_right = TextItem(anchor=(0, 0.5))
label_13_right.setFont(QFont('Arial', 12))
vb_right_20.addItem(label_13_right)  # Add to the right ViewBox
label_dict['label_13_right'] = label_13_right

label_13_2_right = TextItem(anchor=(0, 0.5))
label_13_2_right.setFont(QFont('Arial', 12))
vb_right_21.addItem(label_13_2_right)  # Add to the right ViewBox
label_dict['label_13_2_right'] = label_13_2_right

label_13_3_right = TextItem(anchor=(0, 0.5))
label_13_3_right.setFont(QFont('Arial', 12))
vb_right_22.addItem(label_13_3_right)  # Add to the right ViewBox
label_dict['label_13_3_right'] = label_13_3_right

i=0

expiry_name_0, expiry_name_1, expiry_name_2, expiry_name_3, expiry_name_4 = None, None, None, None, None

def update():
    global a,b,c,d,e, initialize,i
    global expiry_name_0, expiry_name_1, expiry_name_2, expiry_name_3, expiry_name_4
    # tt1 = time.time()
    nifty_0_chain, nifty_0_main_df, expiry_name_0 = chain(instrument_key_nifty,expiry_list_nifty[0],a)
    nifty_1_chain, nifty_1_main_df, expiry_name_1 = chain(instrument_key_nifty,expiry_list_nifty[1],b)
    nifty_3_chain, nifty_3_main_df, expiry_name_2 = chain(instrument_key_nifty,expiry_list_nifty[2],c)
    bnf_0_chain, bnf_0_main_df, expiry_name_3 = chain(instrument_key_bnf,expiry_list_bnf[0],d)
    sensex_0_chain, sensex_0_main_df, expiry_name_4 = chain(instrument_key_sensex,expiry_list_sensex[0],e)

    initialize=2

    df_concat = check_data(structure_initial,structure_current)

    if a==b==c==d==e==3:
        with open(f'data/{tdate}_initial_values.json', 'w') as file_write:
            json.dump(structure_initial, file_write)

    with open(f'data/{tdate}_past_data.json', 'w') as file_write:
        json.dump(past_data, file_write)

    dfp = pd.DataFrame(past_data)

    for i in range(0,5):
        dfp.iloc[0,i] = round(pd.Series(dfp.iloc[0,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[1,i] = round(pd.Series(dfp.iloc[1,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[2,i] = round(pd.Series(dfp.iloc[2,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[3,i] = round(pd.Series(dfp.iloc[3,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[4,i] = round(pd.Series(dfp.iloc[4,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[5,i] = round(pd.Series(dfp.iloc[5,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[6,i] = round(pd.Series(dfp.iloc[6,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[7,i] = round(pd.Series(dfp.iloc[7,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[8,i] = round(pd.Series(dfp.iloc[8,i]).ewm(span=100, adjust=False).mean(),5).tolist()
        dfp.iloc[9,i] = round(pd.Series(dfp.iloc[9,i]).ewm(span=100, adjust=False).mean(),5).tolist()
        dfp.iloc[10,i] = round(pd.Series(dfp.iloc[10,i]).ewm(span=100, adjust=False).mean(),5).tolist()
        dfp.iloc[11,i] = round(pd.Series(dfp.iloc[11,i]).ewm(span=100, adjust=False).mean(),5).tolist()
        dfp.iloc[12,i] = round(pd.Series(dfp.iloc[12,i]).ewm(span=100, adjust=False).mean(),5).tolist()
        dfp.iloc[13,i] = round(pd.Series(dfp.iloc[13,i]).ewm(span=300, adjust=False).mean(),5).tolist()
        dfp.iloc[14,i] = round(pd.Series(dfp.iloc[14,i]).ewm(span=300, adjust=False).mean(),5).tolist()

    # Get time data for all three expiries
    time_str_1 = dfp.iloc[15,0][i]  # Time for Expiry 1 (Nifty)
    time_str_2 = dfp.iloc[15,3][i]  # Time for Expiry 2 (Bank Nifty)
    time_str_3 = dfp.iloc[15,4][i]  # Time for Expiry 3 (Sensex)
    
    # Convert time strings to timestamps
    timestamp_1 = time_string_to_timestamp(time_str_1)
    timestamp_2 = time_string_to_timestamp(time_str_2)
    timestamp_3 = time_string_to_timestamp(time_str_3)
    
    # Store timestamps in x-axis arrays
    x1.append(timestamp_1)
    x2.append(timestamp_2)
    x3.append(timestamp_3)

    # Update Expiry 1 data
    y0_1.append(dfp.iloc[0,0][i])
    y1_1.append(dfp.iloc[1,0][i])
    y10_1.append(dfp.iloc[10,0][i])
    y11_1.append(dfp.iloc[11,0][i])
    y12_1.append(dfp.iloc[12,0][i])
    y6_1.append(dfp.iloc[6,0][i])
    y7_1.append(dfp.iloc[7,0][i])
    y13_1.append(dfp.iloc[13,0][i])
    y15_1.append(dfp.iloc[15,0][i])  # Time data

    # Update Expiry 1 plots with timestamps
    line_0_1.setData(x1, y0_1)
    line_1_1.setData(x1, y1_1)
    line_10_1.setData(x1, y10_1)
    line_11_1.setData(x1, y11_1)
    line_12_1.setData(x1, y12_1)
    line_6_1.setData(x1, y6_1)
    line_7_1.setData(x1, y7_1)
    line_13_1_right.setData(x1, y13_1)  # Use timestamps for right y-axis too
    adjust_right_view_20()

    # Update Expiry 2 data
    y0_2.append(dfp.iloc[0,3][i])
    y1_2.append(dfp.iloc[1,3][i])
    y10_2.append(dfp.iloc[10,3][i])
    y11_2.append(dfp.iloc[11,3][i])
    y12_2.append(dfp.iloc[12,3][i])
    y6_2.append(dfp.iloc[6,3][i])
    y7_2.append(dfp.iloc[7,3][i])
    y13_2.append(dfp.iloc[13,3][i])
    y15_2.append(dfp.iloc[15,3][i])  # Time data

    # Update Expiry 2 plots with timestamps
    line_0_2.setData(x2, y0_2)
    line_1_2.setData(x2, y1_2)
    line_10_2.setData(x2, y10_2)
    line_11_2.setData(x2, y11_2)
    line_12_2.setData(x2, y12_2)
    line_6_2.setData(x2, y6_2)
    line_7_2.setData(x2, y7_2)
    line_13_2_right.setData(x2, y13_2)  # Use timestamps for right y-axis too
    adjust_right_view_21()

    # Update Expiry 3 data
    y0_3.append(dfp.iloc[0,4][i])
    y1_3.append(dfp.iloc[1,4][i])
    y10_3.append(dfp.iloc[10,4][i])
    y11_3.append(dfp.iloc[11,4][i])
    y12_3.append(dfp.iloc[12,4][i])
    y6_3.append(dfp.iloc[6,4][i])
    y7_3.append(dfp.iloc[7,4][i])
    y13_3.append(dfp.iloc[13,4][i])
    y15_3.append(dfp.iloc[15,4][i])  # Time data

    # Update Expiry 3 plots with timestamps
    line_0_3.setData(x3, y0_3)
    line_1_3.setData(x3, y1_3)
    line_10_3.setData(x3, y10_3)
    line_11_3.setData(x3, y11_3)
    line_12_3.setData(x3, y12_3)
    line_6_3.setData(x3, y6_3)
    line_7_3.setData(x3, y7_3)
    line_13_3_right.setData(x3, y13_3)  # Use timestamps for right y-axis too
    adjust_right_view_22()
   
    summary.range('C2').value = nifty_0_main_df
    summary.range('F2').value = nifty_1_main_df
    summary.range('I2').value = nifty_3_main_df
    summary.range('L2').value = bnf_0_main_df
    summary.range('O2').value = sensex_0_main_df

    summary.range('A20').value = df_concat

    nifty_0.range('A1').value = nifty_0_chain
    nifty_1.range('A1').value = nifty_1_chain
    nifty_3.range('A1').value = nifty_3_chain
    bnf_0.range('A1').value = bnf_0_chain
    sensex_0.range('A1').value = sensex_0_chain
    
    if a<=3:
        a=a+1
        b=b+1
        c=c+1
        d=d+1
        e=e+1

    # Update Labels with timestamps for x-position
    if x1 and y0_1:
        # Update Expiry 1 labels
        label_dict['label_0'].setText(f"{y0_1[-1]:.2f}")
        label_dict['label_0'].setPos(x1[-1], y0_1[-1])
        label_dict['label_1'].setText(f"{y1_1[-1]:.2f}")
        label_dict['label_1'].setPos(x1[-1], y1_1[-1])
        label_dict['label_10'].setText(f"{y10_1[-1]:.2f}")
        label_dict['label_10'].setPos(x1[-1], y10_1[-1])
        label_dict['label_11'].setText(f"{y11_1[-1]:.2f}")
        label_dict['label_11'].setPos(x1[-1], y11_1[-1])
        label_dict['label_12'].setText(f"{y12_1[-1]:.2f}")
        label_dict['label_12'].setPos(x1[-1], y12_1[-1])
        label_dict['label_6'].setText(f"{y6_1[-1]:.2f}")
        label_dict['label_6'].setPos(x1[-1], y6_1[-1])
        label_dict['label_7'].setText(f"{y7_1[-1]:.2f}")
        label_dict['label_7'].setPos(x1[-1], y7_1[-1])
        label_dict['label_13_right'].setText(f"{y13_1[-1]:.2f}")
        label_dict['label_13_right'].setPos(x1[-1], y13_1[-1])

    if x2 and y0_2:
        # Update Expiry 2 labels
        label_dict['label_0_2'].setText(f"{y0_2[-1]:.2f}")
        label_dict['label_0_2'].setPos(x2[-1], y0_2[-1])
        label_dict['label_1_2'].setText(f"{y1_2[-1]:.2f}")
        label_dict['label_1_2'].setPos(x2[-1], y1_2[-1])
        label_dict['label_10_2'].setText(f"{y10_2[-1]:.2f}")
        label_dict['label_10_2'].setPos(x2[-1], y10_2[-1])
        label_dict['label_11_2'].setText(f"{y11_2[-1]:.2f}")
        label_dict['label_11_2'].setPos(x2[-1], y11_2[-1])
        label_dict['label_12_2'].setText(f"{y12_2[-1]:.2f}")
        label_dict['label_12_2'].setPos(x2[-1], y12_2[-1])
        label_dict['label_6_2'].setText(f"{y6_2[-1]:.2f}")
        label_dict['label_6_2'].setPos(x2[-1], y6_2[-1])
        label_dict['label_7_2'].setText(f"{y7_2[-1]:.2f}")
        label_dict['label_7_2'].setPos(x2[-1], y7_2[-1])
        label_dict['label_13_2_right'].setText(f"{y13_2[-1]:.2f}")
        label_dict['label_13_2_right'].setPos(x2[-1], y13_2[-1])

    if x3 and y0_3:
        # Update Expiry 3 labels
        label_dict['label_0_3'].setText(f"{y0_3[-1]:.2f}")
        label_dict['label_0_3'].setPos(x3[-1], y0_3[-1])
        label_dict['label_1_3'].setText(f"{y1_3[-1]:.2f}")
        label_dict['label_1_3'].setPos(x3[-1], y1_3[-1])
        label_dict['label_10_3'].setText(f"{y10_3[-1]:.2f}")
        label_dict['label_10_3'].setPos(x3[-1], y10_3[-1])
        label_dict['label_11_3'].setText(f"{y11_3[-1]:.2f}")
        label_dict['label_11_3'].setPos(x3[-1], y11_3[-1])
        label_dict['label_12_3'].setText(f"{y12_3[-1]:.2f}")
        label_dict['label_12_3'].setPos(x3[-1], y12_3[-1])
        label_dict['label_6_3'].setText(f"{y6_3[-1]:.2f}")
        label_dict['label_6_3'].setPos(x3[-1], y6_3[-1])
        label_dict['label_7_3'].setText(f"{y7_3[-1]:.2f}")
        label_dict['label_7_3'].setPos(x3[-1], y7_3[-1])
        label_dict['label_13_3_right'].setText(f"{y13_3[-1]:.2f}")
        label_dict['label_13_3_right'].setPos(x3[-1], y13_3[-1])

    # Set X range for each column of plots separately based on timestamps
    if x1 and len(x1) > 1:
        # Set X range for Expiry 1 plots (first column)
        plot00.setXRange(x1[0], x1[-1], padding=0.1)
        plot10.setXRange(x1[0], x1[-1], padding=0.1)
        plot20.setXRange(x1[0], x1[-1], padding=0.1)
    
    if x2 and len(x2) > 1:
        # Set X range for Expiry 2 plots (second column)
        plot01.setXRange(x2[0], x2[-1], padding=0.1)
        plot11.setXRange(x2[0], x2[-1], padding=0.1)
        plot21.setXRange(x2[0], x2[-1], padding=0.1)
    
    if x3 and len(x3) > 1:
        # Set X range for Expiry 3 plots (third column)
        plot02.setXRange(x3[0], x3[-1], padding=0.1)
        plot12.setXRange(x3[0], x3[-1], padding=0.1)
        plot22.setXRange(x3[0], x3[-1], padding=0.1)

    i += 1
    if i >= 2800:
        exporter = ImageExporter(win.scene())
        exporter.parameters()['width'] = 1600
        exporter.export("plot_snapshot.png")
        print("Plot saved as plot_snapshot.png")
        timer.stop()

# Start timer
timer = QTimer()
timer.timeout.connect(update)
timer.start()

from PyQt5.QtCore import Qt

# Add this after creating the win object
def keyPressEvent(event):
    if event.key() == Qt.Key_F11:  # F11 is commonly used for toggling fullscreen
        if win.isFullScreen():
            win.showMaximized()
        else:
            win.showFullScreen()
    elif event.key() == Qt.Key_Escape and win.isFullScreen():  # ESC to exit fullscreen
        win.showMaximized()

# Connect the keyPressEvent function to the window
win.keyPressEvent = keyPressEvent

#####################################################################

# Run app
app.exec_()