#import pdb; #pdb.set_trace()
import pandas
import sys, shutil, os
#
#
#
class dataframes( object ):
    """
    
    """
    def __init__( self, ):
        super( dataframes, self ).__init__()
        """Return a new Protocol instance (constructor)."""
        try:
            #
            # private members
            self.tempo_dirs_ = []
            #
            # tweackable
            self.data_        = "/home/cobigo/devel/Python/RO1/Models/Curated/"
            self.data_frames_ = {}
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
    def create_main_frames( self ):
        """ Creates the dataframes."""
        try:
            #
            #
            #
            # Volumes
            print ("Loading v.csv")
            v         = os.path.join( self.data_, "v.csv" )
            print ("Loading std_v.csv")
            z_v     = os.path.join( self.data_, "std_v.csv" )
            #
            # DR2 trajectography
            print ("Loading model_v_DR2.csv")
            model_v_DR2  = os.path.join( self.data_, "model_v_DR2.csv" )
            print ("Loading model_std_v_DR2.csv")
            model_z_v_DR2 = os.path.join( self.data_, "model_std_v_DR2.csv" )
            #
            # DR3
            print ("Loading model_v_DR3.csv")
            model_v_DR3  = os.path.join( self.data_, "model_v_DR3.csv" )
            print ("Loading model_std_v_DR3.csv")
            model_z_v_DR3 = os.path.join( self.data_, "model_std_v_DR3.csv" )
            #
            # Global model DR2
            print ("Loading model_glob_v_DR2.csv")
            model_glob_v_DR2   = os.path.join( self.data_, "model_glob_v_DR2.csv" )
            print ("Loading model_glob_std_v_DR2.csv")
            model_glob_z_v_DR2 = os.path.join( self.data_, "model_glob_std_v_DR2.csv" )
            print ("Loading model_glob_v_DR3.csv")
            model_glob_v_DR3   = os.path.join( self.data_, "model_glob_v_DR3.csv" )
            print ("Loading model_glob_std_v_DR3.csv")
            model_glob_z_v_DR3 = os.path.join( self.data_, "model_glob_std_v_DR3.csv" )



            #
            # Load the main frames
            # Volumes
            df_v   = pandas.read_csv( v, sep=',', encoding='latin1' )
            df_z_v = pandas.read_csv( z_v, sep=',', encoding='latin1' )
            # trajectory DR2
            df_model_v_DR2   = pandas.read_csv( model_v_DR2, sep=',', encoding='latin1' )
            df_model_z_v_DR2 = pandas.read_csv( model_z_v_DR2, sep=',', encoding='latin1' )
            # trajectory DR3
            df_model_v_DR3   = pandas.read_csv( model_v_DR3, sep=',', encoding='latin1' )
            df_model_z_v_DR3 = pandas.read_csv( model_z_v_DR3, sep=',', encoding='latin1' )
            # Global trajectories 
            df_glob_v_DR2   = pandas.read_csv( model_glob_v_DR2, sep=',', encoding='latin1' )
            df_glob_z_v_DR2 = pandas.read_csv( model_glob_z_v_DR2, sep=',', encoding='latin1' )
            df_glob_v_DR3   = pandas.read_csv( model_glob_v_DR3, sep=',', encoding='latin1' )
            df_glob_z_v_DR3 = pandas.read_csv( model_glob_z_v_DR3, sep=',', encoding='latin1' )
            #print( df_v )
            self.data_frames_ = \
                {
                    "v":
                    {
                        "DR2":
                        {
                            "ts": df_v,
                            "model": df_model_v_DR2,
                            "C":[25455,8900]
                        },
                        "DR3":
                        {
                            "ts": df_v,
                            "model": df_model_v_DR3,
                            "C":[25455,8900]
                        }
                    },
                    "z_v":
                    {
                        "DR2":
                        {
                            "ts": df_z_v,
                            "model": df_model_z_v_DR2,
                            "C":[25455,8900]
                        },
                        "DR3":
                        {
                            "ts": df_z_v,
                            "model": df_model_z_v_DR3,
                            "C":[25455,8900]
                        }
                    },
                    "global":
                    {
                        "DR2":
                        {
                            "model": df_glob_v_DR2,
                            "model_z": df_glob_z_v_DR2,
                            "C":[25455,8900]
                        },
                        "DR3":
                        {
                            "model": df_glob_v_DR3,
                            "model_z": df_glob_z_v_DR3,
                            "C":[25455,8900]
                        }
                    }
                    #,
                    #        "std_nu":
                    #        {
                    #            "std_nu":df_std_nu,
                    #            "std_nu_DR2": df_model_std_nu_dr2,
                    #            "std_nu_DR3": df_model_std_nu_dr3
                    #        }        
                }
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
