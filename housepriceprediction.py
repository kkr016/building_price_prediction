# -*- coding: utf-8 -*-
"""housepriceprediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1CRo7VijuEFV_dITbqzNM0Smjep5Jr2z3
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ast
import os
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
import plotly.express as px

data = pd.read_csv("/content/train-chennai-sale.csv")
data.head()

data.shape

data.info()

data.describe()

data.dtypes

"""#Cleaning of the Raw Data Set"""

data.isnull().sum()

mean_value=data['QS_OVERALL'].mean()
data['QS_OVERALL'].fillna(value=mean_value, inplace=True)

data.QS_OVERALL.isnull().sum()

data['N_BEDROOM'] = data['N_BEDROOM'].replace(np.nan, data.N_BEDROOM.mode().values[0])
data['N_BEDROOM'] = data['N_BEDROOM'].astype('int64')                                 # Converting all float vals to int

data['N_BATHROOM'] = data['N_BATHROOM'].replace(np.nan, data.N_BEDROOM.mode().values[0])
data['N_BATHROOM'] = data['N_BATHROOM'].astype('int64')                                 # Converting all float vals to int

data.isnull().sum()

"""#Column wise EDA"""

data.columns

data.dtypes

"""#Derived_SALES_PRICE

* Creating "Derived_SALES_PRICE" column Using [REG_FEE, COMMIS, SALES_PRICE] columns.
* ***NOTE:*** If you are a customer want to known the final amount you need to include Tax for the purchasing the building, and brokerage if Applicable.

"""

data["Derived_SALES_PRICE"]=data["REG_FEE"]+data["COMMIS"]+data["SALES_PRICE"]
data=data.drop(["REG_FEE", "COMMIS", "SALES_PRICE"], axis=1)
data.shape[1]

corelation=data.corr()

plt.figure(figsize=(10,10))
sns.heatmap(corelation, cbar=True, square= True, fmt='.1f', annot=True, annot_kws={'size':15}, cmap='BuPu')
plt.show()

"""***NOTE:*** This coleration is calculated before the encoding

* There is good corelation in between the Derived_SALES_PRICE with ["INT_SQFT, N_ROOM, Area, N_BEDROOM, BUILDTYPE"]
"""

#sns.pairplot(data, hue="AREA", height=2.5)
#plt.show()

"""**PRT_ID**"""

len(data.PRT_ID.unique()), data.shape

data=data.drop('PRT_ID',axis=1)
data.shape[1]

"""* All the rows were unique in PRT_ID column. It may affect the model. So remove the particular column\feature from the dataset.

**AREA**
"""

data.AREA.unique()

data=data.replace({'AREA':{'Karapakkam':'Karapakkam', 'Karapakam':'Karapakkam'}})
data=data.replace({'AREA':{'Anna Nagar':'Anna Nagar', 'Ana Nagar':'Anna Nagar', 'Ann Nagar':'Anna Nagar'}})
data=data.replace({'AREA':{'Adyar':'Adyar', 'Adyr':'Adyar'}})
data=data.replace({'AREA':{'Velachery':'Velacheri', 'Velchery':'Velacheri'}})
data=data.replace({'AREA':{'Chrompet':'Chromepet', 'Chrompt':'Chromepet', 'Chrmpet':'Chromepet', 'Chormpet':'Chromepet'}})
data=data.replace({'AREA':{'KK Nagar':'K.K. Nagar', 'KKNagar':'K.K. Nagar'}})
data=data.replace({'AREA':{'TNagar':'Thyagaraya Nagar', 'T Nagar':'Thyagaraya Nagar'}})

data.AREA.unique()

plt.figure(figsize=(20,13))
plt.subplot(221)
plt.xticks(rotation=85)
plt.xlabel('Area')
plt.ylabel('Derived_SALES_PRICE')
plt.title('Sales of houses according to Area')
sns.barplot(x=data.AREA,
            y=data.Derived_SALES_PRICE,order=data.groupby('AREA')['Derived_SALES_PRICE'].mean().reset_index().sort_values('Derived_SALES_PRICE',ascending = True)['AREA'])

plt.subplot(222)
sns.histplot(data, x="AREA", binwidth=1, kde=True)
plt.title('Distribution and histogram of the Area')
plt.xticks(rotation=85)
plt.tight_layout()
plt.show()

"""***Insighgts:*** In the fearture area, there is a good linearity in the data points.

***Insighgts:*** Histogram tells the area i.e. "Chromepet" has highest no of buildings sold, followed by "Karapakkam", "K.K. Nagar"...

**2nd highest no of buildings sold at a particular area was "Karapakkam" but compared to bar plot, mean rate of cost of all the buildings in "Karapakkam" is the least value.**

**i.e. "Karapakkam" is the cheaptest area compared to other areas**

"""

data.AREA.value_counts()

"""**INT_SQFT**"""

f1=px.scatter(data, x="INT_SQFT", y="Derived_SALES_PRICE", color="INT_SQFT")
f1.show()

"""***Insights:*** Above plot clearly deliver good linearity between sale price and total square feet of the building.

* Building price is increased when the area (Square feet) of the building.increases

**DIST_MAINROAD**
"""

data.DIST_MAINROAD.describe()

plt.figure(figsize=(20,13))
plt.subplot(221)

sns.scatterplot(data=data, x="DIST_MAINROAD", y="Derived_SALES_PRICE", hue="AREA", sizes=(20, 200))
plt.xticks(rotation=85)
plt.xlabel('DIST_MAINROAD')
plt.ylabel('Derived_SALES_PRICE')
plt.title('DIST_MAINROAD vs Derived_SALES_PRICE')

plt.subplot(222)
sns.histplot(data, x="DIST_MAINROAD", binwidth=10, kde=True, fill= True, color="black")
plt.title('Distribution and Histogram')
plt.xticks(rotation=85)
plt.tight_layout()
plt.show()

"""***Insights:*** there is no linearity in between this feature "DIST_MAINROAD" and target value "Derived_SALES_PRICE".

* so this data set "DIST_MAINROAD" can be removed from the data set.
"""

data=data.drop("DIST_MAINROAD",axis=1)

"""SALE_COND"""

data.SALE_COND.unique()

data.SALE_COND.value_counts()

data.SALE_COND = data.SALE_COND.map({'AbNormal':'Abnormal', 'Family':"Family", 'Partial':"Partial", "Normal Sale":"Normalsale", 
                                       "Ab Normal":"Abnormal", "Partiall":"Partial", "Adj Land":"Adj_land", "PartiaLl":"Partial", "AdjLand":"Adj_land"})

plt.figure(figsize=(20,13))
sns.set_palette('Spectral')
plt.subplot(221)

sns.barplot(x=data.SALE_COND,
            y=data.Derived_SALES_PRICE,order=data.groupby('SALE_COND')['Derived_SALES_PRICE'].mean().reset_index().sort_values('Derived_SALES_PRICE',ascending = True)['SALE_COND'])
plt.xticks(rotation=85)
plt.xlabel('SALE_COND')
plt.ylabel('Derived_SALES_PRICE')
plt.title('SALE_COND vs Derived_SALES_PRICE')

plt.show()

data.groupby("SALE_COND")["Derived_SALES_PRICE"].mean()

"""***NOTE:*** There is a slight linearity in bewteen this feature and target.

***Insigghts:*** This feature Sale codition is may usefull to predict the price of the model. So it can't remove from the data set.
* We have to verify Sale type of the build doesn't affect the cost of the building or not.

PARK_FACIL
"""

data.PARK_FACIL.unique()

data.PARK_FACIL = data.PARK_FACIL.replace({'Noo':"No"})

plt.figure(figsize=(20,13))
sns.set_palette('Spectral')
plt.subplot(221)

sns.barplot(x=data.PARK_FACIL,
            y=data.Derived_SALES_PRICE,order=data.groupby('PARK_FACIL')['Derived_SALES_PRICE'].mean().reset_index().sort_values('Derived_SALES_PRICE')['PARK_FACIL'])
plt.xticks(rotation=85)
plt.xlabel('PARK_FACIL')
plt.ylabel('Derived_SALES_PRICE')
plt.title('PARK_FACIL vs Derived_SALES_PRICE')

plt.subplot(222)
data.PARK_FACIL.value_counts().plot(kind='pie', autopct="%.2f")
plt.title("Percentage of parking available")
plt.tight_layout()
plt.show()

"""***Insights:*** according to pie plot, ~ 50 % of the building were available with **parking facility**.

* rate of mean cost of the all building having the parking facility has higher cost than buildings have no parking facility.

* This feature column has only 2 different value, so encode this feature with binary encoding technique.
"""

data.PARK_FACIL.unique()

"""BUILDTYPE"""

data.BUILDTYPE.unique()

data=data.replace({'BUILDTYPE':{'Commercial':'Commercial', 'Comercial':'Commercial', 'Others':'Others', 'Other':'Others', 'House':'House',}})

plt.figure(figsize=(20,13))
sns.set_palette('gist_earth')
plt.subplot(221)
sns.barplot(x=data.BUILDTYPE,
            y=data.Derived_SALES_PRICE,order=data.groupby('BUILDTYPE')['Derived_SALES_PRICE'].mean().reset_index().sort_values('Derived_SALES_PRICE')['BUILDTYPE'])
plt.xticks(rotation=85)
plt.xlabel('Type Of the Building')
plt.ylabel('Derived_SALES_PRICE')
plt.title('BUILDTYPEL vs Derived_SALES_PRICE')

plt.subplot(222)
explode = (0.02, 0.03, 0.05)
data.BUILDTYPE.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=explode)
plt.ylabel('')
plt.title("Percentage of the building type categort wise")
plt.tight_layout()
plt.show()

"""***Insights:*** This feature build type has categorical data points in the data set.
* Cost wise commercial build are the higher amount followed by other type and house type buildings.
* percentage of building in each building type was ploted using pie plot.
* apprx all the type of building were equally com to sale.
"""

data.BUILDTYPE.unique()

"""UTILITY_AVAIL"""

data.UTILITY_AVAIL.unique()

data=data.replace({'UTILITY_AVAIL':{'All Pub':'AllPub', 'NoSewr ':'NoSewr', 'NoSeWa':'NoSewa'}})

plt.figure(figsize=(20,13))
sns.set_palette('gist_earth')
plt.subplot(221)
sns.barplot(x=data.UTILITY_AVAIL,
            y=data.Derived_SALES_PRICE,order=data.groupby('UTILITY_AVAIL')['Derived_SALES_PRICE'].mean().reset_index().sort_values('Derived_SALES_PRICE')['UTILITY_AVAIL'])
plt.xticks(rotation=85)
plt.xlabel('UTILITY_AVAIL')
plt.ylabel('Derived_SALES_PRICE')
plt.title('UTILITY_AVAIL vs Derived_SALES_PRICE')

plt.subplot(222)
explode = (0.05, 0.05, 0.05,0.03)
data.UTILITY_AVAIL.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=explode)
plt.ylabel('')
plt.title("Percentage of the building type facility wise")
plt.tight_layout()

plt.show()

dict(data.groupby('UTILITY_AVAIL')['Derived_SALES_PRICE'].mean())

"""***Insights:*** There is sight linear increses in the fearture "UTILITY_AVAIL".
* **Note:** there is a slight increase increase in the mean cost of the buildings in the category of "NoSewr" compared to "NoSewa".

* all public facility build has higher sale count compared to other type.

Slight linearity in this feature. So we can encode this feature with lable encoding technique.
"""

data.UTILITY_AVAIL.unique()

"""STREET"""

data.STREET.unique()

data=data.replace({'STREET':{'Paved':'Paved', 'Gravel':'Gravel', 'No Access':'No Access', 'Pavd':'Paved', 'NoAccess':'No Access'}})

plt.figure(figsize=(20,13))
sns.set_palette('gist_earth')
plt.subplot(221)
sns.barplot(x=data.STREET,
            y=data.Derived_SALES_PRICE,order=data.groupby('STREET')['Derived_SALES_PRICE'].sum().reset_index().sort_values('Derived_SALES_PRICE')['STREET'])
plt.xticks(rotation=85)
plt.xlabel('STREET')
plt.ylabel('Derived_SALES_PRICE')
plt.title('STREET vs Derived_SALES_PRICE')

plt.subplot(222)
sns.histplot(data, x="STREET")
plt.title('Histogram for the STREET type')
plt.xticks(rotation=85)
plt.tight_layout()

plt.show()

"""***Insights***: linearity between the feature "STREET" and traget are good.

* approximately 2500 building have paved street and 2000 builds have no good access path.
"""

data.STREET.unique()

"""MZZONE"""

data.MZZONE.unique()

plt.figure(figsize=(20,13))
sns.set_palette('bone')
plt.subplot(221)
sns.barplot(x=data.MZZONE,
            y=data.Derived_SALES_PRICE,order=data.groupby('MZZONE')['Derived_SALES_PRICE'].sum().reset_index().sort_values('Derived_SALES_PRICE')['MZZONE'])
plt.xticks(rotation=85)
plt.xlabel('MZZONE')
plt.ylabel('Derived_SALES_PRICE')
plt.title('ZONE vs Derived_SALES_PRICE')

plt.subplot(222)
sns.histplot(data, x="MZZONE",)
plt.title('Histogram for the MZZONE')
plt.xticks(rotation=85)
plt.tight_layout()

plt.show()

"""***Insights***: as per histogram, the no of buildings located in agricultural and industrial zones very low in sales.

* vice versa residential zone has higher no of building Selling.
"""

data.MZZONE.unique()

"""DATE_BUILD, DATE_SALE"""

data[['DATE_BUILD', "DATE_SALE"]].head()

from dateutil.relativedelta import relativedelta

data['DATE_BUILD'] = pd.to_datetime(data['DATE_BUILD'])
data['DATE_SALE'] = pd.to_datetime(data['DATE_SALE'])

data['AGE'] = [abs(relativedelta(a, b).years) for a, b in zip(data['DATE_BUILD'], data['DATE_SALE'])]
data.AGE.head()

"""1-  Age of the building was derived from the date attributes i.e. [DATE_SALE.DATE_BUILD]

2- So bothe column in the dataset deleted.
"""

plt.figure(figsize=(20,13))
sns.set_palette('bone')
plt.subplot(221)
sns.lineplot(data=data, x="AGE", y="Derived_SALES_PRICE")
plt.xticks(rotation=85)
plt.xlabel('AGE')
plt.ylabel('Derived_SALES_PRICE')
plt.title('AGE of the building vs Derived_SALES_PRICE')

plt.subplot(222)
sns.histplot(data, x="AGE", binwidth=2, kde=True, shrink=.8)
plt.title('Distribution for the AGE of the buildings')
plt.xticks(rotation=85)
plt.tight_layout()

plt.show()

"""***Insights:*** oldest buildings were not very less in no for sales.
* in the range of 2 to 40 years old builings were large came for sales.

* as per line plot, we can see the negative corelation betwwen the feature "AGE" and the target data. Mean cost of the buildings reduces when the age of the building increaeses.
"""

data=data.drop(["DATE_SALE", "DATE_BUILD"], axis=1)

"""There is a slight negative relation in the AGe vs price."""

data.hist(figsize=(20,20),bins=20)
plt.show()

data.columns

"""N_BEDROOM, N_BATHROOM, N_ROOM"""

fig, axes = plt.subplots(1, 3, figsize=(15, 6), sharey=True)
sns.set_palette('afmhot')

sns.barplot(ax=axes[0], x=data.N_BEDROOM, y=data.Derived_SALES_PRICE)
axes[0].set_title("Bedroom vs Derived_SALES_PRICE")

sns.barplot(ax=axes[1], x=data.N_BATHROOM, y=data.Derived_SALES_PRICE)
axes[1].set_title("Bathroom vs Derived_SALES_PRICE")

sns.barplot(ax=axes[2], x=data.N_ROOM, y=data.Derived_SALES_PRICE)
axes[2].set_title("Room vs Derived_SALES_PRICE")

plt.tight_layout()
plt.show()

"""***Insights:*** As per the above bar plots,
* The no of bedroom, bathroom and no of rooms in the buildings increases would give good sales price.
* Total no of room in the buildings increases the cost of the building also increases.
* Buildings with more bathroom were good sales price than least buildings having least bathroom.

QS_BATHROOM, QS_BEDROOM, QS_OVERALL, Derived_SALES_PRICE
"""

plt.figure(figsize=(20,13))
sns.set_palette('flare_r')
plt.subplot(221)
sns.scatterplot(data=data, x="QS_ROOMS", y="Derived_SALES_PRICE")
plt.xticks(rotation=85)
plt.xlabel('QS_ROOMS')
plt.ylabel('Derived_SALES_PRICE')
plt.title('QS_ROOMS vs Derived_SALES_PRICE')

plt.subplot(222)
sns.scatterplot(data=data, x="QS_BEDROOM", y="Derived_SALES_PRICE")
plt.xticks(rotation=85)
plt.xlabel('QS_BEDROOM')
plt.ylabel('Derived_SALES_PRICE')
plt.title('QS_BEDROOM vs Derived_SALES_PRICE')

plt.subplot(223)
sns.scatterplot(data=data, x="QS_BATHROOM", y="Derived_SALES_PRICE")
plt.xticks(rotation=85)
plt.xlabel('QS_BATHROOM')
plt.ylabel('Derived_SALES_PRICE')
plt.title('QS_BATHROOM vs Derived_SALES_PRICE')

plt.subplot(224)
sns.scatterplot(data=data, x="QS_OVERALL", y="Derived_SALES_PRICE")
plt.xticks(rotation=85)
plt.xlabel('QS_OVERALL')
plt.ylabel('Derived_SALES_PRICE')
plt.title('QS_OVERALL vs Derived_SALES_PRICE')

plt.tight_layout()
plt.show()

"""***NOTE:*** The features ['QS_ROOMS', 'QS_BATHROOM', 'QS_BEDROOM', 'QS_OVERALL'] havn't any linearity in between the target datapoints.

* The masked data points have no relation with the target data point. 
* So, the features ['QS_ROOMS', 'QS_BATHROOM', 'QS_BEDROOM', 'QS_OVERALL'] were removed from the data set.
"""

data=data.drop(['QS_ROOMS', 'QS_BATHROOM', 'QS_BEDROOM', 'QS_OVERALL'], axis=1)

"""# Other EDA"""

data.head(1)

figa=px.scatter(data,x="Derived_SALES_PRICE", y="INT_SQFT", size="N_ROOM",color='AREA',hover_name='MZZONE', title="Square feet vs Sales price of the buildings")
figa.show()

sns.set_palette('YlGn')
sns.catplot(x="AREA", y="AGE", hue="MZZONE", col="PARK_FACIL", kind="bar", data=data, ci=None, height=7, aspect=1.5, sharey=False)
plt.xticks(rotation=85)
plt.show()

"""***Insights:*** There are buildings located in K.K. nagar were recent establised buildings followed by, Chrompet, adyar..

* right side plot represents the buildings located in various area and saturation show the type of zone with packing facility in the Building.
* all the area has buildings in the Residential type zone with parking and without parking facility.

***Note:***
* The area Anna nagar, Chrompet, K.K. Nagar, Thyagarayar nagar don't have any buildings in the Industrial and C zones (below code confirm this statement).

* At the same time exccept from above mentioned area i.e. Karapakkam, Adayar, Velacheri were the only areas, buildings located in Agri Zone.
"""

data.AREA[data["MZZONE"]=='I'].value_counts()

data.AREA[data["MZZONE"]=='A'].value_counts()

sns.set_palette('Paired')
sns.catplot(x="AREA", y="Derived_SALES_PRICE", hue="BUILDTYPE", col="STREET", kind="bar", data=data.sort_values("Derived_SALES_PRICE"), ci=None, height=4, aspect=1.5)
plt.xticks(rotation=85)
plt.show()

"""***Insights:***
* In genral, Mean cost of the buildings are highest in Anna nagar followed by Thyagaraya nagar which are commercial Buildings.
* K.K. Nagar buildings are the only buildings completely has good pathway to the main roads, i.e. Paved or gravel pathway
"""

plt.figure(figsize=(20,13))
sns.set_palette('gist_earth')
plt.subplot(431)
data.N_BEDROOM.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=(0.05, 0.05, 0.05,0.03))
plt.ylabel('')
plt.title("Percentage of the No of bedroom")

plt.subplot(432)
explode = (0.05, 0.05)
data.N_BATHROOM.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=explode)
plt.ylabel('')
plt.title("Percentage of the No of bathroom")

plt.subplot(433)
explode = (0.05, 0.05, 0.05,0.03, 0.01)
data.N_ROOM.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=explode)
plt.ylabel('')
plt.title("Percentage of the No of room")
plt.tight_layout()

plt.subplot(434)
explode = (0.05, 0.05, 0.05,0.03)
data.UTILITY_AVAIL.value_counts().plot(kind='pie', autopct='%1.0f%%', explode=explode)
plt.ylabel('')
plt.title("Percentage of the UTILITY_AVAIL")
plt.tight_layout()

plt.show()

"""***Insights:*** 
* No. of bedrooms "4" has less no of buildings.
* 97 % of the buildings has only one bathroom.
* 60 % of the buildings has more than 2 no of room in it.
* 27% of the buildings hhas all public facilities.
"""

sns.set_palette('Paired')
sns.catplot(x="BUILDTYPE", y="N_ROOM", kind="boxen", col="UTILITY_AVAIL", data=data.sort_values("N_ROOM"), height=4, aspect=1.5)
plt.show()

"""***Insights:*** Building without utility feature ELO don't have 6 rooms."""

sns.catplot(x="BUILDTYPE", y="Derived_SALES_PRICE", hue="AREA", kind="violin", split=False, data=data.sort_values("Derived_SALES_PRICE"), height=6, aspect=3)
plt.title('Sale price of the building in type wise')
plt.show()

"""***Insights:*** Anna nagar has the highest mean rate of cost of the building, in all the 3 type of building type.

* Houses start from the raange of 30 lakhs to 1.5 cores appx.
* Commercial buildings start from the raange of 30 lakhs to 2.7 cores appx.
* Other type of  buildings start from the raange of 30 lakhs to 1.7 cores appx.
"""

data.head()

"""# Encode

* Encoding of the binary and ordinal data points are converted using label encoding technique.
* Nominal data points in the data set need one hot encoding technique.

* Data point ['AREA', 'PARK_FACIL', 'SALE_COND','UTILITY_AVAIL', 'STREET', "MZZONE", needs label encoing.
* and, BUILDTYPE feature needs one hot encoding.
"""

data.head()

data = data.replace({'AREA':{'Karapakkam':1,"Adyar":2, "Chromepet":3, "Velacheri":4, "K.K. Nagar":5, "Anna Nagar":6, 'Thyagaraya Nagar':7}})

data.PARK_FACIL = data.PARK_FACIL.map({'Yes':1, 'No':0})

data.SALE_COND = data.SALE_COND.map({"Abnormal":3,"Adj_land":5, "Family":2, "Normalsale":4, "Partial":1})

data=data.replace({'UTILITY_AVAIL':{'ELO':1, 'NoSewa':2, 'NoSewr':3, "AllPub":4}})

data=data.replace({'STREET':{'Gravel':2, 'Paved':3, 'No Access':1}})

data=data.replace({'MZZONE':{'A':1, 'C':2, 'I':3, 'RH':4,'RL':5,'RM':6,}})

from sklearn.preprocessing import LabelEncoder
typee = data.BUILDTYPE
buildtype = pd.get_dummies(typee)
data = pd.concat([data, buildtype],axis=1)
del data['BUILDTYPE']

data.head()

corelation=data.corr()
plt.figure(figsize=(15,10))
sns.heatmap(corelation, cbar=True, square= True, fmt='.1f', annot=True, annot_kws={'size':15}, cmap='Dark2')
plt.show()

"""***Insights:*** 

* the data points [AREA, INT_SQFT,	N_BEDROOM, 	N_ROOM MZZONE, Commercial,	House,	Others] has good coleration amoung the other data points with Derived_SALES_PRICE.

# Train and Test data split
"""

from sklearn.model_selection import train_test_split

# Spliting target and features variables
X = data.drop(['Derived_SALES_PRICE','AREA'], axis = 1)
y = data['Derived_SALES_PRICE']

# Splitting to training and testing data

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size = 0.2, random_state = 7)

X_train.shape, X_test.shape, y_train.shape , y_test.shape

"""# Scalling"""

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
scaler.fit(X_train,y_train)
x_train = scaler.transform(X_train)
x_test = scaler.transform(X_test)

"""##Model

* for continous values of the target data, use regression model.
* this the Supervised learing problem.

#Linear regression
"""

from sklearn.linear_model import LinearRegression

regressor = LinearRegression()
regressor.fit(X_train, y_train)

print("C value:", regressor.intercept_)

print("Co-efficient:", regressor.coef_)

y_pred_train_lr = regressor.predict(X_train)
y_pred_train_lr

Actu_Pred_df_lr = pd.DataFrame({'Actual': y_train, 'Predicted': y_pred_train_lr})
Actu_Pred_df_lr.head()

plt.figure(figsize=(15,4))
sns.kdeplot(data=Actu_Pred_df_lr, x='Actual', label='actual', color = 'red',shade=True)
sns.kdeplot(data=Actu_Pred_df_lr, x='Predicted', label='predicted', color='blue', shade=True)
plt.title("Actual Price Vs Predicted Price")
plt.legend()
plt.show()

"""***Insights:*** the above plot shows how linear regression model predict the sale price of the building.

* Plot show how predict price of the building fits with the actual price. 
"""

from sklearn import metrics 
r2_lr_train=metrics.r2_score(y_train,y_pred_train_lr)
print('R^2- SCORE for train data using LinearRegression:', metrics.r2_score(y_train,y_pred_train_lr))

y_train.shape, y_pred_train_lr.shape

print('MAE:',metrics.mean_absolute_error(y_train, y_pred_train_lr))
print('MSE:',metrics.mean_squared_error(y_train, y_pred_train_lr))

importance = regressor.coef_
# summarize feature importance\

len(importance), importance

coeffcients = pd.DataFrame([X_train.columns,regressor.coef_]).T
coeffcients = coeffcients.rename(columns={0: 'Attribute', 1: 'Coefficients'})
coeffcients

"""# Random forecast"""

from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor

# Create a Random Forest Regressor
randomf = RandomForestRegressor(n_estimators= 100, max_depth =30, max_features='sqrt')

# Train the model using the training sets 
randomf.fit(X_train, y_train)

# Model prediction on train data
y_pred_train_rf = randomf.predict(X_train)

# Model Evaluation
r2_rf_train=metrics.r2_score(y_train, y_pred_train_rf)
print('R^2- SCORE for train data using Random Forest:',metrics.r2_score(y_train, y_pred_train_rf))

Actu_Pred_df_rf = pd.DataFrame({'Actual': y_train, 'Predicted': y_pred_train_rf})
Actu_Pred_df_rf.head()

plt.figure(figsize=(15,4))
sns.kdeplot(data=Actu_Pred_df_rf, x='Actual', label='actual', color = 'red',shade=True)
sns.kdeplot(data=Actu_Pred_df_rf, x='Predicted', label='predicted', color='blue', shade=True)
plt.title("Actual Price Vs Predicted Price")
plt.legend()
plt.show()

"""***Insights:*** the above plot shows how ramndom forest model predict the sale price of the building.

* Plot show how predict price of the building fits with the actual price. 
"""

#Get numerical feature importances
importances = list(randomf.feature_importances_)

# List of tuples with variable and importance
feature_importances = [(feature, round(importance, 2)) for feature, importance in zip(X_train.columns, importances)]

# Sort the feature importances by most important first
feature_importances = sorted(feature_importances, key = lambda x: x[1], reverse = True)

# Print out the feature and importances 
[print('Variable: {:20} Importance: {}'.format(*pair)) for pair in feature_importances];

"""***Insights:***

* INT_SQRT, Commercial type, N_ROOMS, MZZONE, N_BEDROOM< House, OTHER are very importance features in the given data set.

#XG Boost
"""

from xgboost import XGBRegressor
from sklearn.model_selection import cross_val_score
for l in [0.01,0.02,0.03,0.04,0.05,0.1,0.11,0.12,0.13,0.14,0.15,0.2,0.5,0.7,1]:
  xgb = XGBRegressor(learning_rate = l, n_estimators=100, verbosity = 0)
  xgb.fit(X_train,y_train)
  print("Learning rate : ", l, " Train score : ", xgb.score(X_train,y_train), " Cross-Val score : ", np.mean(cross_val_score(xgb, X_train, y_train, cv=10)))

xgb = XGBRegressor(learning_rate = 0.5, n_estimators=100, verbosity=0)
xgb.fit(X_train,y_train)

y_pred_train_xgb = xgb.predict(X_train)

r2_xgb_train=metrics.r2_score(y_train,y_pred_train_xgb)
print('R^2- SCORE for train data using XGBoost', metrics.r2_score(y_train,y_pred_train_xgb))

Actu_Pred_df_xgb = pd.DataFrame({'Actual': y_train, 'Predicted': y_pred_train_xgb})
Actu_Pred_df_xgb.head()

Actu_Pred_df_xgb.describe()

plt.figure(figsize=(15,4))
sns.kdeplot(data=Actu_Pred_df_xgb, x='Actual', label='actual', color = 'red',shade=True)
sns.kdeplot(data=Actu_Pred_df_xgb, x='Predicted', label='predicted', color='blue', shade=True)
plt.title("Actual Price Vs Predicted Price")
plt.legend()
plt.show()

"""***Insights:*** the above plot shows how linear regression model predict the sale price of the building.

* Plot show how predict price of the building fits with the actual price. 

* XGB boost medel shows excellent fit of predict price of the building with thw actual price.
"""

models = pd.DataFrame({'model_name':['LinearRegression','DecissionTree','RandomForest'],'r2_score_train':[r2_lr_train, r2_rf_train, r2_xgb_train]})
models

"""***Insights:***  R^2 value of the 3 different model i.e. 

*   LinearRegression
*   DecissionTree
*   XGBoost

***NOTE:***
* DecissionTree model gives better r^2 value for the train data set.
"""