"""
quartile is a module for quartiling an attribute based on a target
usage: new_df=quartile.quartile(src_df, 'detailed_occ_cd', 'target')
"""
import numpy as np
import pandas as pd

def load_file(filepath):
	data=pd.read_csv(filepath)
	data.columns = ['age', 'worker_class', 'detailed_ind_cd', 'detailed_occ_cd',
                'education', 'wage', 'enrolled_last_wk', 'marital_status', 
                'major_ind_cd', 'major_occ_cd', 'race', 'hispanic_origin',
                'sex', 'member_labour_union', 'unemployment_reason', 'employment_status', 
                'capital_gains',  'capital_losses',  'dividends', 'tax_filer',
                'region_prev_res', 'state_prev_res', 'detailed_hsld_stat', 'detailed_hsld_smry', 
                'migration_cd_msa', 'migration_cd_reg', 'migration_cd_within_reg', 'same_house_prev_yr', 
                'migration_prev_reg_sunbelt', 'no_persons_worked_for_employer', 'family_members_under18', 
                'weight','birth_country_father', 'birth_country_mother','birth_country', 'citizenship',
                'occupation', 'fill_inc_question_veteran_admin', 'veteran_benefit',  
                'weeks_worked_in_yr',  'year', 'target']
	data1=data.drop_duplicates(keep='first').reset_index(drop=True)
	data1['target']=data1['target'].replace(' - 50000.',0)
	data1['target']=data1['target'].replace(' 50000+.',1)
	return data1

