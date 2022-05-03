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

![image](https://user-images.githubusercontent.com/48091236/166519976-66f124a9-538c-43c1-9a45-512cb147b0b9.png)
![image](https://user-images.githubusercontent.com/48091236/166515595-7fc2fa55-5ada-4c83-9979-aa9997d48ed7.png)
![image](https://user-images.githubusercontent.com/48091236/166515634-69a74323-f7f3-484a-81c6-0081b9b62611.png)
![image](https://user-images.githubusercontent.com/48091236/166515666-5d91a386-d64a-432c-bd2c-eba638b58283.png)
![image](https://user-images.githubusercontent.com/48091236/166515696-1ef01b14-52d1-47e2-a84c-53d78062825e.png)

Improving the user conversion rate in Boston is hard because the proportion of casual is relatively smaller and stable than in other cities.
The city of Chicago, New York, and Washington D.C have a similar trend. The number of users has fluctuations based on temperature and the proportion of casual users is almost half of their total users.
San Francisco is considered a Mediterranean climate, so the fluctuations are not obvious compared with other cities. The proportion of casual users is almost half of their total users.

To further analysis the trip duration and distance in different cities and user's category, we explore and clear data to keep duration and distance data in a range that show their distribution.

![image](https://user-images.githubusercontent.com/48091236/166536422-1899d1ee-c745-4e48-9c56-a7df16891c5e.png)![image](https://user-images.githubusercontent.com/48091236/166536848-ff8146ae-e05d-40fb-933d-74a399a7e2ee.png)





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
