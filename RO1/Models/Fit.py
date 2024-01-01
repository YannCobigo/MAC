#!/usr/bin/python3
#import pdb #; pdb.set_trace()

import os
import numpy as np
import matplotlib.pyplot as plt
import pylab as py
import numpy as np
import matplotlib.cm as cm
import pandas
import statsmodels.formula.api as sm
import statsmodels.robust as robust
import math

#
#
#
import utils.loader                     as loaders
import trajectory.celerity              as celerity
import trajectory.time_series           as time_series
import trajectory.temporal_acceleration as temporal_acceleration

#
#
if __name__ == '__main__':
    #
    # Create the main frames
    dfs = loaders.dataframes()
    dfs.create_main_frames()
    #
    # create the objects
    print ("Instanciate objects that will process the data")
    procs = 1
    # trajectory
    sequence     = time_series.temporal_sequence( Procs      = procs,
                                                  Dataframes = dfs.data_frames_ )
    # velocity
    celerity     = celerity.velocity( Procs      = procs,
                                      Dataframes = dfs.data_frames_ )
    # acceletation
    acceleration = temporal_acceleration.acceleration( Procs      = procs,
                                                       Dataframes = dfs.data_frames_ )

    #########################
    # Plot the trajectories #
    #########################
    #
    #
    ####
    # V: 0 - voxel
    # R: 1 - ROI
    # L: 2 - lobe
    VRL = 2
    # Voxel
    X = 41
    Y = 73
    Z = 35
    # Region of Interest
    ROI = 1027
    #
    # Metric
    # [v, z_v]
    metric = "v"
    # model
    DR = "DR3"


    ####################
    # Plot the results #
    ####################
    fig = plt.figure()
    #
    # Volume
    ax1 = fig.add_subplot(311)
    #plt.ylim(0.2,1.)
    #plt.xlim(0.,1.)
    #
    sequence.load( metric, [ DR, VRL, [ROI, X, Y, Z] ], ax1 )
    ##
    # Velocity
    ax2 = fig.add_subplot(312)
    #plt.ylim(-2.,2.)
    #plt.xlim(0.,1.)
    #
    celerity.load( metric, [ DR, VRL, [ROI, X, Y, Z] ], ax2 )
    #
    # Acceleration
    ax3 = fig.add_subplot(313)
    #plt.ylim(-5.,5.)
    #plt.xlim(0.,1.)
    #
    acceleration.load( metric, [ DR, VRL, [ROI, X, Y, Z] ], ax3 )
    #
    #
    plt.show()
