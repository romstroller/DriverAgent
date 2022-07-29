
from DriverAgent import DriverAgent

import os
import time


class DriverImplementer():
    ''' This example implementation instantiates DriverAgent, requiring
    a path for the driver executable, driver log and download path.
    It also makes agent methods more easily referenced with class variables,
    exposing commonly used driver attributes without needing local imports.
    '''
    
    def __init__( self ):
    
        os.chdir(os.path.dirname(os.path.abspath(__file__)))
        self.cwd = os.getcwd()
        self.downloads = self.cwd + "\\" + "_TEMP"
    
    
    def startSession( self ):
        
        self.agent = DriverAgent( self.downloads )
        self.agent.getBrowser(headless=False)
        
        # for quicker reference, assign agent's methods to class variables
        self.driver = self.agent.driver
        self.xpathEC = self.agent.xpathEC
        self.keys = self.agent.keys
    
    
    def runAction( self ):
        
        self.driver.get('http://www.wikipedia.org')
        
        searchBoxXP = "//*[@id='searchInput']"
        searchBoxEC = self.xpathEC( searchBoxXP )
        if not searchBoxEC: print( "Timeout on searchbox" ); return
        
        searchBoxEC.send_keys("Rick Astley")
        time.sleep(1)
        searchBoxEC.send_keys(self.keys.ENTER)


honk = DriverImplementer()

honk.startSession()

honk.runAction()