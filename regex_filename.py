import pandas as pd
import re

# create toy data 
data = {
    'df1':[
        '15(b)',
        '9821',
        '13270',
        '11929',
        '1016',
        'I-54618-08000002804c5998',
        'I-53647-0800000280472e68',
        'I-52819-080000028043f36c',
        'I-52559-080000028041f843',
        'I-54134-080000028049b1ad',
        'volume-1928-I-32896-English',
        'volume-2503-I-44760',
        'volume-1511-I-26119-English',
        'volume-1579-I-27574-English',
        'volume-1744-I-30373-English'
        ],
    'df2':[
        '15(b)',
        '9821',
        '13270',
        '11929',
        '1016',
        '54618',
        '53647',
        '52819',
        '52559',
        '54134',
        '32896',
        '44760',
        '26119',
        '27574',
        '30373'
    ]
}

df = pd.DataFrame(data)

# we can easily check for equality like this and maybe we can leverage this column to do something
df['check'] = df.df2.isin(df.df1)

# but i'm thinking we want to do something in place...I don't think Python folks like to iterate through pandas rows but I'm a R transplant
# so who cares! HAHA

test = [0] * df.shape[0]

for i, r in enumerate(zip(df['df1'], df['df2'])): # these have to be the same length if using two dfs
    if r[0] is not r[1]:
        nums = re.findall(r'\b\d{5}\b', r[0])
        test[i] = nums[0]
    else:
        test[i] = r[0]
        
print(test)

# we will have to build in a check as well something like 
 # this is your column with only numeric and you will compare to the extracted list from the bad one
test == df['df2'].to_list()

df['new_column_ID'] =  # Use regex extraction here within the df that you want to extract IDs from then do a left join
    