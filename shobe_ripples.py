# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 19:39:33 2016

@author: Charlie Shobe

Ripple model: 1-D ripples

INPUTS:
-none required, but user can change all parameters.

OUTPUTS:
-animated plot of ripples evolving over time.
-static plot of ripple topography at different points in time.
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rcParams['font.family'] = 'Arial'
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams['xtick.major.pad']='10'

#########################INITIALIZE

#spatial domain
n_bins = 200 
bin_width = .01 #m
grain_size = 0.0005 #m
grains_per_bin = bin_width / grain_size
bins = np.arange(0, (n_bins * bin_width) + bin_width, bin_width) #x domain

z = 0 #initial flat topography
bin_heights = np.zeros((len(bins)))
bin_heights[:] = 0
impact_angle = 0.176 #dimensionless slope (10 degrees)
min_firing_height = impact_angle * min(bins) #m, will hit left edge of model domain
max_firing_height = impact_angle * (max(bins) + bin_width) #m, will hit right edge of model domain
n_ejected = 10 #grains ejected per impact

n_grains_fired = 25000
plot_every = 500 #plot every x grains

#instantiate plotting stuff
ripple_fig = plt.figure(figsize=(12,8)) #instantiate figure
ripples = plt.subplot(111)
plt.xlabel('Distance [m]')
plt.ylabel('Elevation [m]')
plt.ion()
plt.show()
saved_values = np.zeros((6, len(bin_heights)))
saved_values[0, :] = 0

##########################RUN

it = 0
save_it = 0
for i in range(n_grains_fired + 1):
    it += 1
    firing_height = np.random.uniform(min_firing_height, max_firing_height)
    trajectory_in_y = -0.176 * bins + firing_height #array of y values
    try:
        impact_bin = np.where(trajectory_in_y <= bin_heights)[0][0] #impact bin
    except:
        pass
    bin_heights[impact_bin] -= (grain_size * (n_ejected / grains_per_bin))#(n_ejected * grain_size) / bin_width
    landing_bin = impact_bin + 1
    try:
        bin_heights[landing_bin] += (grain_size * ((n_ejected) / grains_per_bin))
    except IndexError:
        bin_heights[0] += (grain_size * ((n_ejected) / grains_per_bin))
    
    bin_heights[0] = bin_heights[-1] #wrap-around boundary condition
    mean_elev = np.average(bin_heights)
    bin_heights -= mean_elev
    if it % plot_every == 0: #plot stuff
        ripples.clear()
        ripples.plot(bins, bin_heights)
        ripples.set_xlim(0, 2)
        ripples.set_ylim(-0.1, 0.1)
        ripples.text(8, 0.05, 'Impacts [#]: %.1f' % it)
        ripples.set_xlabel('X [m]')
        ripples.set_ylabel('Z [m]')
        plt.title('Time Evolving Profiles')
        plt.pause(0.01)
    if it % 5000 == 0: #save data for plot to mimic bob's paper
        save_it += 1
        saved_values[save_it, :] = bin_heights

###############################FINALIZE

final_fig = plt.figure(figsize=(12,8))
profiles = plt.subplot(111) #time series of topographic profiles
profiles.plot(bins,saved_values[0, :], linewidth = 3, label='0 impacts')
profiles.plot(bins,saved_values[1, :] + 0.02, linewidth = 3, label='5000')
profiles.plot(bins,saved_values[2, :] + 0.05, linewidth = 3, label='10000')
profiles.plot(bins,saved_values[3, :] + 0.1, linewidth = 3, label='15000')
profiles.plot(bins,saved_values[4, :] + 0.15, linewidth = 3, label='20000')
profiles.plot(bins,saved_values[5, :] + 0.23, linewidth = 3, label='25000')
plt.legend()
plt.title('Ripple Time Series')
profiles.set_xlabel('X [m]')
profiles.set_ylabel('Z [m]')
plt.show()
        