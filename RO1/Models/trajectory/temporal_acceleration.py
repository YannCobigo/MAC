#import pdb #; pdb.set_trace()
import sys, shutil
import numpy
import threading, queue, time
singlelock = threading.Lock()
#
#
#
import utils.threader as threader
#
#
#
class acceleration( threader.multi_thread ):
    """
    
    """
    def __init__( self, Procs, Dataframes = 8 ):
        super( acceleration, self ).__init__( Procs, Dataframes )
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
    def derivative( self, Values, TimePoints ):
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
                DF = self.data_frames_[ self.args_["Metric"] ][ self.args_["Model"][0] ]
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
                        # Voxel treatment
                        X = self.args_["Model"][2][1]
                        Y = self.args_["Model"][2][2]
                        Z = self.args_["Model"][2][3]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Age"]
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Volume"]
                    elif self.args_["Model"][1] == 1:
                        # ROI treatment
                        ROI = self.args_["Model"][2][0]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Age"].mean()
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Volume"].mean()
                    else:
                        # Lobe treatment
                        LOBE = self.Left_temp_ + self.Right_temp_
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Age"].mean()
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Volume"].mean()
                    #
                    # Then add to the plot
                    age = (age - C1) / C2
                    ( c, t ) = self.derivative( vol.values, age.values )
                    ( a, t ) = self.derivative( c, t )
                    #
                    if len(a):
                        singlelock.acquire()
                        self.args_["Ax"].plot( t, a, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                        singlelock.release()
                elif self.args_["Model"][0] == "DR3":
                    # Age transformation
                    C1 = DF["C"][0]
                    C2 = DF["C"][1]
                    #
                    if self.args_["Model"][1] == 0:
                        # Voxel treatment
                        X = self.args_["Model"][2][1]
                        Y = self.args_["Model"][2][2]
                        Z = self.args_["Model"][2][3]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Age"]
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['X'] == X) & (DF["ts"]['Y'] == Y) & (DF["ts"]['Z'] == Z) ]["Volume"]
                    elif self.args_["Model"][1] == 1:
                        # ROI treatment
                        ROI = self.args_["Model"][2][0]
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Age"].mean()
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'] == ROI) ].groupby(["Age"])["Volume"].mean()
                    else:
                        # Lobe treatment
                        LOBE = self.Left_temp_ + self.Right_temp_
                        #
                        age = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Age"].mean()
                        vol = DF["ts"][ (DF["ts"]['PIDN'] == Name) & (DF["ts"]['ROI'].isin(LOBE)) ].groupby(["Age"])["Volume"].mean()
                    #
                    # Then add to the plot
                    age = (age - C1) / C2
                    ( c, t ) = self.derivative( vol.values, age.values )
                    ( a, t ) = self.derivative( c, t )
                    #
                    if len(a):
                        singlelock.acquire()
                        self.args_["Ax"].plot( t, a, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
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
            #pdb.set_trace()
            #
            # Patient characteristics
            # Age transformation
            t1 = numpy.arange(0.0, 1.0, .01)
            #
            # Group #1
            color =  "red"
            # 
            if self.args_["Model"][0] == "DR3":
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a2  = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a02"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    #
                    a2  = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a02"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    #
                    a2  = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a02"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
                #
                # Then add to the plot
                if len( vol ):
                    singlelock.acquire()
                    #pdb.set_trace()
                    self.args_["Ax"].plot( t1, vol, marker='', color = color, linewidth = 0.6, alpha = 0.3 )
                    singlelock.release()
                #
                # Group #2
                color =  "green"
                # 
                if self.args_["Model"][1] == 0:
                    # Voxel treatment
                    X = self.args_["Model"][2][1]
                    Y = self.args_["Model"][2][2]
                    Z = self.args_["Model"][2][3]
                    #
                    # Fitted trajectory
                    a2  = DF["model"][ (DF["model"]['X'] == X) & (DF["model"]['Y'] == Y) & (DF["model"]['Z'] == Z) ]["a12"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
                elif self.args_["Model"][1] == 1:
                    # ROI treatment
                    ROI = self.args_["Model"][2][0]
                    a2 = DF["model"][ (DF["model"]['ROI'] == ROI) ]["a12"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
                else:
                    # Lobe treatment
                    LOBE = self.Left_temp_ + self.Right_temp_
                    a2  = DF["model"][ (DF["model"]['ROI'].isin(LOBE)) ]["a12"].mean()
                    vol = threader.multi_thread.polynome( self, t1, [2. * a2] )
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
