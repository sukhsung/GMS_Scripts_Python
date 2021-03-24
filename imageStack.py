from tkinter import *
import numpy as np

#import DigitalMicrograph as DM
import fauxEM as DM

class imStack :
    def __init__(self):
        self.ccdsize = 4096

        self.root = Tk()
        self.root.geometry("200x400")
        self.root.title("Image Stack")

        self.mainFrame = Frame(self.root)
        self.mainFrame.pack()

        self.topFrame = Frame(self.mainFrame )
        self.topFrame.pack()
        self.lftFrame = Frame( self.topFrame )
        self.lftFrame.pack(side='left')
        self.rgtFrame = Frame( self.topFrame )
        self.rgtFrame.pack(side='right')

        self.botFrame = Frame(self.mainFrame)
        self.botFrame.pack()
        
        self.entry_bin = (labeledEntry( self.lftFrame, self.rgtFrame ,"Bin: ", "10"))
        self.entry_exp = (labeledEntry( self.lftFrame, self.rgtFrame  ,"Exposure (s): ", "0.5"))
        self.entry_fra = (labeledEntry( self.lftFrame, self.rgtFrame  ,"# of Frames: ", "1"))
        self.entry_name = (labeledEntry( self.lftFrame, self.rgtFrame  ,"Name: ", "Image Stack"))

        self.btn_acquire = Button(self.botFrame, text = "Acquire", command = self.acquire)
        self.btn_acquire.pack(padx = 5, pady =5)


        self.root.mainloop()
        

    def parseEntries(self):
        self.bin = int(self.entry_bin.entry.get())
        self.exp = float(self.entry_exp.entry.get())
        self.fra = int(self.entry_fra.entry.get())
        self.nx  = int(self.ccdsize/self.bin)
        self.name  = self.entry_name.entry.get()

    def acquire(self):
        self.parseEntries()

        cam = DM.GetActiveCamera()
        cam.PrepareForAcquire()
        kUnproc = 2#DM.GetCameraUnprocessedEnum()
        max_wait_s = 5*self.exp        # time out after 5 x exposure.  

        # Pre-allocate Images
        dstImage = cam.CreateImageForAcquire( self.bin, self.bin, kUnproc )
        imgArray = np.zeros( (self.fra,self.nx,self.nx) )

        cam.StartContinuousAcquisition( self.exp, self.bin, self.bin, kUnproc )
        
        for i in range(0, self.fra ):
            if ( cam.GetFrameInContinuousMode( dstImage, max_wait_s ) ):
                print( 'Got frame #', i )

                #dstImage.UpdateImage() # Force display update
                imgArray[i,:,:] = dstImage.GetNumArray()

            else:

                print( 'Time-out' ) 

        cam.StopContinuousAcquisition( )
        img = DM.CreateImage(imgArray)
        img.SetName(self.name)

        # Show image in GMS to store imstack to memory
        img.ShowImage()

        # Always delete Py_Image variables again
        del dstImage
        del imgArray
        
        print( 'Finshed Acquiring' )
 

        

class labeledEntry:
    def __init__(self, labelFrame, entryFrame, label, value):
        self.label = Label( labelFrame, text = label)
        self.entry = Entry( entryFrame)
        self.entry.insert(0, value)
        self.label.pack(padx = 5, pady =5)
        self.entry.pack(padx = 5, pady =5)

h = imStack()


