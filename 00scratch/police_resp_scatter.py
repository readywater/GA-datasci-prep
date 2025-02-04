from __future__ import division
from collections import Counter, defaultdict
from functools import partial
import math, random, csv
import matplotlib.pyplot as plt
import dateutil.parser as dateparse
import datetime

def mean(x):
    return sum(x)/ len(x)

def median(v):
    """finds the 'middle-most' value of v"""
    n = len(v)
    sorted_v = sorted(v)
    midpoint = n // 2
    
    if n % 2 == 1:
        # if odd, return the middle value
        return sorted_v[midpoint]
    else:
        # if even, return the average of the middle values
        lo = midpoint - 1
        hi = midpoint
        return (sorted_v[lo] + sorted_v[hi]) / 2
        
def quantile(x, p):
    """returns the pth-percentile value in x"""
    p_index = int(p * len(x))
    return sorted(x)[p_index]

def mode(x):
    """returns a list, might be more than one mode"""
    counts = Counter(x)
    max_count = max(counts.values())
    return [x_i for x_i, count in counts.iteritems()
            if count == max_count]

# "range" already means something in Python, so we'll use a different name
def data_range(x):
    return max(x) - min(x)

def de_mean(x):
    """translate x by subtracting its mean (so the result has mean 0)"""
    x_bar = mean(x)
    return [x_i - x_bar for x_i in x]

def variance(x):
    """assumes x has at least two elements"""
    n = len(x)
    deviations = de_mean(x)
    return sum_of_squares(deviations) / (n - 1)
    
def standard_deviation(x):
    return math.sqrt(variance(x))

def interquartile_range(x):
    return quantile(x, 0.75) - quantile(x, 0.25)

#
#
#

def get_time(opened,closed):
    # 05/31/2014 10:48:56 PM %M/%D/%Y %H:%M:%S %p
    delta = dateparse.parse(closed) - dateparse.parse(opened)
    return int(delta.seconds + delta.days*86400)

def count_like(rowName,reader):
    return list(Counter(row[rowName] if row[rowName] is not None else None
        for row in reader).items())

if __name__ == "__main__":
    random.seed()

    data = []

    with open("data/90_Day_Cases_by_Neighborhood.csv", "rb") as f:
        reader = csv.DictReader(f)
        data = [row for row in reader]

    for row in data:
        row["time_to_solve"] = get_time(row["Opened"],row["Closed"]) if row["Status"] is "Closed" else 0

    # print data

    print Counter([x["time_to_solve"] for x in data])

    plt.scatter([x["time_to_solve"] for x in data],[x["time_to_solve"] for x in data],4)
    
    plt.axis([-50, 
        max([x["time_to_solve"] for x in data]), 
        -50, 
        max([x["time_to_solve"] for x in data])
        ])
    
    plt.annotate([x["Category"] for x in data],
             xy=([x["time_to_solve"] for x in data],[x["time_to_solve"] for x in data]),
             xytext=(5, -5), # but slightly offset
             textcoords='offset points')
    plt.title("Crimes")
    plt.xlabel("Time taken for a given case")
    plt.ylabel("Total hours")
    plt.show()