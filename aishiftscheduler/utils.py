# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/12_utils.ipynb.

# %% auto 0
__all__ = ['pwd_context', 'print_schedule_shifts', 'gap_minutes', 'print_schedule_slots', 'hash', 'verify']

# %% ../nbs/12_utils.ipynb 5
from collections import defaultdict
import pandas as pd
# import matplotlib as mpl
# import matplotlib.pyplot as plt
from copy import copy
# import time
# import math
# from pprint import pprint
## !pip install -U "ray"
# import ray
# import json

from fastcore.basics import patch
import aishiftscheduler.config as cf
# import aishiftscheduler.policy as pol
# import aishiftscheduler.visualization as vis

# %% ../nbs/12_utils.ipynb 6
def print_schedule_shifts(df, pars):
  mask = df.columns.str.contains('Allocd_t')
  resource_allocs = list(df.columns[mask])
  sched = copy(df)
  schedule = sched[['dt']+resource_allocs]

  print(f"SCHEDULE SHIFTS:")
  print(f"===============")
  for res_alloc in resource_allocs:
    _,_,id,resType,_,_,_ = res_alloc.split('_')
    resName = id+'_'+resType
    print(f'\n************** {resName}:')
    sched_list = list(schedule.loc[
      schedule[res_alloc] == True,
      ['dt', res_alloc]
    ]['dt'])
    if len(sched_list) > 0:
      ts_1 = sched_list[0]
      dow_1 = sched_list[0].day_of_week
      print(f"{(sched_list[0]-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}")
      for ts in sched_list:
        dow = ts.day_of_week
        if dow != dow_1:
          print(f"{(ts_1).strftime('%a %b %d %Hh%M')}\n")
          print(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}")
        dow_1 = dow
        ts_1 = ts
      print(f"{(sched_list[-1]).strftime('%a %b %d %Hh%M')}")
  print(f'\n{cf.CONTIGUOUS_REWARD=}')
  print(f'{pars.MAX_DAILY_SLOT_RUN=} ({pars.RESOLUTION}s)')
  print(f'{cf.TH_CumSlots_SPEC=}')
  print(f'{cf.TH_SickProb_SPEC=}')
  print(f'{cf.TH_CumMerits_SPEC=}')
  print(f'{cf.TH_ContSlots_SPEC=}')
  print(f'{cf.TH_Select_SPEC=}')

# %% ../nbs/12_utils.ipynb 7
def gap_minutes(resolution):
  if resolution == 'QUARTER_HOUR':
    return 15
  elif resolution == 'HOUR':
    return 60
  elif resolution == 'BLOCK_8_HOUR':
    return 480
  else:
    print(f'ERROR: Invalid RESOLUTION: {cf.RESOLUTION}')

# %% ../nbs/12_utils.ipynb 8
def print_schedule_slots(df, pars):
  gap_mins = gap_minutes(pars.RESOLUTION)
  mask = df.columns.str.contains('Allocd_t')
  resource_allocs = list(df.columns[mask])
  sched = copy(df)
  schedule = sched[['dt']+resource_allocs]

  print(f"SCHEDULE SLOTS:")
  print(f"===============")
  n_gaps = 0
  for res_alloc in resource_allocs:
    _,_,id,resType,_,_,_ = res_alloc.split('_')
    resName = id+'_'+resType
    print(f'\n************** {resName}:')
    sched_list = list(schedule.loc[
      schedule[res_alloc] == True,
      ['dt', res_alloc]
    ]['dt'])
    if len(sched_list) > 0:
      ## print each slot and indicate gaps
      ts_1 = sched_list[0]
      dow_1 = -1
      for ts in sched_list:
        dow = ts.day_of_week
        if dow != dow_1: print('')
        if (int((ts.to_datetime64() - ts_1.to_datetime64())/(1e9*60)) > gap_mins)\
          and (dow == dow_1):
          n_gaps += 1
          print(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')} GAP")
        else:
          print(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}")
        dow_1 = dow
        ts_1 = ts
  print(f'\nTOTAL NUMBER OF GAPS FOR ALL RESOURCES: {n_gaps}')
  print(f'{cf.CONTIGUOUS_REWARD=}')
  print(f'{pars.MAX_DAILY_SLOT_RUN=} ({pars.RESOLUTION}s)')
  print(f'{cf.TH_CumSlots_SPEC=}')
  print(f'{cf.TH_SickProb_SPEC=}')
  print(f'{cf.TH_CumMerits_SPEC=}')
  print(f'{cf.TH_ContSlots_SPEC=}')
  print(f'{cf.TH_Select_SPEC=}')

# %% ../nbs/12_utils.ipynb 9
## this is utils.py from tut
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
