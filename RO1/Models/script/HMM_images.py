#!/usr/bin/python3
#import pdb #; pdb.set_trace()

import pandas
import sys, shutil, os
import matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf

States    = 5
data_file = "/home/cobigo/devel/Python/MAC/RO1/Models/script/dataset/HMM_dataset_%sStates.csv"%(States)
df        = pandas.read_csv( data_file, sep=',', encoding='latin1' )

#
#
#
def derivative( Values, TimePoints ):
    #
    #print ( "Vals: ", Values )
    #print ( "t: ", TimePoints )
    Velocity = []
    Time     = []
    #
    if len(Values) > 1:
        if len(Values) > 2:
            # good gradiant
            for t in range( 1, len(Values) - 1 ):
                dx  = Values[t+1] - Values[t-1]
                dt  = float( TimePoints[t+1] - TimePoints[t] )
                dt += float( TimePoints[t]   - TimePoints[t-1] )
                dt /= 2.
                t  = TimePoints[t]
                Velocity.append( dx / dt / 2.)
                Time.append( t )
        else:
            # instantaneous gradiant
            for t in range( len(Values) - 1 ):
                dx = Values[t+1] - Values[t]
                dt = float( TimePoints[t+1] - TimePoints[t] )
                t  = (TimePoints[t+1] + TimePoints[t]) / 2.
                Velocity.append( dx / dt )
                Time.append( t )
    #
    #
    return (Velocity, Time)



#
#
if __name__ == '__main__':
    #
    #
    min_age = df[ "Age" ].unique().min()
    max_age = df[ "Age" ].unique().max()
    #
    C1 = min_age
    C2 = max_age - min_age

    
    ####################
    # Plot the results #
    ####################
    fig = plt.figure()
    #
    Ax = {}
    #
    #
    if States == 3:
        Ax["S0"] = fig.add_subplot(311)
        Ax["S1"] = fig.add_subplot(312)
        Ax["S2"] = fig.add_subplot(313)
        #
        # Volume
        for name in df[ "PIDN" ].unique():
            print (name)
            for s in ["S0","S1","S2"]:
                age         = df[ ( df["PIDN"] == name ) & ( df["State"] == s ) ]["Age"]
                cluster     = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["Cluster"]
                probability = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["Probability"]
                level_CDR   = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["N"]
                clus_prob = cluster * probability
                # Color
                group = df[ ( df["PIDN"] == name ) ]["Group"].mean()
                color = "green"
                if group == 1:
                    color = "red"
                # dot mapping
                dot_map = {1:'green', 2:'blue', 3:'red'}
                #
                age = (age - C1) / C2
                ( c, t_c ) = derivative( cluster.values, age.values )
                ( a, t_a ) = derivative( c, t_c )
                #
                #Ax[s].plot( age, clus_prob, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                Ax[s].plot( age, cluster, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #Ax[s].plot( t_c, c, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #Ax[s].plot( t_a, a, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #
                Ax[s].scatter( age, cluster, color = level_CDR.map( dot_map ), s = 2, zorder = 6. )
                #
    elif States == 5:
        #ax = fig.add_subplot(111)
        Ax["S0"] = fig.add_subplot(511)
        Ax["S1"] = fig.add_subplot(512)
        Ax["S2"] = fig.add_subplot(513)
        Ax["S3"] = fig.add_subplot(514)
        Ax["S4"] = fig.add_subplot(515)
        
        #
        # Volume
        for name in df[ "PIDN" ].unique():
            print (name)
            for s in ["S0","S1","S2","S3","S4"]:
                age         = df[ ( df["PIDN"] == name ) & ( df["State"] == s ) ]["Age"]
                cluster     = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["Cluster"]
                probability = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["Probability"]
                level_CDR   = df[ ( df["PIDN"] == name ) & ( df["State"] == s )  ]["N"]
                clus_prob   = cluster * probability
                #
                # Colors
                group = df[ ( df["PIDN"] == name ) ]["Group"].mean()
                color = "green"
                if group == 1:
                    color = "red"
                # dot mapping
                dot_map = {1:'green', 2:'blue', 3:'red'}
                #
                age = (age - C1) / C2
                ( c, t_c ) = derivative( cluster.values, age.values )
                ( a, t_a ) = derivative( c, t_c )
                #
                #Ax[s].plot( age, clus_prob, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                Ax[s].plot( age, cluster, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #Ax[s].plot( t_c, c, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #Ax[s].plot( t_a, a, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                #
                Ax[s].scatter( age, cluster, color = level_CDR.map( dot_map ), s = 2, zorder = 6. )
#                if s == "S0":
#                    ax.plot( age, cluster, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
#                    ax.scatter( age, cluster, color = level_CDR.map( dot_map ), s = 2, zorder = 6. )
        

    #
    #
    plt.show()
