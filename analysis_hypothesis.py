import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import stats
from pandas.core.frame import DataFrame
import warnings

warnings.filterwarnings("ignore")

city_names = ['Boston', 'NYC', 'Chicago', 'SFO', 'Washington D.C']


def loads_bike_covid_data():
    """
    This function is to load bike data and covid data
    :return: bike_df: a dataframe contains the shared bike information
             covid_df: a dataframe contains the covid information
    """
    bike_df = pd.read_csv("bike_merge_df.csv", low_memory=False)
    bike_df_hypo3 = pd.read_csv("bike_merge_df.csv")
    covid_df = pd.read_csv("covid_merge_df.csv", low_memory=False)
    weather_df = pd.read_csv("weather_merge_df.csv", low_memory=False)

    return bike_df, covid_df, weather_df, bike_df_hypo3


def process_df_hypo1(bk_df: pd.DataFrame, w_df: pd.DataFrame):
    """
    This function is to process the dataframe through changing column names,
    grouping by 'Year-Month' columns and 'names', calculating the total cases and total number of rides
    :param bk_df: a dataframe contains the shared bike information
    :param w_df: a dataframe contains the weather information
    :return: a processed and grouped dataframe of bike and covid
    >>> bike_doctest_df = pd.DataFrame({'ride_id': [819741, 819742, 819743],'started_at': ['2021-06-16 06:41', '2021-06-01 06:39', '2021-06-21 06:42'], 'ended_at': ['2021-06-21 06:49', '2021-06-01 06:48', '2021-06-12 06:51'], 'start_lat': ['38.89696', '38.88548253', '38.9055785'], 'start_lng': ['38.89696', '38.88548253', '38.9055785'],'end_lat': ['38.876751', '-77.000736', '38.876751'], 'end_lng': ['-77.000736', '38.88044','-77.025236'],'member_casual': ['casual', 'member','member'], 'dist': ['0.82', '0.33', '0.79'], 'tripduration': ['2625', '7051', '1632'],'name': ['capital', 'divvy', 'blue']})
    >>> weather_doctest_df = pd.DataFrame({'Unnamed: 0': ['1', '2', '99'], 'name': ['boston', 'chicago', 'New york'],'date': ['3/2/21', '4/5/21', '1/1/22'],'weather': ['snow', 'wind', 'partly-cloudy-day']})
    >>> bike_doctest_df, weather_doctest_df = process_df_hypo1(bike_doctest_df, weather_doctest_df)
    >>> bike_doctest_df['name']
    0           Chicago
    1    Washington D.C
    2            Boston
    Name: name, dtype: object
    >>> weather_doctest_df['weather']
    date
    2022-01-01    partly-cloudy-day
    2021-03-02                 snow
    2021-04-05                 wind
    Name: weather, dtype: object
    """
    # process bike df
    bk_df['name'] = bk_df['name'].replace(['capital', 'blue', 'divvy', 'bay', 'citi'],
                                          ['Washington D.C', 'Boston', 'Chicago', 'SFO', 'NYC'])
    bk_df['Year-Month'] = bk_df['started_at'].str[:10]

    # group by 'Year-Month' and 'Bike Company name'
    # calculate the total rides cases of each bike company in each month
    bk_df_grouped = bk_df.groupby(['Year-Month', 'name'], as_index=False)['ride_id'].count()
    bk_df_grouped = bk_df_grouped.rename(columns={'ride_id': 'Rides Count'})

    # process weather df
    # drop useless column (origin index) after read from csv file: 'Unamed: 0'
    weather_df = w_df.drop(columns='Unnamed: 0')
    weather_df_grouped = weather_df.groupby(['date', 'name'], as_index=False)['weather'].sum()
    weather_df_grouped['date'] = pd.to_datetime(weather_df_grouped['date'])
    weather_df_grouped = weather_df_grouped.set_index('date', drop=True)

    return bk_df_grouped, weather_df_grouped


def process_df_hypo2(bk_df: pd.DataFrame, cov_df: pd.DataFrame):
    """
    This function is to process the dataframe through changing column names,
    grouping by 'Year-Month' columns and 'names', calculating the total cases and total number of rides
    :param bk_df: a dataframe contains the shared bike information
    :param cov_df: a dataframe contains the covid information
    :return: a processed and grouped dataframe of bike and covid
    >>> bike_doctest_df = pd.DataFrame({'ride_id': [819741, 819742, 819743],'started_at': ['2021-06-16 06:41', '2021-06-01 06:39', '2021-06-21 06:42'], 'ended_at': ['2021-06-21 06:49', '2021-06-01 06:48', '2021-06-12 06:51'], 'start_lat': ['38.89696', '38.88548253', '38.9055785'], 'start_lng': ['38.89696', '38.88548253', '38.9055785'],'end_lat': ['38.876751', '-77.000736', '38.876751'], 'end_lng': ['-77.000736', '38.88044','-77.025236'],'member_casual': ['casual', 'member','member'], 'dist': ['0.82', '0.33', '0.79'], 'tripduration': ['2625', '7051', '1632'],'name': ['capital', 'divvy', 'blue']})
    >>> covid_doctest_df = pd.DataFrame({'Date': ['2021-06-02', '2021-04-16', '2022-06-16'], 'Cases': ['5', '4', '89'], 'name': ['BOS covid', 'NYC covid', 'CHI covid']})
    >>> bike_doctest_df, covid_doctest_df = process_df_hypo2(bike_doctest_df, covid_doctest_df)
    >>> bike_doctest_df['name']
    0            Boston
    1           Chicago
    2    Washington D.C
    Name: name, dtype: object
    >>> covid_doctest_df['name']
    0       NYC
    1    Boston
    Name: name, dtype: object
    """
    # process bike_df

    bk_df['name'] = bk_df['name'].replace(['capital', 'blue', 'divvy', 'bay', 'citi'],
                                          ['Washington D.C', 'Boston', 'Chicago', 'SFO', 'NYC'])
    # sort by date to let the dataframe better looks better
    bike_df_sorted = bk_df.sort_values('started_at')
    # extract the 'Year-Month' as a new column
    bike_df_sorted['Year-Month'] = bike_df_sorted['started_at'].str[:7]

    # group by 'Year-Month' and 'Bike Company name'
    # calculate the total rides cases of each bike company in each month
    bk_df_grouped = bike_df_sorted.groupby(['Year-Month', 'name'], as_index=False)['ride_id'].count()
    bk_df_grouped = bk_df_grouped.rename(columns={'ride_id': 'Rides Count'})
    # to keep the same time period with the covid data because Boston covid data doesn't contain data in 2022-03
    bk_df_grouped = bk_df_grouped.loc[bk_df_grouped['Year-Month'] < '2022-03']

    # process covid_df

    covid_df = cov_df.sort_values('Date')
    # extract the 'Year-Month' as a new column
    covid_df['Year-Month'] = covid_df['Date'].str[:7]
    # group by 'Year-Month' and 'city name' and calculate the total cases of each city in each month
    covid_df_grouped = covid_df.groupby(['Year-Month', 'name'], as_index=False)['Cases'].sum()
    covid_df_grouped['name'] = covid_df_grouped['name'].replace(
        ['BOS covid', 'NYC covid', 'CHI covid', 'SFO covid', 'WAS covid'],
        ['Boston', 'NYC', 'Chicago', 'SFO', 'Washington D.C'])

    # because covid data is from 2020 to 2022, so we need to extract the same period with the bike data
    covid_df_grouped = covid_df_grouped.loc['2021-03' <= covid_df_grouped['Year-Month']]
    # because Washington D.C official covid data doesn't contain data in 2022-03, so I have to drop other cities' data
    # in 2022-03, therefore, we can do the parallel analysis and comparison.
    covid_df_grouped = covid_df_grouped.loc[covid_df_grouped['Year-Month'] < '2022-03']
    # reset index and avoid the origin index column
    covid_df_grouped = covid_df_grouped.reset_index(drop=True)

    return bk_df_grouped, covid_df_grouped


def bike_rides_overall_analysis_in_quarter(bk_df: pd.DataFrame):
    """
    This function is to draw bar plot to analyze total rides in each city quarterly
    :param bk_df: the processed data frame contains bike information
    :return: a bar plot
    """
    # used for bar plot color
    color_map = ['lightskyblue', 'pink', 'lavender', 'lightsteelblue', 'aquamarine']
    bk_df['Year-Month'] = pd.to_datetime(bk_df['Year-Month'])
    bk_df_temp = bk_df.set_index('Year-Month', drop=True)
    bk_df_temp = bk_df_temp.groupby(['name'], as_index=False).resample('Q')['Rides Count'].sum()

    bk_df_temp.plot(x='name', kind='bar', figsize=(10, 5), title='Rides Usage Between cities (In Quarter)',
                    rot=0, color=color_map)
    plt.legend(['2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4', '2022-Q1'])
    plt.xlabel('Cities')
    plt.ylabel('Rides Count')
    plt.show()


def city_weather_comparison_analysis(w_df: pd.DataFrame):
    """
    This function is to draw bar plot to analyze the relationship between weather and ride usage in each city quarterly
    :param w_df: the processed data frame contains weather information
    :return: a bar plot of each city
    """
    # used for bar plot color
    color_map = ['lightskyblue', 'pink', 'lavender', 'lightsteelblue', 'aquamarine', 'palegreen']

    w_df_grouped = w_df.groupby(['weather', 'name']).resample('Q')['weather'].count()
    w_df_grouped.index.get_level_values('weather')
    df1 = w_df_grouped.unstack(level=1)

    df1['New york'].unstack(level=0).plot(kind='bar', figsize=(20, 8), rot=0, title='New York', color=color_map)
    df1['Washton D.C.'].unstack(level=0).plot(kind='bar', figsize=(20, 8), rot=0, title='Washington D.C',
                                              color=color_map)
    df1['boston'].unstack(level=0).plot(kind='bar', figsize=(20, 8), rot=0, title='Boston', color=color_map)
    df1['chicago'].unstack(level=0).plot(kind='bar', figsize=(20, 8), rot=0, title='Chicago', color=color_map)
    df1['san francisco'].unstack(level=0).plot(kind='bar', figsize=(20, 8), rot=0, title='San Francisco',
                                               color=color_map)

    plt.show()


def plot_q3_weather_bike_analysis(bk_df: pd.DataFrame, w_df: pd.DataFrame):
    """
    This function is to analyze whether the usage of shared bike will be affected by the daily weather in Q3
    :param bk_df: a dataframe contains the shared bike information
    :param w_df: a dataframe contains the weather information
    :return:
    """
    color_map = ['lightskyblue', 'pink', 'lavender', 'lightsteelblue', 'aquamarine', 'palegreen']
    bk_df['Year-Month'] = pd.to_datetime(bk_df['Year-Month'])
    bk_df_temp = bk_df.set_index('Year-Month', drop=True)

    # slice the data frame to get data from period 2021-07 to 2021-09
    w_df_q3 = w_df['2021-07':'2021-09']
    bk_df_q3 = bk_df_temp['2021-07':'2021-09']

    w_df_q3['name'] = w_df_q3['name'].replace(['New york', 'Washton D.C.', 'boston', 'chicago', 'san francisco'],
                                              ['NYC', 'Washington D.C', 'Boston', 'Chicago', 'SFO'])
    # merge dataframe by the time and city name column
    df_combine_q3 = pd.merge(bk_df_q3, w_df_q3, left_on=['Year-Month', 'name'], right_on=['date', 'name'], how='inner')

    df_q3 = df_combine_q3.groupby(['name', 'weather'])['Rides Count'].sum()
    df_q3.unstack(level=-1).plot(kind='bar', rot=0, figsize=(12, 5), title='Ride Usage in Q3 of each city',
                                 color=color_map)
    plt.xlabel('Cities')
    plt.ylabel('Rides Count')
    plt.show()


def implement_general_line_plot(city_bike_df: pd.DataFrame, city_covid_df: pd.DataFrame, n: str):
    """
    This function is to draw line plots of each city.
    These plots contain two lines. The blue line represents number of total rides in this city and
    the orange line represents the number of total covid cases in this city through 2021-03 to 2022-03
    :param city_bike_df: the processed and grouped bike dataframe
    :param city_covid_df: the processed and grouped covid dataframe
    :param n: the city name
    :return: the line plots
    """
    ax = city_bike_df.plot(x='Year-Month', y='Rides Count', kind='line', figsize=(10, 5), title=n)
    city_covid_df.plot(x='Year-Month', y='Cases', kind='line', figsize=(10, 5), title=n, ax=ax)
    plt.show()


def correlation_analysis(df_com: pd.DataFrame, n: str):
    """
    This function is to analyze Correlation Coefficients between each city's covid cases and its total bike rides
    :param df_com: one dataframe contains the combination of bike information and covid cases data
    :param n: the city name
    :return: correlation coefficients
    """
    print(n)
    print(df_com.corr())
    print('\n')


def scatter_plot_analysis(df_com: pd.DataFrame, n: str):
    """
    This function is to use scatter plot to see whether there is a relationship or correlation between
    each city's covid cases and its bike rides
    :param df_com: one dataframe contains the combination of bike information and covid cases data
    :param n: city name
    :return: scatter plots
    """
    plt.figure(figsize=(8, 5))
    plt.scatter(df_com['Cases'], df_com['Rides Count'])
    plt.title(n)
    plt.xlabel('Covid Cases')
    plt.ylabel('Total Rides')
    if n == 'Boston':
        plt.xticks(ticks=np.arange(0, df_com['Cases'].max(), 120000))
        plt.yticks(ticks=np.arange(0, df_com['Rides Count'].max(), 70000))
    elif n == 'NYC':
        plt.xticks(ticks=np.arange(0, df_com['Cases'].max(), 80000))
        plt.yticks(ticks=np.arange(0, df_com['Rides Count'].max(), 15000))
    elif n == 'Chicago':
        plt.xticks(ticks=np.arange(0, df_com['Cases'].max(), 18000))
        plt.yticks(ticks=np.arange(0, df_com['Rides Count'].max(), 120000))
    elif n == 'SFO':
        plt.xticks(ticks=np.arange(0, df_com['Cases'].max(), 7000))
        plt.yticks(ticks=np.arange(0, df_com['Rides Count'].max(), 35000))
    elif n == 'Washington D.C':
        plt.xticks(ticks=np.arange(0, df_com['Cases'].max(), 400000))
        plt.yticks(ticks=np.arange(0, df_com['Rides Count'].max(), 50000))


def analyze_df_for_each_city(b_df_grouped: pd.DataFrame, c_df_grouped: pd.DataFrame):
    """
    This is the main function. Iterate through a city name list and execute the line plot and scatter plot function and
    display the correlation coefficients and then, executes a linear regression function
    :param b_df_grouped: the processed and grouped dataframe of bike information
    :param c_df_grouped: the processed and grouped dataframe of covid information
    :return: the line plots, the scatter plots, the results of linear regression
    """
    for name in city_names:
        city_bike_df = b_df_grouped[b_df_grouped['name'] == name]
        city_covid_df = c_df_grouped[c_df_grouped['name'] == name]

        df_combine = pd.concat([city_bike_df, city_covid_df['Cases']], axis=1)
        df_combine = df_combine.fillna(0)
        df_combine['Cases'] = df_combine['Cases'].astype(int)
        df_combine.reset_index(drop=True)

        implement_general_line_plot(city_bike_df, city_covid_df, name)
        correlation_analysis(df_combine, name)
        scatter_plot_analysis(df_combine, name)

    plt.show()


def liner_regression_analysis(city_bike_df: pd.DataFrame, city_covid_df: pd.DataFrame, n: str):
    """
    This function is to use linear regression to see whether the correlation coefficients of Washington D.C is believable
    :param city_bike_df: the processed and grouped dataframe of bike information
    :param city_covid_df: the processed and grouped dataframe of covid information
    :param n: city name
    :return: the regression results of R-square, p-value and its fitted-line plot
    """
    was_bike_df = city_bike_df[city_bike_df['name'] == n]
    was_covid_df = city_covid_df[city_covid_df['name'] == n]
    was_df_combine = pd.concat([was_bike_df, was_covid_df['Cases']], axis=1)
    was_df_combine.reset_index(drop=True)
    was_df_combine = was_df_combine.fillna(0)
    was_df_combine['Cases'] = was_df_combine['Cases'].astype(int)
    x = was_df_combine['Cases'].values.tolist()
    y = was_df_combine['Rides Count'].values.tolist()
    was_lr_model = stats.linregress(x, y)
    print(n)
    print(f"R-squared: {was_lr_model.rvalue ** 2:.6f}")
    print(f"P-value: {was_lr_model.pvalue}")

    plt.figure(figsize=(8, 5))
    plt.plot(x, y, 'o', label='original data')
    plt.plot(x, was_lr_model.intercept + was_lr_model.slope * np.asarray(x), 'r', label='fitted line')
    plt.title(n)
    plt.xlabel('Covid Cases')
    plt.ylabel('Total Rides')
    plt.legend()
    plt.show()


def get_city_usertype(bikes: pd.DataFrame, shareBikeName: str, isMember: bool) -> pd.DataFrame:
    """
    based on different user type(member, causal) to select different data
    :param bikes: pandas data frame
    :param shareBikeName: a dtring
    :param isMember: boolean type
    :return: a selevted data frame

    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52',\
    '2021-03-21 17:12:05', '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01',\
    '2021-03-16 17:06:00','2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25',\
    '2021-03-21 17:14:39', '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581,\
    38.8840581, 38.8840581, 38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852,\
     -76.9863852, -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581,\
     38.8840581, 38.8840581, 38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852,\
     -76.9863852, -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer',\
     'Subscriber', 'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e,\
     'end_lat' : f, 'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> get_city_usertype(data, 'blue', True)
                ride_id           started_at  ... tripduration  name
    4  041B42F011BB5CCE  2021-03-31 12:49:33  ...          164  blue
    6  52C41328F35B6304  2021-03-09 18:08:52  ...          153  blue
    8  8F0D1EC683414EB5  2021-03-20 18:15:06  ...          415  blue
    <BLANKLINE>
    [3 rows x 11 columns]
    >>> get_city_usertype(data, 'blue', False)
                ride_id           started_at  ... tripduration  name
    5  C8093E7330B2CCC5  2021-03-29 17:33:55  ...          150  blue
    7  43BBD64DAF992E35  2021-03-21 17:12:05  ...          154  blue
    9  2915024C2F78F293  2021-03-30 18:43:49  ...          796  blue
    <BLANKLINE>
    [3 rows x 11 columns]
    >>> get_city_usertype(data, 'capital', False)
                ride_id           started_at  ... tripduration     name
    1  7718672ECB745D5B  2021-03-12 16:37:17  ...         1271  capital
    3  6C0C775AC0888E55  2021-03-16 17:01:00  ...          300  capital
    <BLANKLINE>
    [2 rows x 11 columns]
    """
    #
    city = bikes[bikes['name'] == shareBikeName]
    if shareBikeName != 'blue':
        if isMember:
            return city[city['member_casual'] == 'member']
        else:
            return city[city['member_casual'] == 'casual']
    else:
        if isMember:
            return city[city['member_casual'] == 'Subscriber']
        else:
            return city[city['member_casual'] == 'Customer']


def get_usertype_count_ym(member: pd.DataFrame) -> list:
    """
    group by dataframe based on year and month
    :param member: a selected member pandas dataframe
    :return: group by(year, month) result

    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52', '2021-03-21 17:12:05',\
    '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01', '2021-03-16 17:06:00',\
    '2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25', '2021-03-21 17:14:39',\
    '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer', 'Subscriber',\
    'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e, 'end_lat' : f,\
    'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> get_usertype_count_ym(data)
    [10]
    """
    member.index = pd.to_datetime(member['started_at'])
    member_ym_count = member.groupby([member.index.year, member.index.month]).count()
    member_ym_count_value = member_ym_count['member_casual'].tolist()

    return member_ym_count_value


def pic_stacked_column_charts(x1Lable: str, x2Lable: str, x1Date, x2Date, title: str):
    """
    draw the stacked_column_charts
    :param x1Lable: 'member' or 'casual'
    :param x2Lable: 'casual' or 'member'
    :param x1Date: Corresponding data with x1
    :param x2Date: Corresponding data with x2
    :param title: the string that wants to show on the graph
    """
    month = ['2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10', \
             '2021-11', '2021-12', '2022-01', '2022-02', '2022-03']
    data = {
        x1Lable: x1Date,
        x2Lable: x2Date
    }
    df = pd.DataFrame(data, index=month)
    df.plot(kind="bar", stacked=True)
    plt.legend(loc="lower left", bbox_to_anchor=(0.75, 1.0))
    plt.title(title)
    plt.show()


def draw_member(bikes: pd.DataFrame):
    """
    Draw the first pictures in hypo3
    :param bikes: a dataframe contain all data
    """
    list_bikes = ['capital', 'divvy', 'bay', 'citi', 'blue']
    list_cities = ['Washington D.C', 'Chicago', 'San Francisco',
                   'New York city', 'Boston']
    count = 0
    # print(Chicago_casual_ym_count)
    # pic_stacked_column_charts('member', 'casual', Chicago_member_ym_count, Chicago_casual_ym_count, 'Boston')
    for i in list_bikes:
        member = get_city_usertype(bikes, i, True)
        casual = get_city_usertype(bikes, i, False)
        member_ym_count = get_usertype_count_ym(member)
        casual_ym_count = get_usertype_count_ym(casual)
        pic_stacked_column_charts('member', 'casual', member_ym_count, casual_ym_count, list_cities[count])
        count += 1


def get_dist_dur(bikes: pd.DataFrame) -> pd.DataFrame:
    """
    select data that contain trip duration, distance and convert trip duration from second to minutes
    :param bikes: a whole data set
    :return: a selected data sets
    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52', '2021-03-21 17:12:05',\
    '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01', '2021-03-16 17:06:00',\
    '2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25', '2021-03-21 17:14:39',\
    '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer', 'Subscriber',\
    'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e, 'end_lat' : f,\
    'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> get_dist_dur(data)
          name           started_at  dist  tripduration member_casual
    0  capital  2021-03-20 09:46:54  0.77          8.33        member
    1  capital  2021-03-12 16:37:17  3.67         21.18        casual
    2  capital  2021-03-13 12:38:15  1.98         25.77        member
    3  capital  2021-03-16 17:01:00  0.26          5.00        casual
    4     blue  2021-03-31 12:49:33  0.26          2.73    Subscriber
    5     blue  2021-03-29 17:33:55  0.26          2.50      Customer
    6     blue  2021-03-09 18:08:52  0.26          2.55    Subscriber
    7     blue  2021-03-21 17:12:05  0.26          2.57      Customer
    8     blue  2021-03-20 18:15:06  0.81          6.92    Subscriber
    9     blue  2021-03-30 18:43:49  1.24         13.27      Customer
    """
    bike_tripdist = bikes[['name', 'started_at', 'dist', 'tripduration', 'member_casual']]
    bike_tripdist.loc[:, 'tripduration'] = round(bike_tripdist['tripduration'] / 60, 2)
    indexNames = bike_tripdist[(bike_tripdist['dist'] <= 0)].index
    # delete tripduration <=0
    bike_tripdist.drop(indexNames, inplace=True)

    return bike_tripdist


def filter_data(bike_tripdist: pd.DataFrame, shareBikeName: str, dist: int, dur: int, isMember: bool) -> [
    pd.DataFrame, pd.DataFrame]:
    """
    clean data based on trip duration and trip distance and also select data based on analysis needs. Note: based on data
    explore, the dist = 3 and dur = 50 keep all data in a range and show their distribution
    :param bike_tripdist: a dataframe has trip durationa and trip distance
    :param shareBikeName: a string
    :param dist: a int that Less than or equal to the number
    :param dur: a int that Less than or equal to the number
    :param isMember: boolean value
    :return: two dataframe

    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52', '2021-03-21 17:12:05',\
    '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01', '2021-03-16 17:06:00',\
    '2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25', '2021-03-21 17:14:39',\
    '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer', 'Subscriber',\
    'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e, 'end_lat' : f,\
    'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> data2 = get_dist_dur(data)
    >>> filter_data(data2, 'blue', 3, 50, True)
    (   name           started_at  tripduration member_casual
    4  blue  2021-03-31 12:49:33          2.73    Subscriber
    6  blue  2021-03-09 18:08:52          2.55    Subscriber
    8  blue  2021-03-20 18:15:06          6.92    Subscriber,    name           started_at  dist member_casual
    4  blue  2021-03-31 12:49:33  0.26    Subscriber
    6  blue  2021-03-09 18:08:52  0.26    Subscriber
    8  blue  2021-03-20 18:15:06  0.81    Subscriber)
    """

    city = bike_tripdist[bike_tripdist['name'] == shareBikeName]
    city = city[(city['dist'] <= dist) & (city['tripduration'] <= dur) & (city['tripduration'] > 0)]
    city_dis = city[['name', 'started_at', 'dist', 'member_casual']]
    city_dur = city[['name', 'started_at', 'tripduration', 'member_casual']]
    city_dur_f = get_city_usertype(city_dur, shareBikeName, isMember)
    city_dis_f = get_city_usertype(city_dis, shareBikeName, isMember)

    return city_dur_f, city_dis_f


def pic_his_mean(cityDurDis: pd.DataFrame, isDur: bool, title: str) -> float:
    """
    draw the histogram, and return the mean value
    :param cityDurDis:
    :param isDur: a flag
    :param title: a string title
    :return: mean value for a col
    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52', '2021-03-21 17:12:05',\
    '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01', '2021-03-16 17:06:00',\
    '2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25', '2021-03-21 17:14:39',\
    '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer', 'Subscriber',\
    'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e, 'end_lat' : f,\
    'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> data2 = get_dist_dur(data)
    >>> d = filter_data(data2, 'blue', 3, 50, True)
    >>> pic_his_mean(d[0], True, 'duration')
    4.066666666666666
    """
    cityDurDis.plot.hist(alpha=0.5)
    plt.title(title)
    if isDur:
        return cityDurDis['tripduration'].mean()
    else:
        return cityDurDis['dist'].mean()


def get_member_casual_tpdu(bikes: pd.DataFrame, isMember: bool, isDur: bool) -> list:
    """
    filter data by member and casual
    :param bikes: whole dataset
    :param isMember: True or False
    :param isDur: True or False
    :return: rounded mean results

    >>> a = ['8E20F5D0158AF914', '7718672ECB745D5B', 'CB8FD07893C27276', '6C0C775AC0888E55', '041B42F011BB5CCE',\
    'C8093E7330B2CCC5', '52C41328F35B6304', '43BBD64DAF992E35', '8F0D1EC683414EB5', '2915024C2F78F293']
    >>> b = ['2021-03-20 09:46:54', '2021-03-12 16:37:17', '2021-03-13 12:38:15', '2021-03-16 17:01:00',\
    '2021-03-31 12:49:33', '2021-03-29 17:33:55', '2021-03-09 18:08:52', '2021-03-21 17:12:05',\
    '2021-03-20 18:15:06', '2021-03-30 18:43:49']
    >>> c = ['2021-03-20 09:55:14', '2021-03-12 16:58:28', '2021-03-13 13:04:01', '2021-03-16 17:06:00',\
    '2021-03-31 12:52:17', '2021-03-29 17:36:25', '2021-03-09 18:11:25', '2021-03-21 17:14:39',\
    '2021-03-20 18:22:01', '2021-03-30 18:57:05']
    >>> d = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> e = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.994749, -77.003666]
    >>> f = [38.905737, 38.89482116666667, 38.915246, 38.8840581, 38.8840581, 38.8840581, 38.8840581,\
    38.8840581, 38.897274, 38.89967]
    >>> g = [-77.02227, -77.04658983333333, -77.220157, -76.9863852, -76.9863852, -76.9863852,\
    -76.9863852, -76.9863852, -76.994749, -77.003666]
    >>> h = ['member','casual', 'member','casual', 'Subscriber', 'Customer', 'Subscriber',\
    'Customer', 'Subscriber', 'Customer']
    >>> i = [0.77, 3.67, 1.98, 0.26, 0.26, 0.26, 0.26, 0.26, 0.81, 1.24]
    >>> j = [500, 1271, 1546, 300, 164, 150, 153, 154, 415, 796]
    >>> k = ['capital', 'capital', 'capital', 'capital', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    >>> label = {'ride_id' : a,'started_at' : b,'ended_at' : c,'start_lat' : d, 'start_lng' : e, 'end_lat' : f,\
    'end_lng' : g, 'member_casual' : h, 'dist' : i, 'tripduration' : j, 'name' : k}
    >>> data = DataFrame(label)
    >>> get_member_casual_tpdu(data, True, True)
    [17.05, nan, nan, nan, 4.07]
    >>> get_member_casual_tpdu(data, True, False)
    [1.38, nan, nan, nan, 0.44]
    >>> get_member_casual_tpdu(data, False, False)
    [0.26, nan, nan, nan, 0.59]
    >>> get_member_casual_tpdu(data, False, True)
    [5.0, nan, nan, nan, 6.11]

    """

    list_bikes = ['capital', 'divvy', 'bay', 'citi', 'blue']
    list_cities = ['Washington D.C', 'Chicago', 'San Francisco',
                   'New York city', 'Boston']
    count = 0
    trip_duration = []
    for i in list_bikes:
        bike_tripdist = get_dist_dur(bikes)
        td = filter_data(bike_tripdist, i, 3, 50, isMember)
        dur = td[0]
        dist = td[1]
        if isDur and isMember:
            mean = pic_his_mean(dur, isDur, list_cities[count] + " memebr")
            count += 1
            trip_duration.append(round(mean, 2))
        elif isDur is True and isMember is False:
            mean = pic_his_mean(dur, isDur, list_cities[count] + " casual")
            count += 1
            trip_duration.append(round(mean, 2))
        elif isDur is False and isMember is True:
            mean = pic_his_mean(dist, isDur, list_cities[count] + " memebr")
            count += 1
            trip_duration.append(round(mean, 2))
        elif isDur is False and isMember is False:
            mean = pic_his_mean(dist, isDur, list_cities[count] + " casual")
            count += 1
            trip_duration.append(round(mean, 2))
    return trip_duration


def draw_pictures(bikes: pd.DataFrame):
    """
    draw pictures
    :param bikes: whole data set
    """
    cols = ['Washington D.C', 'Chicago', 'San Francisco', 'New York city', 'Boston']
    rows = ['member_trip_duration', 'casual_trip_duration', 'member_distance', 'casual_distance']
    member_trip_duration = get_member_casual_tpdu(bikes, True, True)
    casual_trip_duration = get_member_casual_tpdu(bikes, False, True)
    member_distance = get_member_casual_tpdu(bikes, True, False)
    casual_distance = get_member_casual_tpdu(bikes, False, False)
    text = [member_trip_duration, casual_trip_duration, member_distance, casual_distance]
    plt.figure(figsize=(20, 8))
    tab = plt.table(cellText=text,
                    colLabels=cols,
                    rowLabels=rows,
                    loc='center',
                    cellLoc='center',
                    rowLoc='center')
    tab.scale(1, 2)
    plt.axis('off')


if __name__ == '__main__':
    bike_data_df, covid_data_df, weather_data_df, bike_data_df_hypo3 = loads_bike_covid_data()

    # Hypothesis 1
    bike_data_grouped, weather_data_grouped = process_df_hypo1(bike_data_df, weather_data_df)
    bike_rides_overall_analysis_in_quarter(bike_data_grouped)
    city_weather_comparison_analysis(weather_data_grouped)
    plot_q3_weather_bike_analysis(bike_data_grouped, weather_data_grouped)

    # Hypothesis 2
    bike_data_df_grouped, covid_data_df_grouped = process_df_hypo2(bike_data_df, covid_data_df)
    analyze_df_for_each_city(bike_data_df_grouped, covid_data_df_grouped)
    liner_regression_analysis(bike_data_df_grouped, covid_data_df_grouped, 'Washington D.C')

    # Hypothesis 3
    draw_pictures(bike_data_df_hypo3)
    draw_member(bike_data_df_hypo3)
