import os
import re
import zipfile
from io import BytesIO
from os.path import exists
from urllib.parse import urlparse
import pandas as pd
import requests
from IPython.core.display_functions import display
from geographiclib.geodesic import Geodesic


def request_files(file_url, file_list, *file_name):
    """
    request different types of file from the file_list
    :param file_url: first part or whole part of a file source url.
    :param file_list: a list of source file
    :param file_name: name of the sourec file passed in as a tuple
    :return: a list of download or exsiting files in the local file

    >>> requests.get('www.https://docs.python.org/3/', ['whatsnew/3.10.html', ''])
        Traceback (most recent call last):
            ...
        requests.exceptions.InvalidSchema: No connection adapters were found for 'www.https://docs.python.org/3/'

    >>> file_url = 'http://history.openweathermap.org/data/2.5/history/city?lat=42.360082&lon=-71.058880&appid=7fed7cf202b7e410119e2cabdf0f0e17'
    >>> requests.get(file_url, [])
        <Response [200]>
    """

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
    """
    getting files ready for cleaning

    :param url: first part or whole part of a file source url.
    :param file_name: name of source file
    :param file_type: determine operations to prepare data
    :return: a list of source file that got downloaded or exsiting in the file
    >>> url = ['www.google.com', 'https://docs.python.org/3/installing/index.html']
    >>> prepare_files(url, [])
    Traceback (most recent call last):
        ...
    TypeError: can only concatenate str (not "list") to str
    """
    file_list = []
    if file_type == 'bike':
        period_range = pd.period_range(start='2021-03-01', end='2021-03-01', freq='m')

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


def get_local_file(file_name, file_list, *file_type):
    """
    check if file exist in the local directory, raise exception if file not found
    :param file_name:  name of the file
    :param file_list:  list of file that exist in the file
    :param file_type:  type of file
    :return: a list of file that exist in the file

    >>> file = 'champaign'
    >>> list = []
    >>> file_list = get_local_file(file, list, 'weather')
        Traceback (most recent call last):
            ...
        IndexError: no file champaign found in the directory
    """
    if (file_name == 'Boston_COVID') or (file_name == 'DC_COVID-19_'):
        for f in os.listdir():
            if f[:12] == file_name:
                file_list.append(f)
    elif file_type[0] == 'weather':
        for f in os.listdir():
            if re.search(file_name, f):
                file_list.append(f)

    if len(file_list) == 0:
        raise IndexError(f'no file {file_name} found in the directory')
    return file_list

def file_to_df(file_name, file_list, file_type=[]):
    """
    read files into a data frame
    :param file_name: name of file that helps dtermine data frame schema and rename operation
    :param file_list: a list of file to be read
    :param file_type: helps to determine schema and other operations for source data
    :return: a data frame

    >>> file_to_df('bike', ['202103-capitalbikeshare-tripdata.csv'], [])
        Empty DataFrame
        Columns: []
        Index: []
    """
    try:
        if len(file_type) == 1:
            file_type = file_type[0]
        if len(file_list) == 0:
            file_list = get_local_file(file_name, file_list, file_type)

        usecolumns = []
        if file_name == 'blue bike':
            usecolumns = ['bikeid', 'starttime', 'stoptime', 'start station latitude', 'start station longitude', 'end station latitude', 'end station longitude', 'usertype', 'tripduration']
        elif file_name in ['divvy bike', 'bay wheel bike', 'capital bike', 'citi bike']:
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

        if file_type == 'weather':
            usecolumns = ['name', 'datetime', 'icon']

        main_df = pd.DataFrame()
        path = "./"
        df = []

        for f in file_list:
            df.append(pd.read_csv(path + f, header=0, usecols=usecolumns))
            main_df = pd.concat(df)

        return main_df

    except Exception as err:
        print('file_to_df error ' + repr(err) + f' for {file_name} ')


def clean_df(df, *df_name, df_type='covid'):
    """
    clean and transform the data frame
    :param df: pandas data frame
    :param df_name: a string in tuple
    :param df_type: string description of data frame type
    :return: a cleaned data frame

    >>> a = [['Window_title','Title','Description1','Category1','Description2','Category2','Value','Value_unit','Value_1','Value_1_unit', 'Comparison', 'Timestamp'],
            ['COVID-19 Positive Tests','COVID-19 Positive Tests','Dates','01/22/2020','Measures','Positive Tests','0','cases','','cases (7-day moving avg)','','04/29/2022']]
    >>> df = pd.DataFrame(a)
    >>> clean = clean_df(df, 'Boston_COVID', 'covid')
    >>> display(clean)
                                 0                        1  ...          11          name
        0             Window_title                    Title  ...   Timestamp  Boston_COVID
        1  COVID-19 Positive Tests  COVID-19 Positive Tests  ...  04/29/2022  Boston_COVID

        [2 rows x 13 columns]
    >>> clean = clean_df(df, 'BOS covid', 'covid')
        Traceback (most recent call last):
            ...
        KeyError: 'Value_unit'
    """
    if df_name:
        df_name = df_name[0]
    if df_type == 'weather':
        df = df.rename(columns={'datetime': 'date', 'icon': 'weather'})

    if df_type == 'bike':
        df = df_dist(df, df_name)
        df = cast_bike_df(df, df_name)

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
    if df_name:
        df['name'] = df_name
    return df


def cast_bike_df(df, df_name):
    """
    cast data frame column types of bike data
    :param df: data frame
    :param df_name: name of data frame
    :return: data fram

    >>> bay = [['357CDE244D24405B','electric_bike','26/01/2021 11:32','26/01/2021 11:38','37.76','-122.41','37.76','-122.42','casual'],
                ['19A3E1F4211D0EE8','electric_bike','26/01/2021 14:16','26/01/2021 14:19','37.77','-122.41','37.76','-122.41','casual']]
    >>> bay = pd.DataFrame(bay, columns = ['ride_id','rideable_type', 'started_at', 'ended_at', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual'])
    >>> bay = cast_bike_df(bay, 'bay')
    >>> display(bay)
                    ride_id  rideable_type  ...  end_lng  member_casual
        0           ride_id  rideable_type  ...  end_lng  member_casual
        1  357CDE244D24405B  electric_bike  ...  -122.42         casual
        2  19A3E1F4211D0EE8  electric_bike  ...  -122.41         casual
        [3 rows x 9 columns]

    >>> blue = [['914','00:04.6','15:19.2','42.366277','-71.09169','-71.07782811','5316','Customer','2139'],
                ['1085','00:21.8','18:27.5','42.35096144','-71.07782811','42.378965','-71.068607','4917','Subscriber','2116']]
    >>> blue = pd.DataFrame(blue, columns = ['tripduration','starttime','stoptime','start station latitude','start station longitude','end station latitude','end station longitude','bikeid','usertype','postal code'])
    >>> blue = cast_bike_df(blue, 'blue')
    >>> display(blue)
          tripduration          started_at  ... member_casual postal code
        0          914 2022-05-03 00:04:36  ...          2139        None
        1         1085 2022-05-03 00:21:48  ...    Subscriber        2116
        [2 rows x 10 columns]

    """
    if df_name in ['divvy', 'bay', 'capital', 'citi']:
        df['started_at'] = pd.to_datetime(df['started_at'])
        df['ended_at'] = pd.to_datetime(df['ended_at'])
        df['tripduration'] = (df['ended_at'] - df['started_at']).dt.total_seconds().astype(int)
    if df_name == 'blue':
        df['starttime'] = pd.to_datetime(df['starttime'])
        df['stoptime'] = pd.to_datetime(df['stoptime'])
        df = df.rename(columns={'bikeid': 'ride_id', 'starttime': 'started_at', 'stoptime': 'ended_at', 'start station latitude': 'start_lat', 'start station longitude': 'start_lng', 'end station latitude': 'end_lat', 'end station longitude': 'end_lng', 'usertype': 'member_casual'})
    return df


def df_dist(df, df_name):
    """
    calculate distance of bike trip
    :param df: data frame
    :param df_name: name of bike companies
    :return: a data frame with bike trip distance

    >>> blue = [['914','00:04.6','15:19.2','42.366277','-71.09169', '42.350961', '-71.077811','5316','Customer','2139'],
                ['1085','00:21.8','18:27.5','42.350944','-71.077811','42.37965','-71.06807','4917','Subscriber','2116']]
    >>> columns = ['tripduration','starttime','stoptime','start station latitude','start station longitude','end station latitude','end station longitude','bikeid','usertype','postal code']
    >>> blue = pd.DataFrame(blue, columns=columns)
    >>> blue['start station latitude'] = blue['start station latitude'].astype(float)
    >>> blue['end station latitude'] = blue['start station latitude'].astype(float)
    >>> blue['end station longitude'] = blue['start station latitude'].astype(float)
    >>> blue['start station longitude'] = blue['start station latitude'].astype(float)
    >>> blue = df_dist(blue, 'blue')
          tripduration starttime stoptime  ...    usertype  postal code  dist
        0          914   00:04.6  15:19.2  ...    Customer         2139   0.0
        1         1085   00:21.8  18:27.5  ...  Subscriber         2116   0.0


    >>> bay = [['357CDE244D24405B','electric_bike','26/01/2021 11:32','26/01/2021 11:38','37.76','-122.41','37.76','-122.42','casual'],
                ['19A3E1F4211D0EE8','electric_bike','26/01/2021 14:16','26/01/2021 14:19','37.77','-122.41','37.76','-122.41','casual']]
    >>> bay = pd.DataFrame(bay, columns = ['ride_id','rideable_type', 'started_at', 'ended_at', 'start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual'])
    >>> bay['start_lat'] =  bay['start_lat'].astype(float)
    >>> bay['start_lng'] = bay['start_lng'].astype(float)
    >>> bay['end_lat'] = bay['end_lat'].astype(float)
    >>> bay['end_lng'] = bay['end_lng'].astype(float)
    >>> bay = df_dist(bay, 'bay')
                    ride_id  rideable_type  ... member_casual  dist
        0  357CDE244D24405B  electric_bike  ...        casual  0.48
        1  19A3E1F4211D0EE8  electric_bike  ...        casual  0.60
        [2 rows x 10 columns]
    """

    gl = Geodesic.WGS84
    dist_list = []
    if df_name in ['divvy', 'bay', 'capital', 'citi']:
        for index, row in df.iterrows():
            dist = gl.Inverse(row['start_lat'], row['start_lng'], row['end_lat'], row['end_lng'])['s12']
            dist = round(dist/1852.0, 2)
            dist_list.append(dist)
        dist_list = pd.DataFrame(dist_list)
        df['dist'] = dist_list
    if df_name == 'blue':
        for index, row in df.iterrows():
            dist = gl.Inverse(row['start station latitude'], row['start station longitude'], row['end station latitude'], row['end station longitude'])['s12']
            dist = round(dist/1852.0, 2)
            dist_list.append(dist)
        dist_list = pd.DataFrame(dist_list)
        df['dist'] = dist_list
    return df


def cast_covid_data(df):
    """
    cast data column of covid data frame
    :param df: data frame
    :return: casted data frame

    >>>
    """
    try:
        df['Date'] = pd.to_datetime(df['Date']).dt.date
        if df['Cases'].dtypes != 'int64':
            df['Cases'] = df['Cases'].fillna(0).astype(int)
        else:
            pass
        return df
    except Exception as err:
        print(f'rename_type error: {err}')


def merge_df(df_list):
    """
    merge a list of data frames into one data frame
    :param df_list: list of data frame to be merged
    :return: a merged data frame, throw exception if list is empty

    >>> columns = ['DATE_OF_INTEREST','CASE_COUNT']
    >>> nyc = [['02/29/2020','1'], ['03/01/2020','0'], ['03/02/2020','0'], ['03/03/2020','1'], ['03/04/2020','5']]
    >>> nyc = pd.DataFrame(nyc, columns=columns)
    >>> nyc = clean_df(nyc, 'NYC covid', 'covid')
    >>> nyc = cast_covid_data(nyc)
    >>> display(nyc)
                 Date  Cases       name
        0  2020-02-29      1  NYC covid
        1  2020-03-01      0  NYC covid
        2  2020-03-02      0  NYC covid
        3  2020-03-03      1  NYC covid
        4  2020-03-04      5  NYC covid

    """
    if len(df_list) == 1:
        pass
    elif len(df_list) > 1:
        merged = pd.concat(df_list, ignore_index=True)
    else:
        raise Exception('empty list')

    return merged


if __name__ == '__main__':

    """
    steps are in the following order:
    1. request bike files from url
    2. read csv files
    3. load csv files into data f-rame
    4. aggregate spring, summer, august and winter data
    5. request covid 19 files
    6. plot # of cases vs bike share usage
    7. calculate distance of bike rides
    """

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

    print(len(bay_cleaned_df.dtypes))

    bike_list = [capital_cleaned_df, citi_cleaned_df, divvy_cleaned_df, blue_cleaned_df, bay_cleaned_df]

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

    covid_list = [NYC_cleaned_df, WAS_cleaned_df, SFO_cleaned_df, CHI_cleaned_df, BOS_cleaned_df]

    bike_merge_df = merge_df(bike_list)
    covid_merge_df = merge_df(covid_list)

    BOS_weather_df = file_to_df('boston ', [], ['weather'])
    CHI_weather_df = file_to_df('chicago ', [], ['weather'])
    NYC_weather_df = file_to_df('new york ', [], ['weather'])
    SFO_weather_df = file_to_df('san francisco ', [], ['weather'])
    WAS_weather_df = file_to_df('washton ', [], ['weather'])
    weather_list = [BOS_weather_df, CHI_weather_df, NYC_weather_df, SFO_weather_df, WAS_weather_df]
    weather_df = merge_df(weather_list)
    weather_cleaned = clean_df(weather_df, df_type='weather')

    # save processed data into .csv file
    # avoid long time requesting and processing data again
    bike_merge_df.to_csv('bike_merge_df.csv')
    covid_merge_df.to_csv('covid_merge_df.csv')
    weather_cleaned.to_csv('weather_merge_df.csv')
