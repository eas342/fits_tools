from astropy.io import fits
from astropy.table import Table
import numpy as np
import os
import glob
import sys
import pdb

class headerTable():
    def __init__(self,fileSearch,headList,extension=0):
        """ A header table is made for a given set of parameters 
        
        Parameters
        -----------------
        fileSearch: str
            A place to search for files. For example '/data/myfiles*.fits'
        headList: list
            A list of headers to include in a table. Ex. ['OBJECT','DATE-OBS']
        extension: int
            The FITS extension for where to look for headers
        """
        self.fileSearch = fileSearch
        self.fileList = glob.glob(fileSearch)
        self.nFile = len(self.fileList)
        self.headers = headList
        self.nkeys = len(headList)
        self.extension = extension
        
    def getVals(self):
        """ Gets the keyword values from headers """
        baseNames = []
        hVals = [] ## list of lists of key values
        ## I do this instead of a 2d array since we don't know types - string/int/float yet
        for keyInd in np.arange(self.nkeys):
            hVals.append([])
        hMask = np.zeros((self.nkeys,self.nFile),dtype=np.bool)
        for fileInd, oneFile in enumerate(self.fileList):
            HDUList = fits.open(oneFile)
            head = HDUList[self.extension].header
            baseNames.append(os.path.basename(oneFile))
            for keyInd, oneKey in enumerate(self.headers):
                if oneKey in head:
                    hVals[keyInd].append(head[oneKey])
                else:
                    hVals[keyInd].append(0)
                    hMask[keyInd,fileInd] = True
        t = Table()
        t['Path'] = baseNames
        for keyInd in np.arange(self.nkeys):
            t[self.headers[keyInd]] = np.ma.masked_array(hVals[keyInd],mask=hMask[keyInd,:])
        return t
    
if __name__ == "__main__":
    hT = headerTable(fileSearch=argv[1],headList=argv[1],extension=0)
    hT.getVals()
    
