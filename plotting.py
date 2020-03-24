# -*- coding: utf-8 -*-
"""
Created on Mon Mar 16 13:03:43 2020

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

#plotting    
def my_plotter(ax, datax, datay, param_dict):
    """
    A helper function to make a graph
    Parameters
    ----------
    ax : Axes
        The axes to draw to
    datax : array
       The x data
    datay : array
       The y data
    param_dict : dict
       Dictionary of kwargs to pass to ax.plot
    """
    if param_dict['number'] > 0:
        ax[0].plot(datax, datay[0], label='Cases')
        ax[param_dict['number']].plot(datax, datay[param_dict['number']], label='Deaths')
        for axes in ax:
            axes.legend()
            locator = mdates.AutoDateLocator()
            formatter = mdates.AutoDateFormatter(locator)
            axes.xaxis.set_major_locator(locator)
            axes.xaxis.set_major_formatter(formatter)
            axes.set_yscale(param_dict['scale'])
    else:
        ax.plot(datax, datay[0], label='Cases')
        ax.plot(datax, datay[1], label='Deaths')
        ax.legend()
        locator = mdates.AutoDateLocator()
        formatter = mdates.AutoDateFormatter(locator)
        ax.xaxis.set_major_locator(locator)
        ax.xaxis.set_major_formatter(formatter)
        ax.set_yscale(param_dict['scale'])
    
    return


fig, axs = plt.subplots(1,1+separate, figsize=(40,5))
my_plotter(axs, dates, (casesum, deathsum), {'marker': 'x','number':separate, 'scale':scale})   

# this is an inset axes over the main axes
right_inset_ax = fig.add_axes([.2, .6, .2, .2], facecolor='k')
right_inset_ax.axis('off')
right_inset_ax.table(cellText=[casesum[l-7:l-4],], colLabels=dates[l-7:l-4],loc='centre')

# this is another inset axes over the main axes
left_inset_ax = fig.add_axes([.6, .6, .2, .2], facecolor='k')
left_inset_ax.plot(t[:len(r)], r)
left_inset_ax.set_title('Impulse response')
left_inset_ax.set_xlim(0, 0.2)
left_inset_ax.set_xticks([])
left_inset_ax.set_yticks([])