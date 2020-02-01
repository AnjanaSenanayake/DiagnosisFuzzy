#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


# In[198]:


# Antecedent objects hold universe variables and membership
heart_rate = ctrl.Antecedent(np.arange(0, 101, 1), 'heart rate')
blood_pressure = ctrl.Antecedent(np.arange(0, 101, 1), 'blood pressure')
spo2_level = ctrl.Antecedent(np.arange(0, 101, 1), 'spo2 level')
glucose_level = ctrl.Antecedent(np.arange(0, 101, 1), 'glucose level')
temperature = ctrl.Antecedent(np.arange(0, 101, 1), 'temperature')
age = ctrl.Antecedent(np.arange(0, 101, 1), 'age')

# Consequent object
health = ctrl.Consequent(np.arange(0, 101, 1), 'health')


# In[199]:


## membership function populations, normalize to 100%
# 80 - 100 pulses/min safe region, max = 130
heart_rate['low'] = fuzz.trimf(health.universe, [0, 0, 70])
heart_rate['good'] = fuzz.trimf(health.universe, [0, 70, 100])
heart_rate['high'] = fuzz.trimf(health.universe, [70, 100, 100])

# 80 - 120 mmHg safe region, max = 180(220-40) for age of 40
blood_pressure['low'] = fuzz.trimf(health.universe, [0, 0, 56])
blood_pressure['good'] = fuzz.trimf(health.universe, [0, 56, 100])
blood_pressure['high'] = fuzz.trimf(health.universe, [56, 100, 100])

# 94 - 99 safe region, max = 100
spo2_level['low'] = fuzz.trimf(health.universe, [0, 0, 94])
spo2_level['medium'] = fuzz.trimf(health.universe, [0, 94, 100])
spo2_level['high'] = fuzz.trimf(health.universe, [94, 100, 100])

# 70 - 130 mgdL safe region, max = 200
glucose_level['low'] = fuzz.trimf(health.universe, [0, 0, 50])
glucose_level['good'] = fuzz.trimf(health.universe, [0, 50, 100])
glucose_level['high'] = fuzz.trimf(health.universe, [50, 100, 100])

# 35 - 38 centigrade safe region, max = 40
temperature['low'] = fuzz.trimf(health.universe, [0, 0, 92])
temperature['good'] = fuzz.trimf(health.universe, [0, 92, 100])
temperature['high'] = fuzz.trimf(health.universe, [92, 100, 100])

# max = 100
age['young'] = fuzz.trimf(health.universe, [0, 0, 35])
age['adult'] = fuzz.trimf(health.universe, [0, 35, 100])
age['senior'] = fuzz.trimf(health.universe, [35, 100, 100])

# max = 100
health['bad'] = fuzz.trimf(health.universe, [0, 0, 70])
health['average'] = fuzz.trimf(health.universe, [0, 70, 100])
health['good'] = fuzz.trimf(health.universe, [70, 100, 100])


# In[200]:


# view of heart rate
heart_rate.view()


# In[201]:


# view of blood pressure
blood_pressure.view()


# In[202]:


spo2_level.view()


# In[203]:


glucose_level.view()


# In[204]:


temperature.view()


# In[205]:


age.view()


# In[206]:


health.view()


# In[207]:


rule1 = ctrl.Rule(spo2_level['low'], health['bad'])
rule2 = ctrl.Rule(heart_rate['high'] & age['adult'], health['average'])
rule3 = ctrl.Rule(heart_rate['high'] & age['senior'], health['bad'])
rule4 = ctrl.Rule(blood_pressure['low'], health['bad'])
rule5 = ctrl.Rule(blood_pressure['high'], health['bad'])
rule6 = ctrl.Rule(temperature['low'], health['bad'])
rule7 = ctrl.Rule(temperature['high'], health['bad'])
rule8 = ctrl.Rule(glucose_level['low'], health['bad'])
rule9 = ctrl.Rule(glucose_level['high'], health['bad'])
rule10 = ctrl.Rule(blood_pressure['high'] & age['senior'], health['bad'])
rule11 = ctrl.Rule(blood_pressure['low'] & age['senior'], health['bad'])
rule12 = ctrl.Rule(temperature['low'] & age['senior'], health['bad'])
rule13 = ctrl.Rule(temperature['high'] & age['senior'], health['bad'])
rule14 = ctrl.Rule(spo2_level['high'] & heart_rate['good'] & blood_pressure['good'] & glucose_level['good'] & temperature['good'], health['good'])
rule15 = ctrl.Rule(spo2_level['low'] & heart_rate['low'] & blood_pressure['low'] & glucose_level['low'] & temperature['low'], health['bad'])

rule10.view()


# In[208]:


health_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12, rule13, rule14, rule15])
health_compute = ctrl.ControlSystemSimulation(health_ctrl)


# In[232]:


# Pass inputs to the ControlSystem using Antecedent labels with Pythonic API
# Note: if you like passing many inputs all at once, use .inputs(dict_of_data)
health_compute.input['heart rate'] = 70
health_compute.input['blood pressure'] = 54
health_compute.input['spo2 level'] = 95
health_compute.input['glucose level'] = 50
health_compute.input['temperature'] = 92
health_compute.input['age'] = 30

# Crunch the numbers
health_compute.compute()


# In[233]:


print(health_compute.output['health'])
health.view(sim = health_compute)

