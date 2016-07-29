"""
quartile is a module for quartiling an attribute based on a target
usage: new_df=quartile.quartile(src_df, 'detailed_occ_cd', 'target')
"""
import numpy as np
import pandas as pd

def allot(rank_lkup, x):
    if x <= rank_lkup.iloc[1,0]:
        return 'D'
    elif x <= rank_lkup.iloc[2,0]:
        return 'C'   
    elif x <= rank_lkup.iloc[3,0]:
        return 'B'
    else:
        return 'A'


def quartile(source_df, col_name, target_col_name):
	hit_rate_df=pd.DataFrame(source_df[[col_name,target_col_name]].groupby(col_name).mean())
	hit_rate_df.rename(columns={target_col_name: 'hit_ratio'}, inplace=True)
	rank_lkup=pd.DataFrame(np.percentile(hit_rate_df['hit_ratio'], [0, 25, 50, 75, 100]))
	hit_rate_df['target_tier']= hit_rate_df['hit_ratio'].map(lambda x: allot(rank_lkup,x))
	results_df = pd.merge(source_df, hit_rate_df, left_on=col_name, right_index=True, how='left', sort=False);
	results_df.drop('hit_ratio', axis=1, inplace=True)
	final_df = pd.concat([results_df, pd.get_dummies(results_df['target_tier'], prefix=col_name)], axis=1)
	final_df.drop('target_tier', axis=1, inplace=True)
	return final_df


