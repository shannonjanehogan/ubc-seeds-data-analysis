import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

## p values, t value, degrees of freedom
culled_data = pd.read_csv("psych_data.csv")
records = culled_data.to_dict(orient='records')
cleaned_data = []

def cleanData():
    for row in records:
        cleaned_row = {}
        if (row['date'] == "March 4" or row['date'] == "March 5" or row['date'] ==
        "March 6" or row['date'] == "March 7"):
            cleaned_row = {
                'building': row['building'],
                'floor': row['floor'],
                'day_of_week': dateToDay(row['date']),
                'item_per_kilo_before': row['item_per_kilo'],
                'item_per_kilo_after': findAfter(row)
            }
            cleaned_data.append(cleaned_row)

def dateToDay(date):
    if (date == "March 4"):
        return "Monday"
    elif (date == "March 5"):
        return "Tuesday"
    elif (date == "March 6"):
        return "Wednesday"
    else:
        return "Thursday"

def findEquivalentDate(date):
    if (date == "March 4"):
        return "March 18"
    elif (date == "March 5"):
        return "March 19"
    elif (date == "March 6"):
        return "March 20"
    else:
        return "March 21"


def findAfter(before_row):
    equivalent_date = findEquivalentDate(before_row['date'])
    for row in records:
        if (row['date'] == equivalent_date and
        row['floor'] == before_row['floor'] and
        row['building'] == before_row['building']):
            return row['item_per_kilo']

cleanData()
cleaned_records = pd.DataFrame.from_dict(cleaned_data)

print("Pre-cleaned data description\n")
print(culled_data[['item_per_kilo','weight', 'num_contam']].describe())
print("Cleaned data description\n")
print(cleaned_records[['item_per_kilo_before','item_per_kilo_after']].describe())

cleaned_records[['item_per_kilo_before', 'item_per_kilo_after']].plot(kind='box')
plt.savefig('boxplot_outliers.png')

cleaned_records['item_per_kilo_difference'] = cleaned_records['item_per_kilo_before'] - cleaned_records['item_per_kilo_after']

cleaned_records['item_per_kilo_difference'].plot(kind='hist', title='Item Per Kilo Difference Histogram')
plt.savefig('item_per_kilo_difference_histogram.png')

stats.probplot(cleaned_records['item_per_kilo_difference'], plot=plt)
plt.title('Item Per Kilo Difference Q-Q Plot')
plt.savefig('item_per_kilo_difference_qq_plot.png')

print(stats.shapiro(cleaned_records['item_per_kilo_difference']))

print(stats.ttest_rel(cleaned_records['item_per_kilo_before'], cleaned_records['item_per_kilo_after']))
