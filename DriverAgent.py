
import os
import time
import random

import urllib.request
from urllib3.exceptions import MaxRetryError

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.firefox.options import FirefoxProfile
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException


class DriverAgent():
    ''' selenium driver agent, packaging driver settings and actions in one
    class for facilitated browser automation, keeping implementations as free 
    from selenium-related detail as possible
    '''
    
    def __init__( self, downDir ):
        
        modDir = os.path.dirname(os.path.abspath(__file__))
        
        self.keys = Keys
        self.exec_path = modDir + "\\_driver\\geckodriver.exe"
        self.downDir = downDir
    
    def raiseDriver( self, headless ):
        
        serv = Service( self.exec_path )
        # serv.log_path = self.logs_path
        serv.log_path = "geckolog.log" # os.path.devnull
        
        opts = self.getOptions( headless )
        
        print("\nRaising webdriver, please wait...\n")
        try: driver = webdriver.Firefox( options=opts, service=serv )
        except Exception as e: 
            print( f"\nDRIVER EXC {type(e).__name__}" )
            inp = input( "ANY INPUT TO RETRY... " )
        else: 
            driver.set_page_load_timeout(30)
            actions = ActionChains(driver)
            self.driver = driver
            self.actions = actions
            print( "Driver running" )
    
    def getOptions( self, headless ):
        
        opts = Options() 
        
        if headless:
            opts.headless = True
            opts.add_argument("--width=2560")
            opts.add_argument("--height=1440")
        
        opts.add_argument("--disable-infobars")
        opts.add_argument("--disable-extensions")
        
        pref = opts.set_preference
        
        user_agent = ( "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:103.0) "
            + "Gecko/20100101 Firefox/103.0" )
            
        pref("general.useragent.override", user_agent)
        
        # SUPPRESS NOTIFICATIONS
        pref("dom.webnotifications.enabled", False);
        pref("dom.push.enabled", False);
        
        # RESTRICT TO SINGLE TAB ( PREVENTS LOCATOR ISSUES )
        pref("browser.link.open_newwindow", 1)
        pref("browser.link.open_newwindow.restriction", 0)
        pref("browser.link.open_newwindow.override.external", 3)
        
        # SET DOWNLOAD PATH
        pref("browser.download.folderList", 2)
        pref("browser.download.dir", self.downDir )  
        
        # DISABLE INTERNAL PDF VIEWER
        pref("browser.download.manager.showWhenStarting", False)
        pref("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        pref("pdfjs.disabled", True)
        
        # PRINT PAGE AS PDF TO FILE
        pref("print_printer", "Microsoft Print to PDF")
        pref("print.always_print_silent", True)
        pref("print.show_print_progress", False)
        pref('print.save_as_pdf.links.enabled', True)
        pref("print.printer_Microsoft_Print_to_PDF.print_to_file", True)
        pref('print.printer_Microsoft_Print_to_PDF.print_to_filename', 
            "printed_temp.pdf")
        
        return opts
    
    
    def getBrowser( self, headless=False, initURL=None ):
        
        if not initURL: initURL = "http://www.example.com"
        
        while True:
            try: self.driver.get( initURL )
            except (
                NameError, 
                WebDriverException, 
                AttributeError,
                ConnectionRefusedError,
                MaxRetryError) as e: 
                self.raiseDriver(headless)
            else: time.sleep(self.randDbl(3, 4)); return
    
    
    def xpathEC( self, _xpath, waitLo=5, waitHi=10, drobject=None):
        driver = self.driver if not drobject else drobject
        while True:
            try: return WebDriverWait( 
                driver, self.randDbl( waitLo, waitHi )).until( 
                    EC.presence_of_element_located(( By.XPATH, _xpath )))
            except TimeoutException: return None
    
    
    def randDbl( self, loLimit=0.4, hiLimit=1.9 ):
        return random.uniform(loLimit, hiLimit)
    
    
    def randSleep( self, lo=2, hi=3 ): time.sleep( self.randDbl(lo, hi) )
    
