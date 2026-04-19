


import pandas as pd, numpy as np, os, json, re,  matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')


jsonData=[]
with open('modcloth_final_data.json') as f:
    for line in f.readlines():
        jsonData.append(json.loads(line))
modcloth_data = pd.DataFrame(jsonData)


def height_converter(x):
    '''converts heights'''
    if pd.isna(x): 
        return x
    else:
        split_x=x.split('ft'); height_in_inches_converted_from_string=int(split_x[0])*12
        if len(split_x)==2:
            if split_x[1]=='':
                pass
            else:
                height_in_inches_converted_from_string=height_in_inches_converted_from_string+int(split_x[1].split('in')[0])



        return height_in_inches_converted_from_string

modcloth_data['height']=modcloth_data['height'].apply(height_converter)


s  = pd.read_csv('sets.csv')
c = pd.read_csv('colors.csv')
iv_df = pd.read_csv('inventories.csv')
i_p_df = pd.read_csv('inventory_parts.csv')
p_and_c = i_p_df.merge(c,left_on='color_id',right_on='id',how='inner')
pcs_df = p_and_c.merge(iv_df,left_on='inventory_id',right_on='id',how='inner')
pcsiv_df = pcs_df.merge(s ,left_on='set_num',right_on='set_num',how='inner')
data = pd.pivot_table(data=pcsiv_df,values='rgb',index='year',aggfunc="nunique")
plt.plot(data)
plt.axvline(x=2004,c='r')
plt.ylabel('unique colors per year')



