import pdb; #pdb.set_trace()
import pandas
import sys, shutil, os
#
#
#
class Interpolation( object ):
    """
    
    """
    def __init__( self, X, Y, Delta ):
        """Return a new Protocol instance (constructor)."""
        try:
            #
            # private members
            self.tempo_dirs_ = []
            #
            # tweackables
            # leap between two acquisitions
            self.days_ = 365.25 / 2.
            #
            # Polynomial interpolation
            self.X_     = X
            self.Y_     = Y
            self.delta_ = Delta
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
    def interpolate( self ):
        """ Creates the dataframes."""
        try:
            #
            # The age should be normalized between [0,1]
            if self.X_.values[0] < 0.0 or self.X_.values[-1] > 1.0:
                raise Exception( "The X values should be between [0,1]." )
            #
            # Calculate the steps
            step   = self.days_ / self.delta_
            steps  = [ self.X_.values[0] ]
            interp = []
            #
            while steps[-1] < self.X_.values[-1]:
                steps.append( steps[-1] + step )
            # remove the last point
            steps = steps[:-1]

            #
            #
            #pdb.set_trace()
            for s in steps:
                coeff = 0.0
                for r in range( len(self.X_.values) ):
                    root_num   = self.Y_.values[ r ]
                    root_denom = 1.0
                    for rr in range( len(self.X_.values) ):
                        if r != rr:
                            root_num   = ( s - self.X_.values[ rr ] ) * root_num
                            root_denom = ( self.X_.values[ r ] - self.X_.values[ rr ] ) * root_denom
                    #
                    coeff += root_num / root_denom
                #
                #
                interp.append( coeff )
            #
            #
            return ( steps, interp )
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
