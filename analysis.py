
import pandas as pd
import os
import numpy as np
import pytz
from datetime import datetime

gmt_0_timezone = pytz.timezone('UTC')
taipei = pytz.timezone('Asia/Taipei')


# data link: https://drive.google.com/drive/folders/1grrL0XK77kBtw-g3S8JwF7N0vhnUlhXT

def timestamp_to_date_taipei(time_stamp):
    time_stamp = int(time_stamp) * 10 **(-3)
    date = datetime.fromtimestamp(time_stamp, taipei).strftime('%Y-%m-%d %H:%M')

    return date


input_file_path = './data/input/MATIC.csv'
output_file_path = './data/output/output_data/MATIC_edit.csv'

#####################################################################
# check working directory
#####################################################################

# Import the os moduleimportos# Print the current working directory

print("Current working directory:{0}".format(os.getcwd()))

# Change the current working directory
#os.chdir('/Users/laalberta/Documents/Crypto_Project/teahouse/strategy_official/')

# Print the current working directory
print("Current working directory:{0}".format(os.getcwd()))


#####################################################################
# read csv and get hourly record
#####################################################################


price_record = pd.read_csv(input_file_path)
price_record['taipei_time'] = price_record['Timestamp'].apply( lambda x: timestamp_to_date_taipei( x ) )


price_record['Hour Funding Rate'] = price_record['Funding Rate'] / 8
price_record['Hour Interest Rate'] = price_record['dailyInterestRate'] / 24
price_record['Perp_Spot_diff'] = price_record['UC'] - price_record['SPOT']

#####################################################################
# perform some actions
#####################################################################

for i in range(1,len(price_record)):

    funding_rate_previous_value = price_record.iloc[i-1]['Hour Funding Rate']
    funding_rate_current_value = price_record.iloc[i]['Hour Funding Rate']

    hour_int_rate_previous_value = price_record.iloc[i-1]['Hour Interest Rate']
    hour_int_rate_current_value = price_record.iloc[i]['Hour Interest Rate']

    if np.isnan(funding_rate_previous_value) is np.False_:
        if np.isnan(funding_rate_current_value) is np.True_:
            price_record.at[i, 'Hour Funding Rate'] = funding_rate_previous_value

    if np.isnan(hour_int_rate_previous_value) is np.False_:
        if np.isnan(hour_int_rate_current_value) is np.True_:
            price_record.at[i, 'Hour Interest Rate'] = hour_int_rate_previous_value





price_record['Hour Interest Rate APY'] = price_record['Hour Interest Rate'] * 24 * 365
price_record['Hour Funding Rate APY'] = price_record['Hour Funding Rate'] * 24 * 365

price_record['diff_hour_int_funding_rate'] = price_record['Hour Interest Rate'] + price_record['Hour Funding Rate']
price_record['diff_hour_int_funding_rate_APY'] = price_record['Hour Interest Rate APY'] + price_record['Hour Funding Rate APY']

#price_record = price_record.dropna()

price_record.to_csv(output_file_path)




#####################################################################
# drawing
#####################################################################

price_record.set_index('taipei_time')


cols_part = ['taipei_time', 'SPOT','Hour Funding Rate APY',
       'Hour Interest Rate APY', 'Perp_Spot_diff', 'diff_hour_int_funding_rate_APY']



#cols_part = ['taipei_time', 'SPOT','Hour Funding Rate',
#       'Hour Interest Rate', 'Perp_Spot_diff', 'diff_hour_int_funding_rate']


test = price_record[cols_part]

test['taipei_time'] = pd.to_datetime(test['taipei_time'])
test = test.set_index('taipei_time')

axes = test.plot( figsize=(15, 8),linestyle='-', subplots=True)

#test.index = test.index.astype(str)
#test["2021-12-15 04:00":"2021-12-15 08:00"].plot()


#axes = test["2021-10-1 04:00":"2021-11-30 08:00"].plot( figsize=(20, 15),linestyle='-', subplots=True)

#axes = test.plot( figsize=(20, 15),linestyle='-', subplots=True)

price_record.to_csv(output_file_path)


