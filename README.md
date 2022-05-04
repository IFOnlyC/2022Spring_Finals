# 2022Spring_Finals
## Final projects
Project Type 3:  Timeline analysis of BikeShare in different cities in the United States

Team Members:

Tianhao Chen (tc30)    Github: IFOnlyC

Jingwei Wang (jw103)  Github: sky1122

HangQing He (hhe16)  Github: mingzhuqiuxiahhq

We choose 5 cities for our analysis. They are New York, Washington D.C, Chicago, San Francisco and Boston.

### Hypothesis 1:
#### Users prefer to use shared bikes in summer rather than spring, autumn and winter.
First, we create a plot of each city's total shared bike usage quarterly.
(Jan-Mar: Q1)
(Apr-Jun: Q2)
(July-Sep: Q3)
(Oct-Dec: Q4)

![bike_trend](https://user-images.githubusercontent.com/63156187/166610955-b7cf3f27-9459-4250-b408-4f2ec010629e.png)

We can see that in each city, the bike usage in Q3 is higher than others. The plots support our hypothesis. Therefore, the usage of shared bikes in Summer is greater than other seasons. But why?
Then we conduct a deeper analysis in daily weather dimension.

![image](https://user-images.githubusercontent.com/63156187/166611294-38575b30-0829-4330-bdaa-6ce1c8b3b52f.png)
![image](https://user-images.githubusercontent.com/63156187/166611296-b02d51a9-92ce-448f-aa3e-cdb49e212761.png)
![image](https://user-images.githubusercontent.com/63156187/166611300-3f7e7e2c-1fd7-4abe-a022-4e879ab201cd.png)
![image](https://user-images.githubusercontent.com/63156187/166611303-0a8e7cc9-2168-498a-b9b1-a786655f9767.png)
![image](https://user-images.githubusercontent.com/63156187/166611305-e0ef57d0-df80-46a6-a24c-1716502d36ca.png)

The plots above are the number of types of daily weather in each city.
We find that the reason why users prefer to use shared bikes in summer is because of the weather because in each city, the proportion of good weather is greater in Q3. However, the proportion of rainy days is also higher in some cities, so we need to do further analysis to figure out that Do people still travel a lot on rainy days? (Further Analysis)

### Hypothesis 2:
#### The effect of COVID-19 pandemic on bike share is greater in eastern cities than middle or western cities in US.
We choose some representitive cities in the eastern, middle, and western areas of the United States.
First, we focus on the overall comparison between each city's total shared-bike rides and their covid cases.

![image](https://user-images.githubusercontent.com/63156187/166604759-370eee6d-9185-4cd4-b261-9e0023894be0.png)
![image](https://user-images.githubusercontent.com/63156187/166606119-d141a16c-1021-41d7-9c68-d3bbfceb8acd.png)
![image](https://user-images.githubusercontent.com/63156187/166606138-fe741e75-6185-4f70-a156-055f5e355b0e.png)
![image](https://user-images.githubusercontent.com/63156187/166606152-ea78feec-e9ca-4373-8110-61a4d03cc954.png)
![image](https://user-images.githubusercontent.com/63156187/166606220-712be286-f577-478b-b079-5bac9bb65c6d.png)

We can see that in the plot of Washington D.C, the trend of bike usage and the trend of covid cases may have a relationship or correlation. For other cities, there is meaningless to do further study on the relationship between these cities' covid cases and the usage of shared bikes. Therefore, we assume a **new Hypothesis** that is In Washington D.C, the covid cases will not affect the usage of shared bikes.
And we decide to use a scatter plot to see the correlations and use correlation coefficients to determine whether there a relationship is.

![image](https://user-images.githubusercontent.com/63156187/166606707-7dc59afa-c00e-4ef1-8ecb-592d01cbe16b.png)
![image](https://user-images.githubusercontent.com/63156187/166606751-e0d36f33-739f-4fa5-9469-8c0a0074e075.png)
![image](https://user-images.githubusercontent.com/63156187/166606781-2f140a99-d4e9-41e5-a745-9c31d098f4f8.png)
![image](https://user-images.githubusercontent.com/63156187/166606814-aa6e4053-ba19-45fd-8a72-1d5305bead97.png)
![image](https://user-images.githubusercontent.com/63156187/166606859-8748df01-830b-4e36-aea3-0dc03b0b8e01.png)

The correlation coefficients are:

|            |   Boston    |      NYC      |      Chicago      |      SFO      |      Washington D.C      |
|------------|:-----------:|--------------:|------------------:|--------------:|-------------------------:|
| Correlation Coefficients |  -0.085123    | -0.360768         | -0.529725     | -0.339701    | -0.814073 |

From the table above, we see that the correlation coefficient in Washington D.C is -0.810473, which means the covid cases have a strong correlation with the usage of the shared bike in Washington D.C. And in Boston, the covid cases have a really weak correlation with the shared bike usage.

Then we use linear regression to demonstrate the correlation.
![image](https://user-images.githubusercontent.com/63156187/166609155-18eb01b4-ee52-4d9d-98c6-3ebc9d757c24.png)

R-squared: 0.662715
P-value: 0.0012688629650304379

From the R-squared value, P-value, and the fitted linear regression plot, we can confirm that the new hypothesis will be rejected and the covid cases will have an impact on the usage of shared bikes in Washington D.C.


### Hypothesis 3:
#### Members prefer using bike share than casual member(non-member) when distance between start and destination is less than 1 miles and trip duration is less than 15 minutes in these cities.

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

***For Trip Duration***

![image](https://user-images.githubusercontent.com/48091236/166536422-1899d1ee-c745-4e48-9c56-a7df16891c5e.png)![image](https://user-images.githubusercontent.com/48091236/166552872-884326cc-8d58-483c-8c85-1ea6f5cf740d.png)

![image](https://user-images.githubusercontent.com/48091236/166552680-c16c7b22-1014-45ef-9b4e-caec2dae4be2.png)![image](https://user-images.githubusercontent.com/48091236/166552748-cc75e6e5-0289-4139-9b01-938a23695530.png)

![image](https://user-images.githubusercontent.com/48091236/166552991-e641dc8c-4de2-4692-a82b-2d33a886974c.png)![image](https://user-images.githubusercontent.com/48091236/166553037-2464f373-dbcd-45b9-8112-38555ba30ef1.png)

![image](https://user-images.githubusercontent.com/48091236/166553072-37792f65-6f56-4a65-a08b-32aad998b3fe.png)![image](https://user-images.githubusercontent.com/48091236/166553142-79e3fd53-1d34-41be-a8b9-9a6c3cccc332.png)

![image](https://user-images.githubusercontent.com/48091236/166553177-a072e6ba-acc5-4ddd-b31d-c16dcaf54434.png)![image](https://user-images.githubusercontent.com/48091236/166553200-9c8b3f4c-591c-4953-a7da-ec53f19b81a9.png)

**overall, the most trip duration is lasting about 20 minutes, and members are more willing to hava a shorter trip compared with casual user.**

***For Trip Distance***

![image](https://user-images.githubusercontent.com/48091236/166566063-c8d3b711-b66c-41ae-8036-347282fe8cee.png)![image](https://user-images.githubusercontent.com/48091236/166566109-36d6b143-9a6a-4da9-a1c8-ab2238677a52.png)
![image](https://user-images.githubusercontent.com/48091236/166566142-f63096cd-8045-489a-b33a-2c062322f75b.png)![image](https://user-images.githubusercontent.com/48091236/166566183-b07fd268-b122-47cb-a0cd-bde2158865e5.png)
![image](https://user-images.githubusercontent.com/48091236/166566226-d25afafe-c481-4880-be6f-7d20ad9eac31.png)![image](https://user-images.githubusercontent.com/48091236/166566262-8bd465c4-82f9-40cf-a4be-93e47e00df33.png)
![image](https://user-images.githubusercontent.com/48091236/166566344-5c4b0d0e-5b73-4ec4-96fd-e21d15780b82.png)![image](https://user-images.githubusercontent.com/48091236/166566381-c877d771-067d-4507-b914-4b8aff247bc9.png)
![image](https://user-images.githubusercontent.com/48091236/166566432-9e42057e-8320-4a70-94da-8dc6bb9b41ce.png)![image](https://user-images.githubusercontent.com/48091236/166566464-30156d39-75ee-4f7a-9f9f-f1a405ffd496.png)

***overall, the distribution bwtween members and casual members for trip Distance is similar.***

Sum up the difference between members and casual users behavior in trip duration and distance, we calculate mean in five different cities.
![image](https://user-images.githubusercontent.com/48091236/166570977-2a9e3ea4-a961-4103-bb09-face98537451.png)

***Conclusion:*** members and casual members have simialr trip distance, but members' trip duration time is lesser than casual users. Members prefer using bike share than casual member(non-member) when trip duration is about 10 minutes in these cities.


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
