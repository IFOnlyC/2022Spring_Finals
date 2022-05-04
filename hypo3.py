from typing import Tuple
import pandas as pd
import matplotlib.pyplot as plt
from pandas.core.frame import DataFrame
import warnings
warnings.filterwarnings("ignore")

def load_data():
    file_path = '/Users/jingwei/LocalDocument/JupyterNotebook/597_finalProject/bike_covid_data/bike_merge_df.csv'
    bikes = pd.read_csv(file_path)
    pd.set_option('display.max_columns', None)
    return bikes


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



def pic_stacked_column_charts(x1Lable:str,x2Lable:str,x1Date,x2Date,title:str):
    """
    draw the stacked_column_charts
    :param x1Lable: 'member' or 'casual'
    :param x2Lable: 'casual' or 'member'
    :param x1Date: Corresponding data with x1
    :param x2Date: Corresponding data with x2
    :param title: the string that wants to show on the graph
    """
    month = ['2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09', '2021-10',\
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
    list_bikes = ['capital','divvy','bay','citi','blue']
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


def pic_his_mean(cityDurDis: pd.DataFrame, isDur: bool, title: str)->float:
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

def get_member_casual_tpdu(bikes: pd.DataFrame,isMember: bool, isDur: bool) -> list:
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

    list_bikes = ['capital','divvy','bay','citi','blue']
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
            mean = pic_his_mean(dur, isDur, list_cities[count]+" memebr")
            count += 1
            trip_duration.append(round(mean,2))
        elif isDur is True and isMember is False:
            mean = pic_his_mean(dur, isDur, list_cities[count]+" casual")
            count += 1
            trip_duration.append(round(mean,2))
        elif isDur is False and isMember is True:
            mean = pic_his_mean(dist, isDur, list_cities[count]+" memebr")
            count += 1
            trip_duration.append(round(mean,2))
        elif isDur is False and isMember is False:
            mean = pic_his_mean(dist, isDur, list_cities[count]+" casual")
            count += 1
            trip_duration.append(round(mean,2))
    return trip_duration

def draw_pictures(bikes: pd.DataFrame):
    """
    draw pictures
    :param bikes: whole data set
    """
    cols = ['Washington D.C', 'Chicago', 'San Francisco', 'New York city', 'Boston']
    rows = ['member_trip_duration', 'casual_trip_duration', 'member_distance', 'casual_distance']
    member_trip_duration = get_member_casual_tpdu(bikes,True, True)
    casual_trip_duration = get_member_casual_tpdu(bikes,False, True)
    member_distance = get_member_casual_tpdu(bikes,True, False)
    casual_distance = get_member_casual_tpdu(bikes,False, False)
    text = [member_trip_duration, casual_trip_duration, member_distance, casual_distance]
    plt.figure(figsize=(20,8))
    tab = plt.table(cellText=text,
              colLabels=cols,
             rowLabels=rows,
              loc='center',
              cellLoc='center',
              rowLoc='center')
    tab.scale(1,2)
    plt.axis('off')


if __name__ == '__main__':
    bikes_data = load_data()
    draw_pictures(bikes_data)
    draw_member(bikes_data)

