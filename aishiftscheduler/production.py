# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_production.ipynb.

# %% auto 0
__all__ = ['app', 'dui', 'Pars', 'prepare_schedule', 'update_parameters_from_user_input', 'root', 'get_default_user_input',
           'find_schedule']

# %% ../nbs/10_production.ipynb 7
from collections import defaultdict
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from copy import copy
import time
import math
from pprint import pprint
import ray
import json
from io import StringIO
import aishiftscheduler.loader as ldr
import aishiftscheduler.config as cf
import aishiftscheduler.visualization as vis
import aishiftscheduler.model as mod
import aishiftscheduler.policy as pol
import aishiftscheduler.inferencer as inf
import aishiftscheduler.trainer as trn
import aishiftscheduler.evaluator as evl
import aishiftscheduler.parameters as par
from PIL import Image
import aishiftscheduler.utils as utl

# from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
# from pydantic import BaseModel
# from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
# from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

# # sqlalchemy and ORM (database.py from tut)
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, Session
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:p@localhost/sai_db2'
# engine = create_engine(SQLALCHEMY_DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

import aishiftscheduler.dbmodels as dbm
from .database import engine

import aishiftscheduler.schemas as sch

import aishiftscheduler.routers as rts
import aishiftscheduler.envconfig as envcfg

# from pydantic import BaseSettings
# from pydantic_settings import BaseSettings

# class Settings(BaseSettings):
#     database_password: str = "localhost"
#     database_username: str = "postgres"
#     secret_key: str = "123jklj902734789df"

# settings = Settings()
# print(settings.database_password)

# %% ../nbs/10_production.ipynb 11
def prepare_schedule(pars):
    start = time.time()
    if 'TRAIN' in cf.MODES:
        print('############################## TRAIN ##############################')
        ## COMMENTED OUT TEMPORARILY FOR QUICKER TESTING
        # L = 2 #5 #20 #10 #5 #2 #3 #2db #10pub
        # T = 7*pars.SLOTS_PER_DAY #5 #7*96
        # First_n_t = int(1.2*T)
        # Last_n_t = int(1*T) ##make whole multiple of T to look better in chart
        
        # trn_Best_theta, trn_Worst_theta, trn_Df_first_n_t, trn_Df_last_n_t = \
        #     trn.train_schedule(L, T, First_n_t, Last_n_t, pars)
        
        # trn_Best_theta_df = pd.DataFrame({
        #     'thCumSlots': [trn_Best_theta[0]], 
        #     'thSickProb': [trn_Best_theta[1]], 
        #     'thCumMerits': [trn_Best_theta[2]], 
        #     'thContSlots': [trn_Best_theta[3]],
        #     'thSelect': [trn_Best_theta[4]]
        # })
        # ldr.save_best_theta(cf.PATH_best_theta_data, trn_Best_theta_df)

        # print(f'{trn_Best_theta=}')
        # print(f'{trn_Df_first_n_t.shape=}')

    if 'EVALU' in cf.MODES:
        print('############################## EVALU ##############################')
        ## COMMENTED OUT TEMPORARILY FOR QUICKER TESTING
        # L = 2 #20 #5 #2 #2db #10pub
        # T = 7*pars.SLOTS_PER_DAY #=672
        # First_n_t = int(.11*L*T)
        
        # evl_Best_theta_opt, evl_Worst_theta_opt, evl_Df_opt = \
        #     evl.evalu_schedule_opt(L, T, First_n_t, trn_Best_theta, pars)
        # print(f'{evl_Best_theta_opt=}')
        # print(f'{evl_Df_opt.shape=}')
    
        # evl_Best_theta_non, evl_Worst_theta_non, evl_Df_non = \
        #     evl.evalu_schedule_non(L, T, First_n_t, trn_Worst_theta, pars)
        # print(f'{evl_Best_theta_non=}')
        # print(f'{evl_Df_non.shape=}')

        # ## single sample-path
        # L = 1 #20 #5 #2 #2db #10pub
        # T = 7*pars.SLOTS_PER_DAY #=672
        # First_n_t = int(1*L*T)
        
        # evl_Best_theta_opt, evl_Worst_theta_opt, evl_Df_opt = \
        #     evl.evalu_schedule_opt(L, T, First_n_t, trn_Best_theta, pars)
        # print(f'{evl_Best_theta_opt=}')
        # print(f'{evl_Df_opt.shape=}')
    
        # evl_Best_theta_non, evl_Worst_theta_non, evl_Df_non = \
        #     evl.evalu_schedule_non(L, T, First_n_t, trn_Worst_theta, pars)
        # print(f'{evl_Best_theta_non=}')
        # print(f'{evl_Df_non.shape=}')

        # print(evl_Df_opt[evl_Df_opt['t']==T-1][['Ccum']])
        # print(evl_Df_non[evl_Df_non['t']==T-1][['Ccum']])
        
    if 'INFER' in cf.MODES:
        print('############################## INFER ##############################')
        L = 1
        T = 7*pars.SLOTS_PER_DAY
        First_n_t = int(1*L*T)
    
        stored_best_theta_tuple = ldr.load_best_theta(cf.PATH_best_theta_data)
        stored_best_theta = pol.Policy(None).build_theta({
            'thCumSlots': stored_best_theta_tuple[0],
            'thSickProb': stored_best_theta_tuple[1],
            'thCumMerits': stored_best_theta_tuple[2],
            'thContSlots': stored_best_theta_tuple[3],
            'thSelect': stored_best_theta_tuple[4]
            })
        
        inf_Best_theta_evalu_opt, inf_Df_evalu_opt, prepped_sched = \
            inf.infer_schedule(L, T, First_n_t, stored_best_theta, pars)
    
        print(f'{inf_Best_theta_evalu_opt=}')
        print(f'{inf_Df_evalu_opt.shape=}')
        ## print(f'{prepped_sched=}')
        utl.print_schedule_shifts(inf_Df_evalu_opt, pars)
        ## utl.print_schedule_slots(inf_Df_evalu_opt, pars)
    end = time.time(); print(f'EXECUTION TIME: {end - start} seconds')
    return prepped_sched

# %% ../nbs/10_production.ipynb 12
## Update the Parameters instance, `Pars` with the latest user input.
def update_parameters_from_user_input(pars, user_input):
  error = None 
  pars.START_DATE_TIME = user_input.start
  sd = pd.to_datetime(user_input.start)
  if not sd.strftime('%a')=='Mon':
    error = f"ERROR: {user_input.start} is a {sd.strftime('%A')}. It should be a Monday."
    print(error)
    return error
  for_now_sd = pd.to_datetime('2023-12-04')
  if not sd==for_now_sd:
    error = f"ERROR: Start date must be {for_now_sd} for now."
    print(error) 
    return error

  spd = int(user_input.slots_per_day)
  if not spd == 24:
    error = f"ERROR: Slots per day must be 24 for now."
    print(error)
    return error
  pars.SLOTS_PER_DAY = spd
  
  mdsr = int(user_input.max_daily_slot_run)
  if not mdsr <= spd:
    error = f"ERROR: 'Max daily slot run' must be less than or equal to 'Slots per day'"
    print(error)
    return error
  pars.MAX_DAILY_SLOT_RUN = mdsr

  resource_type_and_ids = user_input.resources.split(';')
  resource_types = []
  resource_ids = []
  resource_type_counts = []
  for itm in resource_type_and_ids:
      res_type, res_ids = itm.split(':')
      resource_types.append(res_type.strip())
      sep_ids = res_ids.split(','); ##print(f'{sep_ids=}')
      for rid in sep_ids:
          resource_ids.append(rid.strip())
      resource_type_counts.append(len(sep_ids))
  print(f'{resource_types=}')
  print(f'{resource_type_counts=}')
  print(f'{resource_ids=}')
  if len(resource_types) > cf.MAX_RESOURCE_TYPES:
    error = f"ERROR: The number of resource types should not exceed {cf.MAX_RESOURCE_TYPES}.\nYou entered the following resource types: {resource_types}"
    print(error)
    return error
  if len(resource_ids) > cf.MAX_RESOURCE_IDS:
    error = f"ERROR: The number of resources should not exceed {cf.MAX_RESOURCE_IDS}.\nYou entered the following resources: {resource_ids}"
    print(error)
    return error
  pars.RESOURCE_TYPES = resource_types; print(f'{pars.RESOURCE_TYPES=}')
  pars.RESOURCE_TYPE_COUNTS = resource_type_counts; print(f'{pars.RESOURCE_TYPE_COUNTS=}')
  pars.TYPES = []
  for i in range(len(pars.RESOURCE_TYPES)):
    additional_types = [pars.RESOURCE_TYPES[i]]*pars.RESOURCE_TYPE_COUNTS[i]
    for item in additional_types:
      pars.TYPES.append(item)
  print(f'{pars.TYPES=}')
  pars.RESOURCE_IDS = resource_ids; print(f'{pars.RESOURCE_TYPE_COUNTS=}')

  rates = user_input.demands_per_busyness.split(',')
  if '' in rates:
    error = f"ERROR: There should be a demand-per-busyness for each resource type (role).\nYou entered the following values: {demands_per_busyness}"
    print(error)
    return error
  rates = list(map(lambda x: float(x), rates))
  print(f'{rates=}')
  if len(rates) != len(pars.RESOURCE_TYPES):
    error = f"ERROR: The number of demands-per-busyness should be the same as the number of resource types (roles).\nYou entered the following values: {demands_per_busyness}"
    print(error)
    return error
  pars.DEMANDS_PER_BUSYNESS = rates
  pars.DEMAND_PER_BUSYNESS = {e: pars.DEMANDS_PER_BUSYNESS[i] for i,e in enumerate(pars.RESOURCE_TYPES)}

  rates = user_input.demands_per_volume.split(',')
  if '' in rates:
    error = f"ERROR: There should be a demand-per-volume for each resource type (role).\nYou entered the following values: {demands_per_volume}"
    print(error)
    return error
  rates = list(map(lambda x: float(x), rates))
  print(f'{rates=}')
  if len(rates) != len(pars.RESOURCE_TYPES):
    error = f"ERROR: The number of demands-per-volume should be the same as the number of resource types (roles).\nYou entered the following values: {demands_per_volume}"
    print(error)
    return error
  pars.DEMANDS_PER_VOLUME = rates
  pars.DEMAND_PER_VOLUME = {e: pars.DEMANDS_PER_VOLUME[i] for i,e in enumerate(pars.RESOURCE_TYPES)}

  rates = user_input.demands_per_revenue.split(',')
  if '' in rates:
    error = f"ERROR: There should be a demand-per-revenue for each resource type (role).\nYou entered the following values: {demands_per_revenue}"
    print(error)
    return error
  rates = list(map(lambda x: float(x), rates))
  print(f'{rates=}')
  if len(rates) != len(pars.RESOURCE_TYPES):
    error = f"ERROR: The number of demands-per-revenue should be the same as the number of resource types (roles).\nYou entered the following values: {demands_per_revenue}"
    print(error)
    return error
  pars.DEMANDS_PER_REVENUE = rates
  pars.DEMAND_PER_REVENUE = {e: pars.DEMANDS_PER_REVENUE[i] for i,e in enumerate(pars.RESOURCE_TYPES)}

  expenses = user_input.resource_expenses.split(',')
  if '' in expenses:
    error = f"ERROR: There should be a resource expense for each resource type (role).\nYou entered the following values: {resource_expenses}"
    print(error)
    return error  
  expenses = list(map(lambda x: float(x), expenses))
  print(f'{expenses=}')
  if len(expenses) != len(pars.RESOURCE_TYPES):
    error = f"ERROR: The number of resource expenses should be the same as the number of resource types (roles).\nYou entered the following values: {resource_expenses}"
    print(error)
    return error
  pars.RESOURCE_EXPENSES = expenses
  pars.RESOURCE_EXPENSE = {e: pars.RESOURCE_EXPENSES[i] for i,e in enumerate(pars.RESOURCE_TYPES)}

  pars.aNAMES = [tup[0]+'_'+tup[1] for tup in zip(pars.TYPES, pars.RESOURCE_IDS)]; print(f'{pars.aNAMES=}')
  pars.bNAMES = pars.RESOURCE_TYPES; print(f'{pars.bNAMES=}')
  pars.abNAMES = [] ##to DEMAND b
  for a in pars.aNAMES:
    a0,a1 = a.split('_')
    for b in pars.bNAMES:
      if(a0==b):
        abn = (a + '___' + b)
        pars.abNAMES.append(abn)
  print(f'{pars.abNAMES=}')
  pars.LABELS = pars.setup_plot_labels()
  return error

# %% ../nbs/10_production.ipynb 13
# class ParamConfig():#will be copy of Parameters class
# class UserInput():
#     pass

# %% ../nbs/10_production.ipynb 15
app = FastAPI()

## allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# %% ../nbs/10_production.ipynb 16
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
## dbm.Base.metadata.create_all(bind=engine) ##not needed, now we use alembic 

# %% ../nbs/10_production.ipynb 17
app.include_router(rts.userinput_router)
app.include_router(rts.user_router)
app.include_router(rts.auth_router)

# %% ../nbs/10_production.ipynb 18
@app.get("/")
def root():
    return "BusinessN AI Schedule Agent (API) v1.0.0"

# %% ../nbs/10_production.ipynb 19
dui = sch.UserInputBase(
  start="2023-12-04", ##2023-12-11
  slots_per_day=24,
  max_daily_slot_run=9, ##8
  resources="Manager: Matt; AssistMngr: Mike, Tanner; RetailAssoc: Jake, James, Jane, John, Jim, Jenny, Jeremy, Judy, Julie, Jeffrey",
  ## resources = 'Manager: Matt; AssistMngr: Mike, Tanner; RetailAssoc: Jake, James, Jane, John, Jim, Jenny, Jeremy, Judy, Julie',
  ## resources = 'Manager: John, Penelope; SalesPerson: Sally, Sarah, Jim, Costa',
  ## resources = 'SupChief: Ruan, Francine; Sup: Azra, Wendie, Penny, Sally',
  ## resources = 'ChiefTeller: Ruan, Francine; Teller: Azra, Wendie, Penny, Sally',

  ## demands_per_busyness = '.2, 4',
  demands_per_busyness="0.005, 0.008, 0.02",

  ## demands_per_volume = '.02, .4',
  demands_per_volume="0.03, 0.08, 0.2",

  ## demands_per_revenue = '.05, .8',
  demands_per_revenue="0.00005, 0.0001, 0.0008",

  ## resource_expenses = '35.17, 23.85'
  resource_expenses="25.0, 20.0, 18.0",
)

# %% ../nbs/10_production.ipynb 20
@app.get("/defaultuserinput")
def get_default_user_input():
    return {
        "start": dui.start,
        "slots_per_day": dui.slots_per_day,
        "max_daily_slot_run": dui.max_daily_slot_run,
        "resources": dui.resources,
        "demands_per_busyness": dui.demands_per_busyness,
        "demands_per_volume": dui.demands_per_volume,
        "demands_per_revenue": dui.demands_per_revenue,
        "resource_expenses": dui.resource_expenses
    }

# %% ../nbs/10_production.ipynb 21
## Create a Parameter instance & initialize with default pars.
## The `Pars` instance will be passed between various modules
Pars = par.Parameters()

# %% ../nbs/10_production.ipynb 22
@app.post("/schedule")
def find_schedule(user_input: sch.UserInputBase):
    error = update_parameters_from_user_input(Pars, user_input)
    if error == None:
        ## store latest user input to postgres
        sched = prepare_schedule(Pars)
        ## prepare_schedule(Pars)
        return sched
    else:
        return error
