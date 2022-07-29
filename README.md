# Selenium driver agent
Selenium driver agent, packaging driver settings and actions in one
class for facilitated browser automation, keeping implementations as free 
from selenium-related detail as possible.

Latest driver executable ( place at "_driver" ) is available at;
https://github.com/mozilla/geckodriver/releases

Example implementation instantiates DriverAgent, requiring
a path for the driver executable, driver log and download path.
It also makes agent methods more easily referenced with class variables,
exposing commonly used driver attributes without needing local imports.

For a fuller implementation see rsrcCrawler.
