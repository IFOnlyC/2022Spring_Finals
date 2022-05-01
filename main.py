import os
from datetime import datetime
from io import BytesIO
from geographiclib.geodesic import Geodesic
import pandas as pd
import requests
import zipfile
from IPython.display import display
from urllib.parse import urlparse
from os.path import exists


def request_files(file_url, file_list, *file_name):
    # file_name was a string, but get passed in as a tuple
    try:
        if len(file_name) >= 1:
            file_name = file_name[0]

        if exists(f'./{file_name}'):
            file_list.append(file_name)
        else:
            r = requests.get(file_url)
            urlpath = urlparse(file_url).path
            file_extension = urlpath[urlpath.rfind('.')+1:]
            if file_extension == 'zip':
                zip_file = zipfile.ZipFile(BytesIO(r.content))
                zip_file.extractall('./')
                file_list.append(file_name)
            elif file_extension == 'csv':
                file_header = r.headers
                file_name = file_header['content-disposition'].split()[1][9:]
                with open(f'./{file_name}', 'wb') as f:
                    f.write(r.content)
                    f.close()
                file_list.append(file_name)

            elif file_extension == 'xlsx':
                file_name = urlpath.split('/')[-1]
                with open(file_name, 'wb') as f:
                    f.write(r.content)
                file_list.append(file_name)
    except Exception as e:
        print(f'request file error: {e}')


def prepare_files(url, *file_name, file_type='bike'):
    file_list = []
    if file_type == 'bike':
        # get current year and month and create yyyymm format to match correct file url
        cur_year = datetime.now().year
        cur_month = datetime.now().month - 1
        prev_period = datetime(cur_year, cur_month, 1).strftime("%Y-%m-%d")

        # period_range = pandas.period_range(start='2021-01-01', end=prev_period, freq='m')
        period_range = pd.period_range(start='2021-01-01', end='2021-04-01', freq='m')

        # check the csv files are already exist
        # if exist then ignore
        file_name = file_name[0]
        # download and unzip files in the range of periods
        for p in period_range:
            p = p.strftime("%Y%m")
            file_url = url + p + file_name
            if 'citibike' in file_name.split('-'):
                unzipped_file = 'JC-' + p + file_name.split('.')[0] + '.csv'
            else:
                unzipped_file = p + file_name.split('.')[0] + '.csv'

            request_files(file_url, file_list, unzipped_file)

    elif file_type == 'covid':
        request_files(url, file_list, file_name)

    return file_list


def file_to_df(file_name, file_list):
    try:
        if (file_name == 'Boston_COVID') or (file_name == 'DC_COVID-19_'):
            for f in os.listdir():
                if f[:12] == file_name:
                    file_list.append(f)

        if len(file_list) == 0:
            raise IndexError('no file found in the directory')

        usecolumns = []
        if file_name in ['blue bike', 'citi bike']:
            usecolumns = ['bikeid', 'starttime', 'stoptime', 'start station latitude', 'start station longitude', 'end station latitude', 'end station longitude', 'usertype', 'tripduration']
        elif file_name in ['divvy bike', 'bay wheel bike', 'capital bike']:
            usecolumns = ['ride_id', 'started_at', 'ended_at', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual']
        elif file_name == 'NYC covid':
            usecolumns = ['DATE_OF_INTEREST', 'CASE_COUNT']
        elif file_name == 'Boston_COVID':
            usecolumns = ['Description1', 'Category1', 'Value_unit', 'Value']
        elif file_name == 'DC_COVID-19_':
            usecolumns = ['DATE_REPORTED', 'TOTAL_POSITIVES_TST']
        elif file_name == 'CHI covid':
            usecolumns = ['Date', 'Cases - Total']
        elif file_name == 'SFO covid':
            usecolumns = ['Specimen Collection Date', 'New Cases']

        main_df = pd.DataFrame()
        path = "./"
        for f in file_list:
            df = pd.read_csv(path + f, header=0, usecols=usecolumns)
            main_df = main_df.append(df)
        # display(main_df.head(10))
        # display(main_df.tail(10))
        return main_df

    except Exception as err:
        print('file_to_df error ' + repr(err) + f' for {file_name} ')


def clean_df(df, *df_name, df_type='covid'):
    df_name = df_name[0]
    if df_type == 'bike':
        if df_name in ['divvy', 'bay', 'capital']:
            cast_bike_df(df, df_name)
        if df_name in ['blue', 'citi']:
            pass

    if df_type == 'covid':
        if df_name == 'NYC covid':
            df = df.rename(columns={'DATE_OF_INTEREST': 'Date', 'CASE_COUNT': 'Cases'})
            df = cast_covid_data(df)

        if df_name == 'BOS covid':
            df = df[df['Value_unit'] == 'cases']
            df = df[df['Description1'] == 'Dates']
            df = df.rename(columns={'Category1': 'Date', 'Value': 'Cases'})
            df = df[['Date', 'Cases']]
            df = cast_covid_data(df)

        if df_name == 'CHI covid':
            df = df.rename(columns={'Cases - Total': 'Cases'})
            df = cast_covid_data(df)

        if df_name == 'WAS covid':
            df = df.rename(columns={'DATE_REPORTED': 'Date', 'TOTAL_POSITIVES_TST': 'Cases'})
            df = cast_covid_data(df)

        if df_name == 'SFO covid':
            df = df.rename(columns={'Specimen Collection Date': 'Date', 'New Cases': 'Cases'})
            df = cast_covid_data(df)

    display(df)

    return df


def cast_bike_df(df, df_name):

    if df_name in ['divvy', 'bay', 'capital']:
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['ended_at'] = pd.to_datetime(df['ended_at'])
        df['tripduration'] = (df['ended_at'] - df['started_at']).dt.total_seconds().astype(int)
    if df_name in ['blue', 'citi']:
        pass

    return df

def df_dist(df, df_name):
    gl = Geodesic.WGS84
    list = []
    if df_name in ['divvy', 'bay', 'capital']:
        for index, row in df.iterrows():
            list.append(gl.Inverse(row['start_lat'], row['start_lng'], row['end_lat'], row['end_lng'])['s12'])
        list = pd.DataFrame(list)
        new_df = pd.concat([df, list])

    return new_df



def cast_covid_data(df):
    try:
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        if df['Cases'].dtypes != 'int64':
            df['Cases'] = df['Cases'].fillna(0).astype(int)
        else:
            pass
        return df
    except Exception as err:
        print(f'rename_type error: {err}')


def merge_df(df_list, *df_name):
    merged = pd.DataFrame()



    return merged


if __name__ == '__main__':
    # request bike files from url
    # read csv files
    # load csv files into data frame
    # aggregate spring, summer, august and winter data
    # request covid 19 files
    # plot # of cases vs bike share usage
    # calculate distance of bike rides

    capital_bike_url = 'https://s3.amazonaws.com/capitalbikeshare-data/'
    capital_bike_zip = '-capitalbikeshare-tripdata.zip'
    capital_bike_files = prepare_files(capital_bike_url, capital_bike_zip)
    capital_bike_df = file_to_df('capital bike', capital_bike_files)
    capital_cleaned_df = clean_df(capital_bike_df, 'capital', df_type='bike')

    citi_bike_url = 'https://s3.amazonaws.com/tripdata/JC-'
    citi_bike_zip = '-citibike-tripdata.csv.zip'
    citi_bike_files = prepare_files(citi_bike_url, citi_bike_zip)
    citi_bike_df = file_to_df('citi bike', citi_bike_files)
    citi_cleaned_df = clean_df(citi_bike_df, 'citi', df_type='bike')

    divvy_bike_url = 'https://divvy-tripdata.s3.amazonaws.com/'
    divvy_bike_zip = '-divvy-tripdata.zip'
    divvy_bike_files = prepare_files(divvy_bike_url, divvy_bike_zip)
    divvy_bike_df = file_to_df('divvy bike', divvy_bike_files)
    divvy_cleaned_df = clean_df(divvy_bike_df, 'divvy', df_type='bike')

    blue_bike_url = 'https://s3.amazonaws.com/hubway-data/'
    blue_bike_zip = '-bluebikes-tripdata.zip'
    blue_bike_files = prepare_files(blue_bike_url, blue_bike_zip)
    blue_bike_df = file_to_df('blue bike', blue_bike_files)
    blue_cleaned_df = clean_df(blue_bike_df, 'blue', df_type='bike')

    bay_wheel_url = 'https://s3.amazonaws.com/baywheels-data/'
    bay_wheel_zip = '-baywheels-tripdata.csv.zip'
    bay_wheel_files = prepare_files(bay_wheel_url, bay_wheel_zip)
    bay_wheel_df = file_to_df('bay wheel bike', bay_wheel_files)
    bay_cleaned_df = clean_df(bay_wheel_df, 'bay', df_type='bike')

    bike_list = ['capital_cleaned_df', 'citi_cleaned_df', 'divvy_cleaned_df', 'blue_cleaned_df', 'bay_cleaned_df']

    NYC_covid_url = 'https://data.cityofnewyork.us/api/views/rc75-m7u3/rows.csv?accessType=DOWNLOAD'
    NYC_file = prepare_files(NYC_covid_url, 'NYC_covid', file_type='covid')
    NYC_df = file_to_df('NYC covid', NYC_file)
    NYC_cleaned_df = clean_df(NYC_df, 'NYC covid')

    WAS_df = file_to_df('DC_COVID-19_', [])
    WAS_cleaned_df = clean_df(WAS_df, 'WAS covid')

    SFO_covid_url = 'https://data.sfgov.org/api/views/gyr2-k29z/rows.csv?accessType=DOWNLOAD'
    SFO_file = prepare_files(SFO_covid_url, 'SFO_covid', file_type='covid')
    SFO_df = file_to_df('SFO covid', SFO_file)
    SFO_cleaned_df = clean_df(SFO_df, 'SFO covid')

    CHI_covid_url = 'https://data.cityofchicago.org/api/views/naz8-j4nc/rows.csv?accessType=DOWNLOAD'
    CHI_file = prepare_files(CHI_covid_url, 'CHI_covid', file_type='covid')
    CHI_df = file_to_df('CHI covid', CHI_file)
    CHI_cleaned_df = clean_df(CHI_df, 'CHI covid')

    BOS_df = file_to_df('Boston_COVID', [])
    BOS_cleaned_df = clean_df(BOS_df, 'BOS covid')

    covid_list = ['NYC_cleaned_df', 'WAS_cleaned_df', 'SFO_cleaned_df', 'CHI_cleaned_df', 'BOS_cleaned_df']

    bike_merge_df = merge_df(bike_list)
    covid_merge_df = merge_df(covid_list)
