from datetime import datetime
from io import BytesIO
from os.path import exists
import pandas as pd
import requests
import zipfile
from IPython.display import display


def request_file(url, zip_name):
    # get current year and month and create yyyymm format to match correct file url
    cur_year = datetime.now().year
    cur_month = datetime.now().month - 1
    prev_period = datetime(cur_year, cur_month, 1).strftime("%Y-%m-%d")

    # period_range = pandas.period_range(start='2021-01-01', end=prev_period, freq='m')
    period_range = pd.period_range(start='2021-01-01', end='2021-04-01', freq='m')

    # check the csv files are already exist
    # if exist then ignore

    # download and unzip files in the range of periods

    file_list = []
    for p in period_range:
        p = p.strftime("%Y%m")
        file_url = url + p + zip_name
        unzip_name = p + zip_name.split('.')[0] + '.csv'
        # loop current directory to get file name
        if exists(f'./{unzip_name}'):
            print(f'{unzip_name} already exist')
            file_list.append(unzip_name)
            continue
        else:
            r = requests.get(file_url)
            zip_file = zipfile.ZipFile(BytesIO(r.content))
            zip_file.extractall('./')
            file_list.append(unzip_name)

    return file_list


def read_files(file_name, file_list):
    if file_name == 'capital bike':
        usecols = [0, 1, 2, 3, 8, 9, 10, 11, 12]
    elif file_name == 'citi bike':
        usecols = [0, 1, 2, 3, 8, 9, 10, 11, 12]
    elif file_name == 'metro bike':
        usecols = [0, 1, 2, 3, 5, 6, 8, 9, 10, 13, 14]
    elif file_name == 'divvy bike':
        usecols = [0, 1, 2, 3, 8, 9, 10, 11, 12]

    if len(file_list) == 0:
        return
    path = '../'
    file_test = file_list[0]
    df = pd.read_csv(path + file_test, header=0, usecols=usecols)
    display(df.head(10))

    return df


if __name__ == '__main__':
    # request bike files from url
    # read csv files
    # load csv files into data frame
    # aggregate spring, summer, august and winter data
    # request covid 19 files
    # plot # of cases vs bike share usage
    # calculate distance of bike rides

    capital_bike_url = f'https://s3.amazonaws.com/capitalbikeshare-data/'
    capital_bike_zip = '-capitalbikeshare-tripdata.zip'
    capital_bike_files = request_file(capital_bike_url, capital_bike_zip)
    capital_bike_df = read_files('capital bike', capital_bike_files)

