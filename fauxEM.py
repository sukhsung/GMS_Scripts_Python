import numpy as np

class fauxCamera :
    def __init__(self):
        self.ccdx = 4096
        self.ccdy = 4096


    def PrepareForAcquire(self):
        return True

    def CreateImageForAcquire( self, binX, binY, Processing):
        nx = int( self.ccdx/ binX)
        ny = int( self.ccdy/ binY)
        return CreateImage( np.zeros( (nx,ny) ) )

    def StartContinuousAcquisition( self, exposureTime, binX, binY, Processing):
        self.nx = int( self.ccdx/ binX)
        self.ny = int( self.ccdy/ binY)
        return True

    def StopContinuousAcquisition( self):
        return True

    def GetFrameInContinuousMode( self, dstImage, max_wait_s ):
        dstImage.setImage( np.random.random( (self.nx, self.ny) ) )
        
        return True

class Py_Microscope() :
    def __init__(self):
        self.beamTiltX = 0
        self.beamTiltY = 0
    
    def GetBeamTilt(self):
        return (self.beamTiltX, self.beamTiltY)

    def SetBeamTilt(self, tiltX, tiltY):
        self.beamTiltX = tiltX
        self.beamTiltY = tiltX

class DMImage :
    def __init__( self,image ):
        self.image = image

    def SetName( self, name ):
        self.name = name

    def ShowImage( self ):
        return True

    def GetNumArray( self ):
        return self.image

    def setImage (self, image):
        self.image =image

def GetActiveCamera() :
    return fauxCamera()

def CreateImage(imgArray) :
    return DMImage(imgArray)

def GetCameraUnprocessedEnum():
    return 3