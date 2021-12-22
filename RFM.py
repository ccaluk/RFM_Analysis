import datetime as dt
import pandas as pd
pd.set_option("display.max_column",None)
pd.set_option('display.float_format', lambda x: '%.5f' % x)



#1

df_ = pd.read_excel("data/online_retail_II.xlsx", sheet_name="Year 2010-2011")
df = df_.copy()
df = df[df["Quantity"] > 0]
df = df[df["Price"] > 0]

#2

df.describe().T

#3

df.isnull().any()
df.isnull().sum()

#4

df.dropna(inplace=True)

#5

df["Description"].nunique()

#6

df["Description"].value_counts()

#7

df.sort_values("Quantity", ascending=False).head()

#8

df = df[~df["Invoice"].str.contains("C",na=False)]

#9

df["TotalPrice"] = df["Quantity"] * df["Price"]



today_date=dt.datetime(2011, 12, 11)


rfm=df.groupby("Customer ID").agg({"InvoiceDate": lambda InvoiceDate : (today_date-InvoiceDate.max()).days,
                                   "Invoice" : lambda Invoice : Invoice.nunique(),
                                   "TotalPrice" : lambda TotalPrice : TotalPrice.sum()})

rfm.columns=["recency","frequency","monetary"]

rfm=rfm[rfm["monetary"] > 0]



rfm["recency_score"]=pd.qcut(rfm["recency"],5,labels=[5,4,3,2,1])

rfm["frequency_score"]= pd.qcut(rfm["frequency"].rank(method="first"),5, labels=[1,2,3,4,5])

rfm["monetary_score"]=pd.qcut(rfm["monetary"],5,labels=[1,2,3,4,5])

rfm["RFM_SCORE"]=(rfm["recency_score"].astype(str)+rfm["frequency_score"].astype(str))



seg_map = {
    r'[1-2][1-2]': 'hibernating',
    r'[1-2][3-4]': 'at_Risk',
    r'[1-2]5': 'cant_loose',
    r'3[1-2]': 'about_to_sleep',
    r'33': 'need_attention',
    r'[3-4][4-5]': 'loyal_customers',
    r'41': 'promising',
    r'51': 'champions',
    r'[4-5][2-3]': 'potential_loyalists',
    r'5[4-5]': 'champions'
}

rfm["segment"]=rfm["RFM_SCORE"].replace(seg_map,regex=True)


rfm.groupby("segment")["recency","frequency","monetary"].agg({"mean","count"})



