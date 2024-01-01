#import pdb; #pdb.set_trace()
import pandas
import sys, shutil, os
import numpy
import threading, queue, time
singlelock = threading.Lock()

class multi_thread( object ):
    """
    
    """
    def __init__( self, Procs = 8, Dataframes = {} ):
        """Return a new Protocol instance (constructor)."""
        try:
            #
            # private members
            self.tempo_dirs_ = []
            #
            # Multi-threading
            self.queue_ = queue.Queue()
            self.procs_ = Procs
            #
            #
            self.data_frames_ = Dataframes
            self.args_        = {}
            #
            #
            self.Left_temp_   = ["1009","1015","1030","1033","1034"]
            self.Right_temp_  = ["2009","2015","2030","2033","2034"]
            self.Left_front_  = ["1003","1012","1014","1027","1028","1032"]
            self.Right_front_ = ["2003","2012","2014","2027","2028","2032"]
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
    def load( self, Metric, Model, Ax ):
        """ Create the plot model for the specific object."""
        try:
            #
            #
            self.args_ = { "Metric" : Metric,
                           "Model"  : Model,
                           "Ax"     : Ax }
            #
            # create the pool of threads
            for i in range( self.procs_ ):
                t        = threading.Thread( target = self.get_time_series_ )
                t.daemon = True
                t.start()

            #
            #
            for name in self.data_frames_[ Metric ][ Model[0] ][ "ts" ][ "PIDN" ].unique():
                print (name)
                self.queue_.put( [name] )
            #
            # block until all tasks are done
            self.queue_.join()

            #
            # Add the group model
            self.get_group_fit_()
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
    def polynome( self, T, Parameters ):
        """."""
        try:
            #
            #
            # Remove temporary directories
            value = 0
            #pdb.set_trace()
            #
            for power in range( len(Parameters) ):
                #print (power)
                t = [1] * len(T)
                #
                for p in range( power ):
                    t = numpy.multiply(t, T)
                #
                value += Parameters[power] * numpy.asarray( t )
            #
            #
            return ( value )
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
