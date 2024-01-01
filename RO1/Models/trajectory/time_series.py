import pdb #pdb.set_trace()
import sys, shutil
import numpy
import threading, queue, time
singlelock = threading.Lock()
#
#
#
import utils.threader as threader
import utils.Lagrange as Lagrange
#
#
#
class temporal_sequence( threader.multi_thread ):
    """
    
    """
    def __init__( self, Procs = 8, Dataframes = {} ):
        super( temporal_sequence, self ).__init__( Procs, Dataframes )
        """Return a new Protocol instance (constructor)."""
        try:
            #
            #
            pass
            #
        except Exception as inst:
            quit( -1 )
        except IOError as e:
            print( "I/O error({0}): {1}".format(e.errno, e.strerror) )
            quit( -1 )
        except:
            print( "Unexpected error:", sys.exc_info()[0] )
            quit( -1 )
    #
    #
    #
    def __del__( self ):
        """Destroy the Structural instance (destructor)."""
        try:
            #
            #
            # Remove temporary directories
            for directory in self.tempo_dirs_:
                if True:
                    print( "this tmpdir:", directory )
                else:
                    shutil.rmtree( directory )
            #
            #
        except Exception as inst:
            quit( -1 )
        except IOError as e:
            print( "I/O error({0}): {1}".format(e.errno, e.strerror) )
            quit( -1 )
        except:
            print( "Unexpected error:", sys.exc_info()[0] )
            quit( -1 )
    #
    #
    #
    def get_time_series_( self ):
        """Destroy the Structural instance (destructor)."""
        try:
            # 
            # Loop on the tasks
            while True:
                #
                #
                [Name] = self.queue_.get()
                #pdb.set_trace()
                DF = self.data_frames_[ self.args_["Metric"] ][ self.args_["Model"][0] ]
                t1 = numpy.arange(0.0, 1.0, .01)
                #
                # Patient characteristics
                if  DF["ts"][ (DF["ts"]['PIDN'] == Name) ]["Group"].mean() == 1:
                    color =  "red"
                else:
                    color = "green"
                    #
                if self.args_["Model"][0] == "DR2":
                    # Age transformation
                    C1 = DF["C"][0]
                    C2 = DF["C"][1]
                    #
                    if self.args_["Model"][1] == 0:
                        ###
                        # Voxel treatment
                        #pdb.set_trace()
                        X = self.args_["Model"][2][1]
                        Y = self.args_["Model"][2][2]
                        Z = self.args_["Model"][2][3]
                        # time points
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Age"]
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Volume"]
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["Rate"]
                    elif self.args_["Model"][1] == 1:
                        ###
                        # ROI treatment
                        ROI = self.args_["Model"][2][0]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Age"].mean()
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Volume"].mean()
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ]["Rate"]
                    else:
                        ###
                        # Lobe treatment
                        LOBE = self.Left_temp_ + self.Right_temp_
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Age"].mean()
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Volume"].mean()
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ]["Rate"]
                    #
                    # Then add to the plot
                    if len( vol ):
                        t1 = numpy.arange(age.values[0], age.values[-1], .01)
                        fit = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean()] )
                        # interpolation
                        interp = Lagrange.Interpolation( X = age, Y = vol, Delta = C2 )
                        (x_lagrange, y_lagrange) = interp.interpolate()
                        singlelock.acquire()
                        self.args_["Ax"].plot( age, vol, marker='.', color = color, linewidth = 0.6, alpha = 0.2 )
                        self.args_["Ax"].plot( x_lagrange, y_lagrange, marker='.', color = "purple", linewidth = 0.6, alpha = 0.2 )
                        self.args_["Ax"].plot( t1,  fit, marker='', color = color, linewidth = 0.6, alpha = 0.6 )
                        singlelock.release()
                elif self.args_["Model"][0] == "DR3":
                    # Age transformation
                    C1 = DF["C"][0]
                    C2 = DF["C"][1]
                    #
                    if self.args_["Model"][1] == 0:
                        ###
                        # Voxel treatment
                        #pdb.set_trace()
                        X = self.args_["Model"][2][1]
                        Y = self.args_["Model"][2][2]
                        Z = self.args_["Model"][2][3]
                        # time points
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Age"]
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Volume"]
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["Rate"]
                        a2  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["Acceleration"]
                    elif self.args_["Model"][1] == 1:
                        ###
                        # ROI treatment
                        ROI = self.args_["Model"][2][0]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Age"].mean()
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Volume"].mean()
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ]["Rate"]
                        a2  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ]["Acceleration"]
                    else:
                        ###
                        # Lobe treatment
                        LOBE = self.Left_temp_ + self.Right_temp_
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Age"].mean()
                        age = (age - C1) / C2
                        # Acquisition
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Volume"].mean()
                        # Polynome fit
                        a0  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ]["Intercept"]
                        a1  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ]["Rate"]
                        a2  = DF["model"][ (DF["model"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ]["Acceleration"]
                    #
                    # Then add to the plot
                    if len( vol ):
                        t1 = numpy.arange(age.values[0], age.values[-1], .01)
                        fit = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean(), a2.mean()] )
                        # interpolation
                        interp = Lagrange.Interpolation( X = age, Y = vol, Delta = C2 )
                        (x_lagrange, y_lagrange) = interp.interpolate()
                        singlelock.acquire()
                        self.args_["Ax"].plot( age, vol, marker='.', color = color, linewidth = 0.6, alpha = 0.2 )
                        self.args_["Ax"].plot( x_lagrange, y_lagrange, marker='.', color = "purple", linewidth = 0.6, alpha = 0.2 )
                        self.args_["Ax"].plot( t1,  fit, marker='', color = color, linewidth = 0.6, alpha = 0.6 )
                        singlelock.release()
                else:
                    # Age transformation
                    C1 = DF["C"][0]
                    C2 = DF["C"][1]
                    C3 = DF["C"][2]
                
                #
                #
                self.queue_.task_done()
            #
            #
        except Exception as inst:
            quit( -1 )
        except IOError as e:
            print( "I/O error({0}): {1}".format(e.errno, e.strerror) )
            quit( -1 )
        except:
            print( "Unexpected error:", sys.exc_info()[0] )
            quit( -1 )
    #
    #
    #
    def get_group_fit_( self ):
        """Destroy the Structural instance (destructor)."""
        try:
            # 
            # Loop on the tasks
            DF = self.data_frames_[ "global" ][ self.args_["Model"][0] ]
            #
            # Patient characteristics
            # Age transformation
            t1 = numpy.arange(0.0, 1.0, .01)
            #
            # Group #1
            color =  "red"
            # 
            if self.args_["Model"][0] == "DR2":
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a0 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a00"]
                    a1 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a01"]
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean()] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a00"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a01"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a00"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a01"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1] )
                #
                # Then add to the plot
                if len( vol ):
                    singlelock.acquire()
                    #pdb.set_trace()
                    self.args_["Ax"].plot( t1, vol, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                    singlelock.release()
                #
                # Group #1
                color =  "green"
                # 
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a0 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a10"]
                    a1 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a11"]
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean()] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a10"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a11"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a10"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a11"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1] )
                #
                # Then add to the plot
                if len( vol ):
                    singlelock.acquire()
                    #pdb.set_trace()
                    self.args_["Ax"].plot( t1, vol, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                    singlelock.release()
            elif self.args_["Model"][0] == "DR3":
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a0 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a00"]
                    a1 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a01"]
                    a2 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a02"]
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean(), a2.mean()] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a00"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a01"].mean()
                    a2 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a02"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1, a2] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a00"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a01"].mean()
                    a2 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a02"].mean()
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0, a1, a2] )
                #
                # Then add to the plot
                if len( vol ):
                    singlelock.acquire()
                    #pdb.set_trace()
                    self.args_["Ax"].plot( t1, vol, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                    singlelock.release()
                #
                # Group #1
                color =  "green"
                # 
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a0 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a10"]
                    a1 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a11"]
                    a2 = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a12"]
                    #
                    vol = threader.multi_thread.polynome( self,  t1, [a0.mean(), a1.mean(), a2.mean()] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a10"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a11"].mean()
                    a2 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a12"].mean()
                    #
                    vol = threader.multi_thread.polynome( self, t1, [a0, a1, a2] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    #
                    a0 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a10"].mean()
                    a1 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a11"].mean()
                    a2 = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a12"].mean()
                   #
                    vol = threader.multi_thread.polynome( self, t1, [a0, a1, a2] )
                #
                # Then add to the plot
                if len( vol ):
                    singlelock.acquire()
                    #pdb.set_trace()
                    self.args_["Ax"].plot( t1, vol, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                    singlelock.release()
            #
            #
        except Exception as inst:
            quit( -1 )
        except IOError as e:
            print( "I/O error({0}): {1}".format(e.errno, e.strerror) )
            quit( -1 )
        except:
            print( "Unexpected error:", sys.exc_info()[0] )
            quit( -1 )
           
