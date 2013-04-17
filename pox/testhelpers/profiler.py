'''
Created on Apr 17, 2013

@author: Tim Herinckx

This is a wrapper for the yappi profiler (code.google.com/p/yappi)
cProfile doesn't work well with pox due to the cooperative threading design.
yappi does produce valuable measurements.

Make sure yappi is installed (easy_install yappi)

At the moment the profiling information is written to the log when pox is stopped.
There is a small change to core.py to achieve this (search for #Added to finish yappi  in the source).

For the command line options, please check the yappi wiki.
Setting a limit is recommended

'''

from pox.core import core
from pox.lib.recoco import Timer
import yappi

log=core.getLogger()

class Profiler:
    
  def __init__(self,sorttypeyappi,sortorderyappi,limityappi):
      yappi.start(builtins=False) 
      self.sorttypeyappi=sorttypeyappi
      self.sortorderyappi=sortorderyappi
      self.limityappi=limityappi
    
    
  def finish(self):
    yappi.stop()
    stats = yappi.get_stats(self.sorttypeyappi,self.sortorderyappi,self.limityappi)
    for s in stats.func_stats:
      log.info('%s was called %s times, ttotal %s, tsub %s0',s.name,s.ncall,s.ttot,s.tsub)

def launch (sorttype='',sortorder='',limit=-1):
    
    #set sorttype (see yapi wiki for more information)
    if (sorttype=='NAME'):
        sorttypeyappi= yappi.SORTTYPE_NAME
    elif (sorttype=='NCALL'):
        sorttypeyappi= yappi.SORTTYPE_NCALL
    elif (sorttype=='TTOTAL'):
	#TODO: there's currently still an issue with TTOTAL
        sorttypeyappi= yappi.SORTTYPE_TTOTAL
    elif (sorttype=='TSUB'):
        sorttypeyappi= yappi.SORTTYPE_TSUB
    elif (sorttype=='TAVG'):
        sorttypeyappi= yappi.SORTTYPE_TAVG
    else:
        #default
        sorttypeyappi= yappi.SORTTYPE_TAVG      
 
    #set sortorder
    if(sortorder=='ASC'):
        sortorderyappi=yappi.SORTORDER_ASC
    elif(sortorder=='DESC'):
        sortorderyappi=yappi.SORTORDER_DESC
    else:
        #default
        sortorderyappi=yappi.SORTORDER_ASC
        
    #set limit
    limityappi=int(limit)
    if (limit==-1):
        limityappi=yappi.SHOW_ALL
    
    if not core.hasComponent("profiler"):
        core.register("profiler",Profiler(sorttypeyappi,sortorderyappi,limityappi))
    log.debug('Yappi is running')
        
