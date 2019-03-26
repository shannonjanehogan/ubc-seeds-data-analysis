import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import unicodecsv as csv

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
keys = cleaned_data[0].keys()
with open('cleaned_data.csv', 'wb') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(cleaned_data)

# Tutorials followed:
# https://pythonfordatascience.org/paired-samples-t-test-python/
# http://pythonfordatascience.org/wilcoxon-sign-ranked-test-python/

print("Pre-cleaned data description\n")
print(culled_data[['item_per_kilo','weight', 'num_contam']].describe())
print("\nCleaned data description\n")
print(cleaned_records[['item_per_kilo_before','item_per_kilo_after']].describe())

cleaned_records[['item_per_kilo_before', 'item_per_kilo_after']].plot(kind='box')
plt.savefig('boxplot_outliers.png')

cleaned_records['item_per_kilo_difference'] = cleaned_records['item_per_kilo_before'] - cleaned_records['item_per_kilo_after']

cleaned_records['item_per_kilo_difference'].plot(kind='hist', title='Item Per Kilo Difference Histogram')
plt.savefig('item_per_kilo_difference_histogram.png')

stats.probplot(cleaned_records['item_per_kilo_difference'], plot=plt)
plt.title('Item Per Kilo Difference Q-Q Plot')
plt.savefig('item_per_kilo_difference_qq_plot.png')

## Decided not to use paired ttest due to data violating the assumption of the ttest
# print(stats.shapiro(cleaned_records['item_per_kilo_difference']))
# print(stats.ttest_rel(cleaned_records['item_per_kilo_before'], cleaned_records['item_per_kilo_after']))

cleaned_records[['item_per_kilo_before','item_per_kilo_after']].describe()
cleaned_records['item_per_kilo_difference'] = cleaned_records['item_per_kilo_before'] - cleaned_records['item_per_kilo_after']
cleaned_records['item_per_kilo_difference'][cleaned_records['item_per_kilo_difference']==0]
print("\n Wilcoxon test on item per kilo difference")
print(stats.wilcoxon(cleaned_records['item_per_kilo_difference']))
print("\n Wilcoxon test on item per kilo before and after")
print(stats.wilcoxon(cleaned_records['item_per_kilo_before'], cleaned_records['item_per_kilo_after']))
