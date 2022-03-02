import pandas as pd
path = './datasets/wid-all/'

print('Reading US data...')

us = pd.read_csv(r"datasets\wid-all\WID_data_US.csv", sep = ';')

print('Done reading US data')
print('Reading US metadata...')

us_meta = pd.read_csv(
    r"datasets\wid-all\WID_metadata_US.csv",
    sep = ';',
    encoding='ISO-8859-1'
)

print('Data Loaded')

# Fixing the error
us_meta['variable'] = us_meta['variable'].apply(
    lambda x : x[:-4] + x[-3:] + x[-4]
)

print('Merging...')

us = us.merge(
    us_meta[['variable', 'shortname', 'shortage', 'simpledes',
                'shorttype', 'shortpop', 'unit']],
    on = 'variable',
    how = 'inner'
).drop(
    ['age', 'pop'],
    axis = 1
)

# Some cleanup
us['shortname'] = us['shortname'].apply(
    lambda x : x.strip()
)

print('Writing us-master.csv...')

us['percentile'] = us.percentile.str.replace("p", "-").str.slice(1, ) + "th"

us.to_csv(r"datasets\wid-all\us-master.csv")

print('Done')