# -*- coding: utf-8 -*-
"""IEEE-CIS Fraud Detection_EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TpXDtBAoi8d25n0T6byQGKFLGsz2i16d
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import gc

import warnings
warnings.filterwarnings('ignore')

"""Below Function reduces the accuracy below the required level, therefore the second function is used (Second Function fill na's with -1)"""

def reduce_mem_usage(df, verbose=True):
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    start_mem = df.memory_usage(deep=True).sum() / 1024 ** 2 # just added 
    for col in df.columns:
      col_type = df[col].dtypes
      if col_type in numerics:
          c_min = df[col].min()
          c_max = df[col].max()
          if str(col_type)[:3] == 'int':
               if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                   df[col] = df[col].astype(np.int8)
                   df[col] = df[col].astype(np.int16)
               elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
               elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
               else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)    
    end_mem = df.memory_usage(deep=True).sum() / 1024 ** 2
    percent = 100 * (start_mem - end_mem) / start_mem
    print('Mem. usage decreased from {:5.2f} Mb to {:5.2f} Mb ({:.1f}% reduction)'.format(start_mem, end_mem, percent))
    return df

def reduce_memory_usage(df):
    start_mem_usg = df.memory_usage().sum() / 1024**2 
    print("Memory usage of properties dataframe is :",start_mem_usg," MB")
    NAlist = [] # Keeps track of columns that have missing values filled in. 
    for col in df.columns:
        if df[col].dtype != object:  # Exclude strings            
            # Print current column type
            print("******************************")
            print("Column: ",col)
            print("dtype before: ",df[col].dtype)            
            # make variables for Int, max and min
            IsInt = False
            mx = df[col].max()
            mn = df[col].min()
            print("min for this col: ",mn)
            print("max for this col: ",mx)
            # Integer does not support NA, therefore, NA needs to be filled
            if not np.isfinite(df[col]).all(): 
                NAlist.append(col)
                df[col].fillna(mn-1,inplace=True)  
                   
            # test if column can be converted to an integer
            asint = df[col].fillna(0).astype(np.int64)
            result = (df[col] - asint)
            result = result.sum()
            if result > -0.01 and result < 0.01:
                IsInt = True            
            # Make Integer/unsigned Integer datatypes
            if IsInt:
                if mn >= 0:
                    if mx < 255:
                        df[col] = df[col].astype(np.uint8)
                    elif mx < 65535:
                        df[col] = df[col].astype(np.uint16)
                    elif mx < 4294967295:
                        df[col] = df[col].astype(np.uint32)
                    else:
                        df[col] = df[col].astype(np.uint64)
                else:
                    if mn > np.iinfo(np.int8).min and mx < np.iinfo(np.int8).max:
                        df[col] = df[col].astype(np.int8)
                    elif mn > np.iinfo(np.int16).min and mx < np.iinfo(np.int16).max:
                        df[col] = df[col].astype(np.int16)
                    elif mn > np.iinfo(np.int32).min and mx < np.iinfo(np.int32).max:
                        df[col] = df[col].astype(np.int32)
                    elif mn > np.iinfo(np.int64).min and mx < np.iinfo(np.int64).max:
                        df[col] = df[col].astype(np.int64)    
            # Make float datatypes 32 bit
            else:
                df[col] = df[col].astype(np.float32)
            
            # Print new column type
            print("dtype after: ",df[col].dtype)
            print("******************************")
    # Print final result
    print("___MEMORY USAGE AFTER COMPLETION:___")
    mem_usg = df.memory_usage().sum() / 1024**2 
    print("Memory usage is: ",mem_usg," MB")
    print("This is ",100*mem_usg/start_mem_usg,"% of the initial size")
    return df, NAlist

! gdown 1XOG7Z82IDUBHaJwKxDee1la6uNJ3oHTU

! gdown 1OngX7ISBeZguhlGnOlbAH1FVk9rz75N5

! gdown 153Sx97Jwg5gj9POQr3Gz8PjcjFviNjvY

! gdown 1C0dvs_LlSCAV2gU73jCru1OddlAChqaD

train_tr=pd.read_csv('train_transaction.csv')
train_id=pd.read_csv('train_identity.csv')
test_tr=pd.read_csv('test_transaction.csv')
test_id=pd.read_csv('test_identity.csv')

#train_tr=reduce_mem_usage(train_tr)
#train_id=reduce_mem_usage(train_id)
#test_tr=reduce_mem_usage(test_tr)
#test_id=reduce_mem_usage(test_id)

#train_tr,NAlist=reduce_memory_usage(train_tr)
#train_id,NAlist=reduce_memory_usage(train_id)
#test_tr,NAlist=reduce_memory_usage(test_tr)
#test_id,NAlist=reduce_memory_usage(test_id)

train=train_tr.merge(train_id, on='TransactionID', how='left')
test=test_tr.merge(test_id, on='TransactionID', how='left')

ids_=['id-01','id-02','id-03','id-04','id-05','id-06','id-07','id-08','id-09','id-10','id-11']
ids__=['id_01','id_02','id_03','id_04','id_05','id_06','id_07','id_08','id_09','id_10','id_11']
id=[]
for i in range(12,39):
  id.append('id_{}'.format(i))

ids=ids__+id

id2=[]
for i in range(12,39):
  id2.append('id-{}'.format(i))

ids2=ids_+id2

names=dict(zip(ids2,ids))
test=test.rename(names, axis=1)

del train_tr,train_id,test_tr,test_id

train.shape

test.shape

train.info()

train.describe()

test.info()

test.describe()

"""**Transaction Amount Distribution**"""

sns.set_theme(style="darkgrid")
sns.distplot(train['TransactionAmt'])
plt.title('Train Transaction Amount Distribution');

sns.boxplot(train['TransactionAmt'])
plt.title('Train Transaction Amount Outlier Presentation');

"""*note:
Transaction Amount has Outliers in Train DataSet and is right Skewed*
"""

sns.distplot(test['TransactionAmt'])
plt.title('Test Transaction Amount Distribution');

sns.boxplot(test['TransactionAmt'])
plt.title('Test Transaction Amount Outlier Presentation');

"""*Note: Test Data Set has Outliers and it's distribution is right skewed*"""

df=pd.concat([train, test])
df['TransactionAmt_Outlier']=np.abs(df.TransactionAmt-train.TransactionAmt.mean()) > (3*train.TransactionAmt.std())

train=df.iloc[:len(train)]
test=df.iloc[len(train):].drop('isFraud', axis=1).reset_index(drop=True)

del df

"""**Creating the Time Dimension**"""

train['transaction_day']=np.floor(train['TransactionDT']/86400)
test['transaction_day']=np.floor(test['TransactionDT']/86400)

print('First Day of Train Transactions is :', train['transaction_day'].min())
print('Last Day of Train Transactions is :', train['transaction_day'].max())
print('First Day of Train Transactions is :', test['transaction_day'].min())
print('Last Day of Test Transactions is :', test['transaction_day'].max())

train['transaction_Year']=np.ceil(train['transaction_day']/365)
test['transaction_Year']=np.ceil(test['transaction_day']/365)

train['transaction_DayOfYear']=train['transaction_day'].apply(lambda x:x-365 if x>365 else x)
test['transaction_DayOfYear']=test['transaction_day'].apply(lambda x:x-365 if x>365 else x)

train['transaction_week']=np.ceil(train['transaction_day']/7)
test['transaction_week']=np.ceil(test['transaction_day']/7)

train['transaction_week']=train['transaction_week'].apply(lambda x:x-52 if x>52 else x)
test['transaction_week']=test['transaction_week'].apply(lambda x:x-52 if x>52  else x)

train['transaction_weekDay']=train['transaction_day'].apply(lambda x: 7 if x%7==0 else x%7 )
test['transaction_weekDay']=test['transaction_day'].apply(lambda x: 7 if x%7==0 else x%7 )

"""id_12 to id_38 are categorical features"""

for i in range(12,39):
  print('Train id_{} nunique:'.format(i), train['id_{}'.format(i)].nunique(),' ', 'Train Nan values:', train['id_{}'.format(i)].isna().sum())

for i in range(12,39):
  print('Test id_{} nunique:'.format(i), test['id_{}'.format(i)].nunique(),' ', 'Test Nan values:', test['id_{}'.format(i)].isna().sum())

temp=train.groupby('id_14')['TransactionAmt'].mean().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('id_14')['TransactionAmt'].mean().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(18,5))
sns.barplot(x='id_14', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('Time Zone')
plt.ylabel('mean_TransactionAmt')
plt.title('Time Zone Mean Transaction Amount')
plt.xticks(rotation=90);

del temp

df=pd.concat([train,test])
temp=df.groupby('id_14')['TransactionAmt'].mean().to_frame().reset_index()
plt.figure(figsize=(18,5))
sns.barplot(x='id_14', y='TransactionAmt', data=temp)
plt.xlabel('Time Zone')
plt.ylabel('mean_TransactionAmt')
plt.title('Time Zone Mean Transaction Amount')
plt.xticks(rotation=90);

del temp,df

temp=train.groupby('id_14')['TransactionAmt'].count().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('id_14')['TransactionAmt'].count().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(18,5))
sns.barplot(x='id_14', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('Time Zone')
plt.ylabel('count Transaction')
plt.title('Time Zone Count Transaction')
plt.xticks(rotation=90);

del temp

df=pd.concat([train,test])
temp=df.groupby('id_14')['TransactionAmt'].count().to_frame().reset_index()
plt.figure(figsize=(18,5))
sns.barplot(x='id_14', y='TransactionAmt', data=temp)
plt.xlabel('Time Zone')
plt.ylabel('count_Transaction')
plt.title('Time Zone Count Transaction')
plt.xticks(rotation=90);

del temp,df

train['id_31'].nunique()

train['id_31'].unique()

import re
train['Browser_version']=train['id_31'].astype('str').apply(lambda x: re.findall(r"[-+]?\d*\.\d+|\d+", x))
train['Browser_version']=train['Browser_version'].map(lambda x: np.nan if len(x) == 0 else x[0])

test['Browser_version']=test['id_31'].astype('str').apply(lambda x: re.findall(r"[-+]?\d*\.\d+|\d+", x))
test['Browser_version']=test['Browser_version'].map(lambda x: np.nan if len(x) == 0 else x[0])

train['Browser']=train['id_31'].str.replace('[-+]?\d*\.\d+|\d+', '')
train['Browser']=train['Browser'].str.rstrip()

test['Browser']=test['id_31'].str.replace('[-+]?\d*\.\d+|\d+', '')
test['Browser']=test['Browser'].str.rstrip()

train['Browser'].unique()

df=train['Browser'].value_counts().to_frame().reset_index().rename({'index':'Browser', 'Browser':'Count'}, axis=1)
plt.figure(figsize=(15,5))
sns.barplot(x='Browser',y='Count', data=df)
plt.xticks(rotation=90)

del df
gc.collect()

df=pd.concat([train, test])
df['match_status']=df['id_34'].str.split(':', n=1, expand=True)[1]

train=df.iloc[:len(train)]
test=df.iloc[len(train):].drop('isFraud', axis=1).reset_index(drop=True)

train.drop('id_34', axis=1, inplace=True)
test.drop('id_34', axis=1, inplace=True)

del df
gc.collect()

for id in ids__:
  print(id,'nunique:', train[id].nunique(), ' ', 'Train NaN Values:', train[id].isna().sum())

for id in ids__:
  print('Test',id,'nunique:', test[id].nunique(),' ','Test NaN Values:', test[id].isna().sum())

sns.distplot(train['id_01'], label='Train')
sns.distplot(test['id_01'], label='Test')
plt.title('Train id_01 ditribution')
plt.legend();

"""**Device Type and Device Info**"""

train['DeviceType'].unique()

train['DeviceInfo'].nunique()

test['DeviceInfo'].nunique()

"""*There more unique values for Device Info in Test Set*

**How much of the transactions in Train set are fradulent?**
"""

isFraud=len(train[train['isFraud']==1])
total=len(train)
FraudRatio=isFraud/total*100
print('{:.2f}% of the transactions in train set are Fraud'.format(FraudRatio))

sns.countplot(x='isFraud', data=train)
plt.title('Count of Fradulent Transactions');

"""**Transaction Amount / Day/ Week**"""

sns.set_theme(style="darkgrid")
df=pd.concat([train,test])
temp=df.groupby('transaction_day')['TransactionAmt'].mean().to_frame().reset_index()
sns.lineplot(x='transaction_day', y='TransactionAmt', data=temp)
plt.xlabel('transaction_day')
plt.ylabel('mean_TransactionAmt')
plt.title('daily Mean of Transaction Amount')

del temp,df

sns.set_theme(style="darkgrid")
temp=train.groupby('transaction_week')['TransactionAmt'].mean().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('train_transaction_week')
plt.ylabel('train_mean_TransactionAmt')
plt.title('Train Weekly Mean of Transaction Amount')

del temp

sns.set_theme(style="darkgrid")
temp=train.groupby('transaction_week')['TransactionAmt'].sum().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('train_transaction_week')
plt.ylabel('train_sum_TransactionAmt')
plt.title('Train weekly Sum of Transaction Amount')

del temp

sns.set_theme(style="darkgrid")
temp=train.groupby('transaction_week')['TransactionAmt'].count().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('train_transaction_week')
plt.ylabel('train_Transaction_count')
plt.title('Train weekly Count of Transaction')

del temp

temp=test.groupby('transaction_week')['TransactionAmt'].mean().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('test_transaction_week')
plt.ylabel('test_mean_TransactionAmt')
plt.title('Test Weekly Mean of Transaction Amount')
del temp

temp=test.groupby('transaction_week')['TransactionAmt'].sum().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('test_transaction_week')
plt.ylabel('test_sum_TransactionAmt')
plt.title('Test weekly Sum of Transaction Amount')
del temp

temp=test.groupby('transaction_week')['TransactionAmt'].count().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('test_transaction_week')
plt.ylabel('test_Transaction_count')
del temp

df=pd.concat([train,test])
temp=df.groupby('transaction_week')['TransactionAmt'].mean().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('transaction_week')
plt.ylabel('mean_TransactionAmt')
plt.title('Mean Total Transaction Amount');

del temp,df

df=pd.concat([train,test])
temp=df.groupby('transaction_week')['TransactionAmt'].sum().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('transaction_week')
plt.ylabel('Sum_TransactionAmt')

del temp,df

df=pd.concat([train,test])
temp=df.groupby('transaction_week')['TransactionAmt'].count().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='TransactionAmt', data=temp)
plt.xlabel('transaction_week')
plt.ylabel('Count_Transaction')

del temp,df

"""*Note: There is a drop in mean Transaction amount before week 10 but a peak in number of transactions leading to a peak in total transaction amount*

**Fraud / Week**
"""

temp=train.groupby('transaction_week')['isFraud'].sum().to_frame().reset_index()
sns.lineplot(x='transaction_week', y='isFraud', data=temp)
plt.title('Weekly Fraud Count');

del temp

"""*Note: peak of fraud is between week of 15 and 20*

**Device Type / Transaction/Fraud**
"""

df=pd.concat([train, test])
temp=df.groupby('DeviceType')['TransactionAmt'].sum().to_frame().reset_index()

sns.barplot(x='DeviceType', y='TransactionAmt', data=temp)
plt.title('Transaction Amount by deivce Type');

del df, temp

df=pd.concat([train, test])
temp=df.groupby('DeviceType')['TransactionAmt'].mean().to_frame().reset_index()

sns.barplot(x='DeviceType', y='TransactionAmt', data=temp)
plt.title('Mean Transaction Amount by deivce Type');

del df, temp

temp=train.groupby('DeviceType')['TransactionAmt'].count().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('DeviceType')['TransactionAmt'].count().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(10,5))
sns.barplot(x='DeviceType', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('Device Type')
plt.ylabel('count Transaction')
plt.title('Device Type Count Transaction')
plt.xticks(rotation=90);

del temp

df=pd.concat([train, test])
temp=df.groupby('DeviceType')['TransactionAmt'].count().to_frame().reset_index()

sns.barplot(x='DeviceType', y='TransactionAmt', data=temp)
plt.ylabel('Count_Transaction')
plt.title('Transaction Count by device Type');

del df, temp

temp=train.groupby('DeviceType')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('DeviceType')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='DeviceType', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
sns.barplot(x='DeviceType', y='Fraud_Ratio', data=temp)
plt.ylabel('Device_Fraud_Ratio')
plt.title('Device Fraud Ratio');
del temp, temp2

"""Note: Ratio of Fraud is higher in mobile devices while there is more use of desktop devices

**product Code/Transaction/Fraud**
"""

train['ProductCD'].value_counts()

df=pd.concat([train, test])
temp=df.groupby('ProductCD')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='ProductCD', y='TransactionAmt', data=temp)
plt.ylabel('TransactionAmt')
plt.title('Sum of Transaction Amount for product code');

del df, temp

df=pd.concat([train, test])
temp=df.groupby('ProductCD')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='ProductCD', y='TransactionAmt', data=temp)
plt.ylabel('TransactionAmt')
plt.title('Mean Transaction Amount for product code');

del df, temp

temp=train.groupby('ProductCD')['TransactionAmt'].count().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('ProductCD')['TransactionAmt'].count().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(10,5))
sns.barplot(x='ProductCD', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('ProductCD Type')
plt.ylabel('count Transaction')
plt.title('ProductCD Count Transaction');

del temp

df=pd.concat([train, test])
temp=df.groupby('ProductCD')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='ProductCD', y='TransactionAmt', data=temp)
plt.ylabel('Transaction_Count')
plt.title('Count of Transactions for product code');

del df, temp

temp=train.groupby('ProductCD')['isFraud'].sum().to_frame().reset_index().sort_values(by='isFraud')
temp2=train.groupby('ProductCD')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='ProductCD', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True)
sns.barplot(x='ProductCD', y='Fraud_Ratio', data=temp)
plt.xlabel('ProductCD')
plt.ylabel('ProductCD_Fraud_Ratio')
plt.title('ProductCD Fraud Ratio');
del temp, temp2

"""**Card / Transaction / Fraud**"""

Card_nunique={col:train[col].nunique() for col in train.columns if 'card'in col}

Card_nunique

Card_Missing_train={col:train[col].isna().sum() for col in train.columns if 'card'in col}
Card_Missing_train

Card_Missing_test={col:test[col].isna().sum() for col in test.columns if 'card'in col}
Card_Missing_test

"""*Note: No missing Values in card1*"""

temp1=train[train['isFraud']==1]
temp0=train[train['isFraud']==0]

sns.kdeplot(x='card1', data=temp1, label='Fraud')
sns.kdeplot(x='card1', data=temp0, label='No Fraud')
plt.title('card1 Distribution based on Target')
plt.legend();

train['card4'].value_counts()

train['card6'].value_counts()

df=pd.concat([train, test])
temp=df.groupby('card4')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card4', y='TransactionAmt', data=temp)
plt.xlabel('card')
plt.ylabel('TransactionAmt')
plt.title('Card Transaction_Amount ');

del df, temp

df=pd.concat([train, test])
temp=df.groupby('card4')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card4', y='TransactionAmt', data=temp)
plt.xlabel('card')
plt.ylabel('TransactionAmt')
plt.title('Card Mean Transaction_Amount ');

del df, temp

temp=train.groupby('card4')['TransactionAmt'].count().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('card4')['TransactionAmt'].count().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(10,5))
sns.barplot(x='card4', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('card')
plt.ylabel('count Transaction')
plt.title('card Count Transaction');

del temp

df=pd.concat([train, test])
temp=df.groupby('card4')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card4', y='TransactionAmt', data=temp)
plt.xlabel('card')
plt.ylabel('Transaction_Count')
plt.title('Card Transaction_Count ');

del df, temp

temp=train.groupby('card4')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('card4')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='card4', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
sns.barplot(x='card4', y='Fraud_Ratio', data=temp)
plt.xlabel('card')
plt.ylabel('card_Fraud_Ratio')
plt.title('Card Fraud Ratio');
del temp, temp2

"""*Note: discover has the highest ratio of frauds compared to others*"""

df=pd.concat([train, test])
temp=df.groupby('card6')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card6', y='TransactionAmt', data=temp)
plt.xlabel('card Type')
plt.ylabel('TransactionAmt')
plt.title('Card Type Sum TransactionAmt');

del df, temp

df=pd.concat([train, test])
temp=df.groupby('card6')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card6', y='TransactionAmt', data=temp)
plt.xlabel('card Type')
plt.ylabel('TransactionAmt')
plt.title('Card Type Mean TransactionAmt');

del df, temp

temp=train.groupby('card6')['TransactionAmt'].count().to_frame().reset_index()
temp['train_test']='Tr'
temp2=test.groupby('card6')['TransactionAmt'].count().to_frame().reset_index()
temp2['train_test']='Te'
temp=pd.concat([temp, temp2])
plt.figure(figsize=(10,5))
sns.barplot(x='card6', y='TransactionAmt',hue='train_test', data=temp)
plt.xlabel('card Type')
plt.ylabel('count Transaction')
plt.title('card Type Transaction');

del temp

df=pd.concat([train, test])
temp=df.groupby('card6')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt')

sns.barplot(x='card6', y='TransactionAmt', data=temp)
plt.xlabel('card Type')
plt.ylabel('Transaction_Count')
plt.title('Card Type Transaction Count');

del df, temp

temp=train.groupby('card6')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('card6')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='card6', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
sns.barplot(x='card6', y='Fraud_Ratio', data=temp)
plt.xlabel('card Type')
plt.ylabel('card Type_Fraud_Ratio')
plt.title('Card Type Fraud Ratio');
del temp, temp2

"""*Note: Credit Cards are more prone to Fraud than other card Types*

**Email Domain Transaction / Fraud**
"""

df=pd.concat([train, test])
df['P_emaildomain'].value_counts()

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('P_emaildomain')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='P_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Purchaser emaildomain')
plt.ylabel('TransactionAmt')
plt.title('Purchaser emaildomain Transaction Amount')
plt.xticks(rotation=90);

del df, temp

"""*Note: we have two separate categories which look same: gmail.com and gmail*"""

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('P_emaildomain')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='P_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Purchaser emaildomain')
plt.ylabel('TransactionAmt')
plt.title('Purchaser emaildomain Mean Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('P_emaildomain')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='P_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Purchaser emaildomain')
plt.ylabel('Transaction Count')
plt.title('Purchaser emaildomain Transaction Count')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
temp=train.groupby('P_emaildomain')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('P_emaildomain')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='P_emaildomain', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='P_emaildomain', y='Fraud_Ratio', data=temp)
plt.xlabel('Purchaser emaildomain')
plt.ylabel('Purchaser emaildomain_Fraud_Ratio')
plt.title('Purchaser emaildomain Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

df=pd.concat([train, test])
df['R_emaildomain'].value_counts()

del df
gc.collect()

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('R_emaildomain')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='R_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Receiver emaildomain')
plt.ylabel('TransactionAmt')
plt.title('Receiver emaildomain Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('R_emaildomain')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='R_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Receiver emaildomain')
plt.ylabel('TransactionAmt')
plt.title('Receiver emaildomain Mean Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('R_emaildomain')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='R_emaildomain', y='TransactionAmt', data=temp)
plt.xlabel('Receiver emaildomain')
plt.ylabel('Transaction Count')
plt.title('Receiver emaildomain Transaction Count')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
temp=train.groupby('R_emaildomain')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('R_emaildomain')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='R_emaildomain', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='R_emaildomain', y='Fraud_Ratio', data=temp)
plt.xlabel('Receiver emaildomain')
plt.ylabel('Receiver emaildomain_Fraud_Ratio')
plt.title('Receiver emaildomain Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

"""**OS Transaction/Fraud**"""

train[['OS', 'OS_Version']]=train['id_30'].str.split(n=1,expand=True)
test[['OS', 'OS_Version']]=test['id_30'].str.split(n=1,expand=True)

df=pd.concat([train,test])
df=df[df['DeviceType']=='mobile']

temp=df.groupby('OS')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='OS', y='TransactionAmt', data=temp)
plt.xlabel('Mobile OS')
plt.ylabel('TransactionAmt')
plt.title('Mobile OS Transaction Amount')
plt.xticks(rotation=90);

del df, temp

df=pd.concat([train,test])
df=df[df['DeviceType']=='desktop']

temp=df.groupby('OS')['TransactionAmt'].sum().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='OS', y='TransactionAmt', data=temp)
plt.xlabel('desktop OS')
plt.ylabel('TransactionAmt')
plt.title('Desktop Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(15,5))
temp=train[train['DeviceType']=='mobile'].groupby('OS')['isFraud'].sum().to_frame().reset_index()
temp2=train[train['DeviceType']=='mobile'].groupby('OS')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='OS', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='OS', y='Fraud_Ratio', data=temp)
plt.xlabel('mobile OS')
plt.ylabel('mobile OS_Fraud_Ratio')
plt.title('mobile OS Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

plt.figure(figsize=(15,5))
temp=train[train['DeviceType']=='desktop'].groupby('OS')['isFraud'].sum().to_frame().reset_index()
temp2=train[train['DeviceType']=='desktop'].groupby('OS')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='OS', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='OS', y='Fraud_Ratio', data=temp)
plt.xlabel('Desktop OS')
plt.ylabel('Desktop OS_Fraud_Ratio')
plt.title('Desktop OS Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

"""**Transaction Outlier / Fraud**"""

temp=train.groupby('TransactionAmt_Outlier')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('TransactionAmt_Outlier')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='TransactionAmt_Outlier', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='TransactionAmt_Outlier', y='Fraud_Ratio', data=temp)
plt.xlabel('TransactionAmt_Outlier')
plt.ylabel('TransactionAmt_Outlier_Fraud_Ratio')
plt.title('TransactionAmt_Outlier Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

"""*Note: When a Transaction Amount is an outlier, there is more chance for it to be a fradulent transaction*

**Address / Transaction / Fraud**

addr1 is billing zip code
"""

train['addr1'].nunique()

train['addr1'].isna().sum()

"""addr2 is billing country"""

train['addr2'].nunique()

train['addr2'].isna().sum()

train['addr2']= train['addr2'].map(str)
train['addr1']= train['addr1'].map(str)

test['addr2']= test['addr2'].map(str)
test['addr1']= test['addr1'].map(str)

df=pd.concat([train,test])
df['Transaction_location']=df['addr2']+'_'+df['addr1']

train=df.iloc[:len(train)]
test=df.iloc[len(train):].drop('isFraud', axis=1).reset_index(drop=True)

del df

train['Transaction_location'].nunique()

plt.figure(figsize=(15,5))
df=pd.concat([train, test])
temp=df.groupby('Transaction_location')['TransactionAmt'].sum().to_frame().reset_index()
temp=temp.sort_values(by='TransactionAmt', ascending=False)[:50]
sns.barplot(x='Transaction_location', y='TransactionAmt', data=temp)
plt.xlabel('Transaction_location')
plt.ylabel('TransactionAmt')
plt.title('Transaction_location Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(15,5))
temp=train.groupby('Transaction_location')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('Transaction_location')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='Transaction_location', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='Transaction_location', y='Fraud_Ratio', data=temp[:30])
plt.xlabel('Transaction_location')
plt.ylabel('Transaction_location_Fraud_Ratio')
plt.title('Transaction_location Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

"""**Correlation Among similar columns**"""

def get_redundant_pairs(df):
    '''Get diagonal and lower triangular pairs of correlation matrix'''
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(df, n=5):
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    return au_corr[0:n]

"""**C Columns**"""

C=[]
for i in range(1,15):
  C.append('C{}'.format(i))

for c in C:
  print(c+' Train Unique Values', train[c].nunique())

for c in C:
  print(c+' Train Nan Values', train[c].isna().sum())

sns.set(style="white")
corr = train[C].corr()
mask = np.triu(np.ones_like(corr, dtype=np.bool))
f, ax = plt.subplots(figsize=(18, 10))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
plt.title("C Columns' Correlation Matrix", fontsize=15)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
plt.show()

"""Note: Highly Correlated columns:
C1,C14,C12,C11,C10,C8,C7,C6,C4,C2 /

C9,C5
"""

get_top_abs_correlations(train[C], n=40)

"""**D Columns**"""

D=[]
for i in range(1,16):
  D.append('D{}'.format(i))

print('D unique Values:\n')
for d in D:
  print(d,':', train[d].nunique())

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('D9')['TransactionAmt'].mean().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='D9', y='TransactionAmt', data=temp)
plt.xlabel('Hour')
plt.ylabel('TransactionAmt')
plt.title('Hour Mean Transaction Amount')
plt.xticks(rotation=90);

del df, temp

plt.figure(figsize=(20,5))
df=pd.concat([train, test])
temp=df.groupby('D9')['TransactionAmt'].count().to_frame().reset_index().sort_values(by='TransactionAmt', ascending=False)

sns.barplot(x='D9', y='TransactionAmt', data=temp)
plt.xlabel('Hour')
plt.ylabel('Transaction Count')
plt.title('Hour Count Transaction')
plt.xticks(rotation=90);

del df, temp

temp=train.groupby('D9')['isFraud'].sum().to_frame().reset_index()
temp2=train.groupby('D9')['isFraud'].count().to_frame().reset_index().rename({'isFraud':'Count_Fraud'}, axis=1)
temp=temp.merge(temp2, on='D9', how='left')
temp['Fraud_Ratio']=temp['isFraud']/temp['Count_Fraud']
temp.sort_values(by='Fraud_Ratio', inplace=True, ascending=False)
sns.barplot(x='D9', y='Fraud_Ratio', data=temp)
plt.xlabel('Hour')
plt.ylabel('Hour_Fraud_Ratio')
plt.title('Hour Fraud Ratio')
plt.xticks(rotation=90);
del temp, temp2

def D_plots():
    sns.set_style('whitegrid')
    plt.figure()
    fig, ax = plt.subplots(5,3,figsize=(10,10))
    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=2, 
                    wspace=0.4, 
                    hspace=0.4)
    
    for i in range(15):
      plt.subplot(5,3,i+1)
      sns.scatterplot(x=train['TransactionDT'], y=train[D[i]])
      sns.scatterplot(x=test['TransactionDT'], y=test[D[i]])
      plt.title('D{} VS. Time'.format(i+1), fontsize=12,fontweight='bold');

D_plots()

"""*Note: Almost all the D values have an increasing trend with time, D9 is the Hour of Transaction*"""

sns.set(style="white")
corr = train[D].corr()
mask = np.triu(np.ones_like(corr, dtype=np.bool))
f, ax = plt.subplots(figsize=(18, 10))
cmap = sns.diverging_palette(220, 10, as_cmap=True)
plt.title("D Columns' Correlation Matrix", fontsize=15)
sns.heatmap(corr, mask=mask, cmap=cmap, vmax=.3, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)
plt.show()

get_top_abs_correlations(train[D], n=5)

"""**V Columns**"""

V=[]
for i in range(1,340):
  V.append('V{}'.format(i))

"""**V Columns mean distribution**"""

df=pd.concat([train, test])
df['V_mean']=df[V].mean(axis=1)
sns.distplot(df['V_mean'])

del df

get_top_abs_correlations(train[V], n=100)

"""**M columns** known as match, e.g. such as names on card and address so most of them are True or False / M columns are considered Categorical"""

M_nunique={col:train[col].nunique() for col in train.columns if col.startswith('M')}
M_nunique

M=[]
for i in range(1,10):
  M.append('M{}'.format(i))
print('Train Nan Values')
for m in M:
  print(m ,' : ', train[m].isna().sum())

"""**A function which calculates correlation of one column with other columns**"""

from IPython.core.display import HTML

def h(content):
    display(HTML(content))
def corrs(col, N=None):
    num_vars = [f for f in train.columns if train[f].dtype != 'object']
    trx = train.head(N) if N is not None else train.copy()
    corrs = trx[num_vars].corrwith(trx[col]).reset_index().sort_values(0, ascending=False).reset_index(drop=True).rename({'index':'Column',0:'Correlation with ' + col}, axis=1)
    print('\033[1m'+'Most correlated Columns with',col,':','\033[0m')
    trx = pd.concat([corrs.head(10), corrs.dropna().tail(6)])
    h(trx.to_html(escape=False))

corrs('TransactionDT')

corrs('isFraud')

corrs('TransactionAmt')

corrs('id_01')

corrs('dist1')

corrs('dist2')

train['dist1'].corr(train['isFraud'])

train['dist2'].corr(train['isFraud'])