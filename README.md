# 2022Spring_Finals
## Final projects
Project Type 3:  Timeline analysis of BikeShare in different cities in the United States

Team Members:

Tianhao Chen (tc30)    Github: IFOnlyC

Jingwei Wang (jw103)  Github: sky1122

HangQing He (hhe16)  Github: mingzhuqiuxiahhq


### Hypothesis 1:

Users prefer to use shared bicycles in spring and summer rather than autumn and winter.
why? -> weather, holiday, temp


### Hypothesis 2:

The effect of COVID-19 pandemic on bike share is greater by 10% in X ... Y.

以月为单位算trip总数， covid case总数

### Hypothesis 3:
Members prefer using bike share than non-member when distance between start and destination is less than 1 miles and trip duration is less than 15 minutes in these cities.

We will use five cities including **Boston, Washton D.C, Chicago, San Francisco, New York** to test our hypothesis. In these five cities, the bikeshare companies have two category users which are member and casual.
The following pictures display the distrubution of the member and casual users

![image](https://user-images.githubusercontent.com/48091236/166553359-01e048a6-7da2-441d-af0f-652fffd3df27.png)
![image](https://user-images.githubusercontent.com/48091236/166553406-433ff8e4-5327-48cc-bd36-c1495fa0d030.png)
![image](https://user-images.githubusercontent.com/48091236/166553482-75db77a2-57f4-4757-a2fa-cb88b50ad542.png)
![image](https://user-images.githubusercontent.com/48091236/166553541-110c5256-b227-411f-b174-2023381c118f.png)
![image](https://user-images.githubusercontent.com/48091236/166515696-1ef01b14-52d1-47e2-a84c-53d78062825e.png)

Improving the user conversion rate in Boston is hard because the proportion of casual is relatively smaller and stable than in other cities.
The city of Chicago, New York, and Washington D.C have a similar trend. The number of users has fluctuations based on temperature and the proportion of casual users is almost half of their total users.
San Francisco is considered a Mediterranean climate, so the fluctuations are not obvious compared with other cities. The proportion of casual users is almost half of their total users.

To further analysis the trip duration and distance in different cities and user's category, we explore and clear data to keep duration and distance data in a range that show their distribution.

![image](https://user-images.githubusercontent.com/48091236/166536422-1899d1ee-c745-4e48-9c56-a7df16891c5e.png)![image](https://user-images.githubusercontent.com/48091236/166552872-884326cc-8d58-483c-8c85-1ea6f5cf740d.png)

![image](https://user-images.githubusercontent.com/48091236/166552680-c16c7b22-1014-45ef-9b4e-caec2dae4be2.png)![image](https://user-images.githubusercontent.com/48091236/166552748-cc75e6e5-0289-4139-9b01-938a23695530.png)

![image](https://user-images.githubusercontent.com/48091236/166552991-e641dc8c-4de2-4692-a82b-2d33a886974c.png)![image](https://user-images.githubusercontent.com/48091236/166553037-2464f373-dbcd-45b9-8112-38555ba30ef1.png)

![image](https://user-images.githubusercontent.com/48091236/166553072-37792f65-6f56-4a65-a08b-32aad998b3fe.png)![image](https://user-images.githubusercontent.com/48091236/166553142-79e3fd53-1d34-41be-a8b9-9a6c3cccc332.png)

![image](https://user-images.githubusercontent.com/48091236/166553177-a072e6ba-acc5-4ddd-b31d-c16dcaf54434.png)![image](https://user-images.githubusercontent.com/48091236/166553200-9c8b3f4c-591c-4953-a7da-ec53f19b81a9.png)











### DataSets Source:

BayWheel(San Francisco): https://www.lyft.com/bikes/bay-wheels/system-data

Divvy Bikeshare(Chicago): https://data.cityofchicago.org/Transportation/Divvy-Trips/fg6s-gzvg

Citibike(New York city): https://ride.capitalbikeshare.com/system-data

Blue Bike(Boston): https://www.bluebikes.com/system-data

Capital Bikeshare(Washton D.C): https://ride.capitalbikeshare.com/system-data


### Covid-19 Data Source:

NYC: https://github.com/nychealth/coronavirus-data （他们传在了github上)

Washington: https://doh.wa.gov/emergencies/covid-19/data-dashboard#downloads

Boston: https://bphc-dashboard.shinyapps.io/BPHC-dashboard/

SFO: https://sf.gov/data/covid-19-cases-and-deaths

Washington: https://doh.wa.gov/emergencies/covid-19/data-dashboard
