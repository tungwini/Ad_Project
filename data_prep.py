"""
quartile is a module for quartiling an attribute based on a target
usage: new_df=quartile.quartile(src_df, 'detailed_occ_cd', 'target')
"""
import numpy as np
import pandas as pd
import quartile

def load_file(filepath):
	data=pd.read_csv(filepath)
	data.columns = ['age', 'worker_class', 'detailed_ind_cd', 'detailed_occ_cd',
                'education', 'wage', 'enrolled_last_wk', 'marital_status', 
                'major_ind_cd', 'major_occ_cd', 'race', 'hispanic_origin',
                'sex', 'member_labour_union', 'unemployment_reason', 'employment_status', 
                'capital_gains',  'capital_losses',  'dividends', 'tax_filer',
                'region_prev_res', 'state_prev_res', 'detailed_hsld_stat', 'detailed_hsld_smry', 'weight',
                'migration_cd_msa', 'migration_cd_reg', 'migration_cd_within_reg', 'same_house_prev_yr', 
                'migration_prev_reg_sunbelt', 'no_persons_worked_for_employer', 'family_members_under18', 
                'birth_country_father', 'birth_country_mother','birth_country', 'citizenship',
                'occupation', 'fill_inc_question_veteran_admin', 'veteran_benefit',  
                'weeks_worked_in_yr',  'year', 'target']
	data1=data.drop_duplicates(keep='first').reset_index(drop=True)
	data1['target']=data1['target'].replace(' - 50000.',0)
	data1['target']=data1['target'].replace(' 50000+.',1)
	return data1

def make_variables(row):
	a=row['migration_cd_within_reg']
	b=row['migration_cd_reg']
	c=row['migration_cd_msa']
	new_value=1
	if a in (' ?',' Nonmover'):
		new_value=1
	elif a==' Abroad':
		new_value=0
	elif a==' Different county same state':
		if c in (' MSA to MSA',' Not identifiable'):
			new_value=1
		else:
			new_value=0
	elif a==' Different state in Midwest':
		if ((b==' Different division same region') & (c==' MSA to MSA')):
			new_value=1
		elif ((b==' Different region')&(c in (' MSA to MSA',' MSA to nonMSA'))):
			new_value=1
		else:
			new_value=0
	elif a==' Different state in Northeast':
		if ((b==' Different state same division')&(c in (' MSA to MSA',' MSA to nonMSA'))):
			new_value=1
		elif ((b==' Different region')&(c in (' MSA to MSA',' MSA to nonMSA',' NonMSA to MSA'))):
			new_value=1
		else:
			new_value=0
	elif a==' Different state in West':
		if ((b==' Different state same division')&(c in (' MSA to MSA',' NonMSA to nonMSA'))):
			new_value=1
		elif ((b==' Different division same region')&(c in (' MSA to MSA',' NonMSA to MSA',' Not identifiable'))):
			new_value=1
		elif ((b==' Different region')&(c in (' MSA to MSA',' NonMSA to nonMSA'))):
			new_value=1
		else:
			new_value=0
	elif a==' Different state in South':
		if ((b==' Different state same division')&(c in (' MSA to MSA',' NonMSA to nonMSA',' NonMSA to MSA'))):
			new_value=1
		elif ((b==' Different division same region')&(c==' MSA to MSA')):
			new_value=1
		elif ((b==' Different region')&(row['migration_cd_msa'] in (' MSA to MSA',' MSA to nonMSA',' NonMSA to MSA',' Not identifiable'))):
			new_value=1
		else:
			new_value=0
	elif a==' Same country':
		if row['migration_cd_msa'] in (' MSA to nonMSA',' Not identifiable'):
			new_value=1
		else:
			new_value=0
	else:
		new_value=0
	return new_value

def clean_data(data1):
	data1['region_prev_res_1']=np.where(data1['region_prev_res']=='Not in universe',1,0)
	data1['marital_status_1']=np.where(data1['marital_status']=='Married-civilian spouse present',1,0)
	data1['marital_status_2']=np.where(data1['marital_status'].isin(['Divorced','Married-spouse absent']),1,0)
	data1['worker_class_1']=np.where(data1['worker_class']=='Federal government',1,0)
	data1['worker_class_2']=np.where(data1['worker_class']=='Self-employed-incorporated',1,0)
	data1['worker_class_3']=np.where(data1['worker_class'].isin(['State government','Local government','Private','Self-employed-not incorporated']),1,0)
	data1['fill_inc_question_veteran_admin_1']=np.where(data1['fill_inc_question_veteran_admin']=='No',1,0)
	data1['sex_1']=np.where(data1['sex']=='Male',1,0)
	data1['enrolled_last_wk_1']=np.where(data1['enrolled_last_wk']=='Not in universe',1,0)
	data1['citizenship_1']=np.where(data1['citizenship'].isin(['Foreign born- Not a citizen of U S','Native- Born in Pureto Rico or U S Outlying']),0,1)
	data1['employment_status_1']=np.where(data1['employment_status'].isin(['Full-time schedules','PT for econ reasons usually PT', 'PT for non-econ reasons usually FT']),1,0)
	data1['occupation_1']=np.where(data1['occupation']==1,1,0)
	data1['hispanic_origin_1']=np.where(data1['hispanic_origin'].isin(['NA','All other']),1,0)
	data1['tax_filer_1']=np.where(data1['tax_filer']=='Joint both under 65',1,0)
	data1['tax_filer_2']=np.where(data1['tax_filer'].isin(['Head of household','Single','Joint both 65+','Joint one under 65 & one 65+']),1,0)
	data1['detailed_hsld_smry_1']=np.where(data1['detailed_hsld_smry']=='Householder',1,0)
	data1['year_1']=np.where(data1['year']==95,1,0)
	data1['veteran_benefit_1']=np.where(data1['veteran_benefit']==0,0,1)
	data1['member_labour_union_1']=np.where(data1['member_labour_union']=='Not in universe',0,1)
	data1['race_1']=np.where(data1['race'].isin(['White','Asian or Pacific Islander']),1,0)
	data1['unemployment_reason_1']=np.where(data1['unemployment_reason']=='Not in universe',0,1)
	data1['family_members_under18_1']=np.where(data1['family_members_under18']=='Not in universe',0,1)
	data1['same_house_prev_yr_1']=np.where(data1['same_house_prev_yr']=='Not in universe',1,0)
	data1['capital_gains_1']=data1['capital_gains']-data1['capital_losses']
	data1['education_1']=np.where(data1['education'].isin(['Prof school degree (MD DDS DVM LLB JD)','Doctorate degree(PhD EdD)']),1,0)
	data1['education_2']=np.where(data1['education'].isin(['Masters degree(MA MS MEng MEd MSW MBA)','Bachelors degree(BA AB BS)']),1,0)
	data1['migration_1']= data1.apply(lambda row: make_variables(row), axis=1)
	new_df=quartile.quartile(data1, 'detailed_occ_cd', 'target')
	data1=quartile.quartile(new_df, 'detailed_ind_cd', 'target')
	return data1[['target','detailed_hsld_smry_1',
                         'region_prev_res_1',
                         'marital_status_1',
                         'marital_status_2',
                         'worker_class_1',
                         'worker_class_2',
                         'worker_class_3',
                         'age',
                         'wage',
                         'dividends',
                         'no_persons_worked_for_employer',
                         'weeks_worked_in_yr',
                         'fill_inc_question_veteran_admin_1',
                         'sex_1',
                         'enrolled_last_wk_1',
                         'citizenship_1',
                         'employment_status_1',
                         'occupation_1',
                         'hispanic_origin_1',
                         'tax_filer_1',
                         'tax_filer_2',
                         'year_1',
                         'veteran_benefit_1',
                         'member_labour_union_1',
                         'race_1',
                         'unemployment_reason_1',
                         'family_members_under18_1',
                         'same_house_prev_yr_1',
                         'capital_gains_1',
                         'education_1',
                         'education_2',
                         'migration_1', 
                         'detailed_occ_cd_A', 
                         'detailed_occ_cd_B',
                         'detailed_occ_cd_C', 
                         'detailed_occ_cd_D', 
                         'detailed_ind_cd_A',
                         'detailed_ind_cd_B', 
                         'detailed_ind_cd_C', 
                         'detailed_ind_cd_D' ]]
