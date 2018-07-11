import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

import pygrib, os, sys, glob
from netCDF4 import Dataset
from numpy import *
import numpy as np
from pylab import *
import time
from datetime import date, timedelta
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib.mlab import bivariate_normal
from matplotlib.mlab import bivariate_normal
from matplotlib import colors, ticker, cm
from datetime import date, timedelta
from tempfile import TemporaryFile
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import colors, ticker, cm
import matplotlib.lines as mlines






#x = np.arange(5.08,50.800001,2.54)
x = np.arange(5,95.1,5)
linecolor = ['blue', 'green', 'red', 'c', 'gold', 'magenta']
fig1=plt.figure(num=None, figsize=(14,15), dpi=500, facecolor='w', edgecolor='k')
fig1.subplots_adjust(hspace=.2, bottom = 0.2)



ax2 = fig1.add_subplot(321)
plt.gca().set_color_cycle(linecolor)
ax2.plot(x,hitrate[:,0:6],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
blue = mlines.Line2D([], [], color='blue',
                           label='NCAR ENS CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
green = mlines.Line2D([], [], color='green',
                           label='GFS', linewidth = 2,marker = "o", markeredgecolor = 'none')
red = mlines.Line2D([], [], color='red',
                           label='HRRR', linewidth = 2,marker = "o", markeredgecolor = 'none')
cyan = mlines.Line2D([], [], color='c',
                           label='NAM-3km', linewidth = 2,marker = "o", markeredgecolor = 'none')
gold = mlines.Line2D([], [], color='gold',
                           label='SREF ARW CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
magenta = mlines.Line2D([], [], color='magenta',
                           label='SREF NMMB CTL', linewidth = 2,marker = "o", markeredgecolor = 'none')
props = dict(boxstyle='square', facecolor='white', alpha=1)
plt.ylabel('Hit Rate', fontsize = 20)
plt.title('Pacific Ranges', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.19,0.7])
plt.xticks(np.arange(75,96,5))
ax2.set_xticklabels(np.arange(75,96,5), fontsize = 14)
ax2.tick_params(axis='y', labelsize=14)
locx = 30
locy = 30
font = 25
fig1.text(0.129, 0.71, '(a)', fontsize = font)




ax2 = fig1.add_subplot(322)
plt.gca().set_color_cycle(linecolor)
ax2.plot(x,hitrate[:,6:12],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.title('Interior Ranges', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.19,0.7])
plt.xticks(np.arange(5,96,5))
ax2.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax2.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.71, '(b)', fontsize = font)





ax3 = fig1.add_subplot(323, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax3.plot(x,faratio[:,0:6],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.ylabel('False Alarm Ratio', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.8])
plt.xticks(np.arange(5,96,5))
ax3.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax3.tick_params(axis='y', labelsize=14)
fig1.text(0.129, 0.457, '(c)', fontsize = font)



ax3 = fig1.add_subplot(324, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax3.plot(x,faratio[:,6:12],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.xlim([75,95.1])
plt.ylim([0.09,0.8])
plt.xticks(np.arange(5,96,5))
ax3.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax3.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.457, '(d)', fontsize = font)


ax4 = fig1.add_subplot(325, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,ets[:,0:6],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.ylabel('ETS', fontsize = 20)
plt.xlabel('Event Size (Percentile)', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.45])
plt.xticks(np.arange(5,96,5))
ax4.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax4.tick_params(axis='y', labelsize=14)
fig1.text(0.129, 0.213, '(e)', fontsize = font)



ax4 = fig1.add_subplot(326, sharex = ax2)
plt.gca().set_color_cycle(linecolor)
ax4.plot(x,ets[:,6:12],linewidth = 2,marker = "o", markeredgecolor = 'none')
plt.grid(True)
plt.xlabel('Event Size (Percentile)', fontsize = 20)
plt.xlim([75,95.1])
plt.ylim([0.09,0.45])
plt.xticks(np.arange(5,96,5))
plt.xlim([75,95.1])
ax4.set_xticklabels(np.arange(5,96,5), fontsize = 14)
ax4.tick_params(axis='y', labelsize=14)
fig1.text(0.552, 0.213, '(f)', fontsize = font)




plt.legend(handles=[ blue, red, cyan,green, gold, magenta], loc='upper center', bbox_to_anchor=(-0.10, -0.21), 
           ncol=3, fontsize = 18)
plt.savefig("../../../public_html/categorical_scores_percentileforecasts_interp_regional_2016_17.pdf")
