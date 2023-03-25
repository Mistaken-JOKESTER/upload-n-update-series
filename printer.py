from simple_chalk import chalk, green, bgWhite, red, black, bgGray
from config import Configuration

class Printer:
    log_falg = True

    def __init__(self) -> None:
        self.log_flag = Configuration.log_flag

    def success(self,msg):
        color =  black.bold.bgWhite
        print(color(msg))

    def danger(self,msg):
        color =  red.bold.bgWhite
        print('\n')
        print(color(msg))

    def info(self,msg):
        if self.log_falg:
            print('\t:: '+ msg)
    
    def subInfo(self,msg):
        if self.log_falg:
            print('\t\t:: '+ msg)
