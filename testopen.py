# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 12:00:40 2020

@author: ropj593
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates
from datetime import datetime

# open data
folder = "csse_covid_19_data\\csse_covid_19_time_series\\"
deathsname = 'time_series_19-covid-Deaths.csv'
casesname = 'time_series_19-covid-Confirmed.csv'

def file_len(fname, delimiter=","):
    firstline = 0
    with open(fname, 'r') as fin:
        for line in fin:
            while firstline == 0:
                l = len(line.split(delimiter))
                headers = [x for x in line.split(delimiter)]
                firstline += 1  
    return l, headers   

l, headers = file_len(folder+casesname)
columns = [x for x in range(4,l)]

cases_array = np.loadtxt(folder + casesname,delimiter=",",skiprows=1,usecols=columns)    
deaths_array = np.loadtxt(folder + deathsname,delimiter=",",skiprows=1,usecols=columns) 
labels_array = np.loadtxt(folder + casesname,dtype=str,delimiter=",",skiprows=1,usecols=(0,1,2,3))

# choose parameters
countryselection = "Australia"
separate = 1 #1 for separate graphs, 0 for combined
scale = "linear" #log or linear

# aggregate country data
rows=set(index[0] for index, value in np.ndenumerate(cases_array) if labels_array[index[0],1]==countryselection)
casesum=cases_array[np.array(list(rows),dtype=int),].sum(0)
deathsum=deaths_array[np.array(list(rows),dtype=int),].sum(0)
dates = [datetime.strptime(x.strip(), '%m/%d/%y') for x in headers[4:l]]

cellText=casesum[l-8:l-5]
print(casesum)
print(cellText)