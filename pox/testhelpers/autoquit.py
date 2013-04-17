'''
Created on Apr 17, 2013

@author: Tim Herinckx

This module halts pox after the specified number of seconds

'''

from pox.core import core
from pox.lib.recoco import Timer

log=core.getLogger()
 
 
def _quit_pox():
  log.info('Autoquit will halt pox')
  core.quit()

def launch (quittime=0):
  qt=round(float(quittime)) 
  if(qt>0):
    Timer(qt, _quit_pox,args=[])
    log.debug('Autoquit started, will halt pox in %d seconds',qt)