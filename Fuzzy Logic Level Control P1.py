# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 15:24:43 2020
Version 2:
Antecedent:
    Error=[-4,-3,-2,-1,0,1,2,3,4]
    derror=[-0.008,-0.007,-0.006 .... 0 .... 0.006, 0.007,0.008]
    dvoltage=[-3,-2,-1,0,1,2,3]
Member function:
    Error: 3 categaries 
    Change rate(aka:delta error): 3 categaries
    Voltage: 5 categaries
Rules: 
    7 designed rules
@author: damien
"""
#----------------------Import libraries---------------------------------------+
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from scipy.integrate import odeint
import matplotlib.pyplot as plt

#------------------Initial conditions-----------------------------------------+
hi=0                                    #Current height
h_dot=0                                 #Height change rate
h_des=4                                 #Desired height
h_d=h_des-hi                            #Delta height
start=0
end=1999
freq=20
n=(end+1)*freq
t=np.linspace(start,end,n)
h_list=[]                               #List of Current height
v_list=[]                               #List of Current voltgate

#New Antecedent/Consequent objects hold universe variables and membership func.
error = ctrl.Antecedent(np.arange(-4, 5, 1), 'e')
derror = ctrl.Antecedent(np.arange(-0.006, 0.007, 0.001), 'er')
dvoltage = ctrl.Consequent(np.arange(-3, 4, 1), 'dvoltage')


###Custom membership functions can be built interactively with a familiar###
#-----------------Membership function for error term--------------------------+
error['poor'] = fuzz.trapmf(error.universe, [-4, -4, -2, -1])
error['average'] = fuzz.trimf(error.universe, [-1, 0, 1])
error['good'] = fuzz.trapmf(error.universe, [1, 2, 4, 4])

#-----------------Membership function for delta error term--------------------+
derror['poor'] = fuzz.trapmf(derror.universe, [-0.006, -0.006, -0.003, 0])
derror['average'] = fuzz.trimf(derror.universe, [-0.003, 0, 0.003])
derror['good'] = fuzz.trapmf(derror.universe, [0, 0.003, 0.006, 0.006])

#-----------------Membership function for voltage term------------------------+
dvoltage['ll'] = fuzz.trapmf(dvoltage.universe, [-3, -3, -2, -1])
dvoltage['lh'] = fuzz.trimf(dvoltage.universe, [-2, -1, 0])
dvoltage['medium'] = fuzz.trimf(dvoltage.universe, [-1, 0, 1])
dvoltage['hl'] = fuzz.trimf(dvoltage.universe, [0, 1, 2])
dvoltage['hh'] = fuzz.trapmf(dvoltage.universe, [1, 2, 3, 3])

#-----------------Define complex rules----------------------------------------+
rule1 = ctrl.Rule(error['poor'] & derror['poor'], dvoltage['ll'])
rule2 = ctrl.Rule(error['poor'] & derror['average'], dvoltage['lh'])
rule3 = ctrl.Rule(error['average'] & derror['poor'], dvoltage['lh'])
rule4 = ctrl.Rule(error['average'] & derror['average'], dvoltage['medium'])
rule5 = ctrl.Rule(error['good'] & derror['average'], dvoltage['hl'])
rule6 = ctrl.Rule(error['average'] & derror['good'], dvoltage['hl'])
rule7 = ctrl.Rule(error['good'] & derror['good'], dvoltage['hh'])

#-----------------Control system framework------------------------------------+
height_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7])
height = ctrl.ControlSystemSimulation(height_ctrl)

#Create a function to constantly compute voltage with the current height error
#and height change rate. 
def volt_compute(error, chan_error):
  height.input['e'] = error
  height.input['er'] = chan_error
  height.compute()
  return height.output['dvoltage']

def check_bounds(volt):
    if volt<0:
        volt=0
    elif volt>48:
        volt=48
    return volt
        
#Compute the inital voltage condition
vi=0

#--------------------Create a ODE model---------------------------------------+
def model(h,t,v):
    a,b = 0.1, 0.01        #a,b: constant numbers
    r = 5                  #Radius: 5 meters
    dhdt = (b*v-a*np.sqrt(h))/(np.pi*r**2)
    return dhdt
  
#Use ODEINT to compute new height and use fuzzy logic to compute voltage ######
#Height change rate is computed by difference between current and previous height
for i in range(1,n):
    tspan = [t[i-1],t[i]]
    h = odeint(model,hi,tspan,args=(vi,))
    dhdt = h[1][0]-hi
    hi = h[1][0]
    h_d = h_des-hi
    vi += volt_compute(h_d,dhdt)
    vi=check_bounds(vi)

    h_list.append(hi)
    v_list.append(vi)

plt.plot(t[1:],h_list)
plt.show()
plt.plot(t[1:],v_list)