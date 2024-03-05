# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/09_inferencer.ipynb.

# %% auto 0
__all__ = ['get_best_theta_Alloc', 'do_infer', 'prepare_schedule_shifts_as_text', 'prepare_schedule_slots_as_text',
           'prepare_schedule_slots_as_json', 'infer_schedule']

# %% ../nbs/09_inferencer.ipynb 5
from collections import defaultdict
import pandas as pd
from copy import copy
import time

import aishiftscheduler.config as cf
import aishiftscheduler.model as mod
import aishiftscheduler.policy as pol
import aishiftscheduler.utils as utl

# %% ../nbs/09_inferencer.ipynb 6
def get_best_theta_Alloc():
  best_theta_Alloc = \
    pol.Policy(None).build_theta({
      'thCumSlots': cf.BEST_THETA_Alloc[0],
      'thSickProb': cf.BEST_THETA_Alloc[1],
      'thCumMerits': cf.BEST_THETA_Alloc[2],
      'thContSlots': cf.BEST_THETA_Alloc[3],
      'thSelect': cf.BEST_THETA_Alloc[4]
    })
  return best_theta_Alloc

# %% ../nbs/09_inferencer.ipynb 7
def do_infer(L, T, best_theta_Alloc, pars):
  M = mod.Model(pars)
  P = pol.Policy(M)
  ## DEM = DemandSimulator(seed=SEED_EVALU)
  ## MER = MeritSimulator(seed=SEED_EVALU)
  
  thetasOpt = []; thetasOpt.append(best_theta_Alloc) ##from storage
  return \
    P.perform_grid_search_sample_paths('X__Alloc', thetasOpt, L, T, pars)

# %% ../nbs/09_inferencer.ipynb 8
from io import StringIO
def prepare_schedule_shifts_as_text(df, buf, pars):
  mask = df.columns.str.contains('Allocd_t')
  resource_allocs = list(df.columns[mask])
  sched = copy(df)
  schedule = sched[['dt']+resource_allocs]

  buf.write(f"SCHEDULE SHIFTS:\n")
  buf.write(f"================\n")
  for res_alloc in resource_allocs:
    _,_,id,resType,_,_,_ = res_alloc.split('_')
    resName = id+'_'+resType
    buf.write(f'\n************** {resName}:\n')
    sched_list = list(schedule.loc[
      schedule[res_alloc] == True,
      ['dt', res_alloc]
    ]['dt'])
    if len(sched_list) > 0:
      ts_1 = sched_list[0]
      dow_1 = sched_list[0].day_of_week
      buf.write(f"{(sched_list[0]-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}\n")
      for ts in sched_list:
        dow = ts.day_of_week
        if dow != dow_1:
          buf.write(f"{(ts_1).strftime('%a %b %d %Hh%M')}\n\n")
          buf.write(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}\n")
        dow_1 = dow
        ts_1 = ts
      buf.write(f"{(sched_list[-1]).strftime('%a %b %d %Hh%M')}\n")
  buf.write(f'\n{cf.CONTIGUOUS_REWARD=}\n')
  buf.write(f'{pars.MAX_DAILY_SLOT_RUN=} ({pars.RESOLUTION}s)\n')
  buf.write(f'{cf.TH_CumSlots_SPEC=}\n')
  buf.write(f'{cf.TH_SickProb_SPEC=}\n')
  buf.write(f'{cf.TH_CumMerits_SPEC=}\n')
  buf.write(f'{cf.TH_ContSlots_SPEC=}\n')
  buf.write(f'{cf.TH_Select_SPEC=}\n')
  return buf.getvalue()

# %% ../nbs/09_inferencer.ipynb 9
from io import StringIO
def prepare_schedule_slots_as_text(df, buf):
  gap_mins = utl.gap_minutes(cf.RESOLUTION)
  mask = df.columns.str.contains('Allocd_t')
  resource_allocs = list(df.columns[mask])
  sched = copy(df)
  schedule = sched[['dt']+resource_allocs]

  buf.write(f"SCHEDULE SLOTS:\n")
  buf.write(f"===============\n")
  n_gaps = 0
  for res_alloc in resource_allocs:
    _,_,id,resType,_,_,_ = res_alloc.split('_')
    resName = id+'_'+resType
    buf.write(f'\n************** {resName}:\n')
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
        if dow != dow_1: buf.write('\n')
        if (int((ts.to_datetime64() - ts_1.to_datetime64())/(1e9*60)) > gap_mins)\
          and (dow == dow_1):
          n_gaps += 1
          buf.write(f"{(ts-pd.Timedelta(cf.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')} GAP\n")
        else:
          buf.write(f"{(ts-pd.Timedelta(cf.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}\n")
        dow_1 = dow
        ts_1 = ts
  buf.write(f'\nTOTAL NUMBER OF GAPS FOR ALL RESOURCES: {n_gaps}\n')
  buf.write(f'{cf.CONTIGUOUS_REWARD=}\n')
  buf.write(f'{cf.MAX_DAILY_SLOT_RUN=} ({cf.RESOLUTION}s)\n')
  buf.write(f'{cf.TH_CumSlots_SPEC=}\n')
  buf.write(f'{cf.TH_SickProb_SPEC=}\n')
  buf.write(f'{cf.TH_CumMerits_SPEC=}\n')
  buf.write(f'{cf.TH_ContSlots_SPEC=}\n')
  buf.write(f'{cf.TH_Select_SPEC=}\n')
  return buf.getvalue()

# %% ../nbs/09_inferencer.ipynb 10
def prepare_schedule_slots_as_json(df, pars):
  sched_dict = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
  gap_mins = utl.gap_minutes(pars.RESOLUTION)
  mask = df.columns.str.contains('Allocd_t')
  resource_allocs = list(df.columns[mask])
  sched = copy(df)
  schedule = sched[['dt']+resource_allocs]

  n_gaps = 0
  for res_alloc in resource_allocs:
    _,_,id,resType,_,_,_ = res_alloc.split('_')
    resName = id+'_'+resType
    sched_list = list(schedule.loc[
      schedule[res_alloc] == True,
      ['dt', res_alloc]
    ]['dt'])
    if len(sched_list) > 0:
      ## capture each slot and indicate gaps
      ts_1 = sched_list[0]
      dow_1 = -1
      for ts in sched_list:
        dow = ts.day_of_week
        if (int((ts.to_datetime64() - ts_1.to_datetime64())/(1e9*60)) > gap_mins)\
          and (dow == dow_1):
          n_gaps += 1
          sched_dict['slots'][resName][dow].append(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')} GAP")
        else:
          sched_dict['slots'][resName][dow].append(f"{(ts-pd.Timedelta(pars.DATE_TIME_DELTA)).strftime('%a %b %d %Hh%M')}")
        dow_1 = dow
        ts_1 = ts
  sched_dict['config']['TOTAL NUMBER OF GAPS FOR ALL RESOURCES'] = n_gaps
  sched_dict['config']['CONTIGUOUS_REWARD'] = cf.CONTIGUOUS_REWARD
  sched_dict['config']['MAX_DAILY_SLOT_RUN'] = pars.MAX_DAILY_SLOT_RUN
  sched_dict['config']['RESOLUTION'] = pars.RESOLUTION  
  sched_dict['config']['TH_CumSlots_SPEC'] = cf.TH_CumSlots_SPEC
  sched_dict['config']['TH_SickProb_SPEC'] = cf.TH_SickProb_SPEC
  sched_dict['config']['TH_CumMerits_SPEC'] = cf.TH_CumMerits_SPEC
  sched_dict['config']['TH_ContSlots_SPEC'] = cf.TH_ContSlots_SPEC
  sched_dict['config']['TH_Select_SPEC'] = cf.TH_Select_SPEC
  return sched_dict

# %% ../nbs/09_inferencer.ipynb 11
def infer_schedule(L, T, First_n_t, stored_best_theta, pars):
    start = time.time()
    
    ThetaStar_expCbarcum_evalu_opt, ThetaStar_expCtilcum_evalu_opt, \
    _, _, \
    Best_theta_evalu_opt, Worst_theta_evalu_opt, \
    _, _, \
    _, _, \
    Record_evalu_opt = \
      do_infer(L, T, stored_best_theta, pars)
    Df_evalu_opt = pd.DataFrame.from_records(
        Record_evalu_opt[:First_n_t], columns=pars.LABELS)
    ## print(
    ##   f'{ThetaStar_expCbarcum_evalu_opt.iloc[-1]=:.2f}')    
    ## print_schedule_shifts(Df_evalu_opt)
    end = time.time(); print(f'EXECUTION TIME: {end - start} seconds')

    buf = StringIO()
    ## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    ## prepped_sched = prepare_schedule_shifts_as_text(Df_evalu_opt, buf, pars)
    prepped_sched = prepare_schedule_slots_as_json(Df_evalu_opt, pars)
    ## >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    buf.close()

    return Best_theta_evalu_opt, Df_evalu_opt, prepped_sched
