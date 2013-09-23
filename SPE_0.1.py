# -*- coding: utf-8 -*-
"""
Created on Mon Sep 23 14:19:27 2013

@author: eweixwa
"""

import time
from pyvisa.visa import *
###############################################################################
# SPE test
# Agilent N9020A and N9030A support
###############################################################################


###############################################################################
# Input parameter definition
###############################################################################
# 1) Configuration information
sa_addr='GPIB0::18'

part_number='FU0001'
revision='R1'
series_number='CBM123456'
inspector='jy01'
test_date='2013-09-22'
ambient_temperature=23



# 2) SPE test parameters
# [start_f,stop_f,rbw,detector,sweep_time,ext_gain,limit]

test_para=[[10,100,100,'aver',1,'-1',-100],[100,1000,100,'aver',1,'-1',6,-36],[1000,3000,100,'aver',1,'-1',-36]]

###############################################################################
# sub-function definition
###############################################################################
# SA reset
def sa_reset():
    sa.write('*rst')
    return

# delay in second    
def delay(second):
    time.sleep(second)
    return

# frequency setup
def freq_setup(start_f,stop_f):
    sa.write('sens:freq:star '+str(float(start_f)*1000000))
    sa.write('sens:freq:stop '+str(float(stop_f)*1000000))
    return
    
# rbw setup
def rbw_setup(rbw):
    sa.write('sens:bwid:res '+str(float(rbw)*1000))
    return

# detecotr selection
def det_setup(detector):
    sa.write('sens:det '+str(detector))
    return
    
# sweep_time setup
def sweep_time_setup(sweep_time):
    sa.write('sens:swe:time '+str(sweep_time))
    return
    
# ext_gain calibration
def ext_gain_compensation(ext_gain):
    sa.write('sens:corr:sa:rf:gain '+str(ext_gain))
    return
    
# auto scale
def scale_setup():
    sa.write('sens:spur:pow:rang:auto on')
    return

# reference level setup
def ref_level_setup(limit):
    sa.write(':disp:view:wind:trac:y:rlev '+str(float(limit)+30))
    return
    
# continous test on
def cont_setup():
    sa.write(':init:cont on')
    return

# marker on
def marker_on():
    sa.write(':calc:mark aoff')
    sa.write(':calc:mark:stat on')
    return
    
# max finding
def max_finding():
    sa.write(':calc:mark:cps on')
    delay(0.5)
    max_value='%.2f' % float(sa.ask(':calc:mark:y?'))
    return max_value
    
# result judgement
def result_judgement(spec,test_value):
    if (float(test_value)<float(spec)):
        test_result='PASS'
    else:
        test_result='FAIL'
    return test_result
    




###############################################################################
# main test
###############################################################################
sa=instrument(str(sa_addr))
sa_reset()
delay(1)

for item in test_para:
    freq_setup(item[0],item[1])
    rbw_setup(item[2])
    det_setup(item[3])
    sweep_time_setup(item[4])
    ext_gain_compensation(item[5])
    scale_setup()
    cont_setup()
    ref_level_setup(item[6])
    marker_on()
    delay(float(item[4])*5)
    test_value=max_finding()
    test_result=result_judgement(item[6],test_value)
    print item,test_value,test_result
    
    
print 'test finished!'



















