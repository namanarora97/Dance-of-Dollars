import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Where do the $$$ go?")
@st.cache  # add caching so we load the data only once
def load_data():
    '''
    Load the processed master data set\n
    If the file is available locally, it is loaded. \n
    Else, the file is fetched from a self-hosted Azure blob 
    '''
    local_file = './datasets/wid-all/us-master.csv'
    my_file = Path(local_file)
    if my_file.is_file():
        master_url = local_file
    else:
        master_url = 'https://metashady.blob.core.windows.net/public/us-master.csv'
    return pd.read_csv(master_url)

@st.cache # caching for faster access
def load_meta():
    '''
    Load the metadata dataset 
    '''
    meta_url = './datasets/wid-all/WID_metadata_US.csv'
    return pd.read_csv(
    meta_url, 
    sep = ';',
    encoding='ISO-8859-1'
    )

@st.cache
def get_slice(variable, dict=None):
    '''
    Returns a slice of a datset for the given variable
    '''
    df = us[(us.shortname == variable)
        & (us.shorttype == 'Average')
        & (us.shortpop == 'equal-split adults')
        & (us.shortage == 'Adults')]
    if dict != None:
        df = df.loc[(df[list(dict)] == pd.Series(dict)).all(axis=1)]
    return df


# Load the data
with st.spinner(text="Loading data..."):
    us = load_data()
    meta = load_meta()

# Display data if user wants 
if st.checkbox('Show data sample'):
    st.write(us[:20])    
    st.write('Only first 20 rows were loaded.')
    if st.checkbox('Show entire data (may be slow)'):
        slice_index = st.slider(
            'Select a range of indices', 
            0, len(us), 
            (0, 50)
        )
        min_range, max_range = slice_index
        st.write(us[min_range:max_range+1])


st.write(
    'We know that income is not equally distributed. But how unequal is it, really?'
)

st.write(
    "Let's first look at how the income has changed for each individual section of the population\n" +
    "This should give us a perspective into inflation, and overall growth of a country."
)

percentiles = ['p0p1'] + [i+j for i,j in zip(
    ['p' + str(i) for i in range(9,100,10)], 
    ['p' + str(i) for i in range(10,101,10)]
    )] + ['p99.9p100']

percentile_brush = st.selectbox(
    'Select a percentile you want to explore\n (pXpY translates to indivuals between the X and Y percentiles)',
    percentiles,
    index = 1
)

st.write('Tip: Try selecting the lowest percentile')

if percentile_brush == 'p0p1':
    st.write('The chart is empty! The lowest 1% have been living in poverty/unemployment for a while now.')

print(percentile_brush)

year_brush = st.slider(
    'Select a range of years to display',
    1900, 
    int(us.year.max()),
    (1920, 2021)
)

# year_brush_a, year_brush_b = year_brush

single = alt.selection_single(encodings = ['x'])

print(single)

# Single percentile selected via drop down and trend seen across all years
single_percentile_vs_years = alt.Chart(
    get_slice(
        'Pre-tax national income',
        {'percentile' : percentile_brush}
    ),
).mark_bar(tooltip=True).encode(
    alt.Y('value:Q', title = 'Income'),
    alt.X('year:O', scale = alt.Scale(zero=False)),
).properties(
    width=1000,
    height=500
).transform_filter(
    alt.FieldRangePredicate(field='year', range = list(year_brush)),
).add_selection(
    single
).encode(
    color=alt.condition(single, alt.value("steelblue"), alt.value("grey"))
)

st.write(single_percentile_vs_years)

# t_df = get_slice('Pre-tax national income', {})

# all_percentiles_single_year = alt.Chart(
#     t_df[t_df.percentile.isin(percentiles)]
# ).mark_bar(tooltip=True).encode(
#     alt.Y('sum(value)', title = 'Income'),
#     alt.X('percentile'),
# ).properties(
#     width=1000,
#     height=500
# )

st.write('Has the distribution of wealth changed over time?')
st.write('Use the slider underneath to visualize!')

t_df = get_slice('Pre-tax national income', {})
# Slider used to select a single year
slider = alt.binding_range(min=1920, max=2021, step=1, name='year:')
# Setting up a selector for the year using the value from slider 
selector = alt.selection_single(name="SelectorName", fields=['year'],
                                bind=slider, init={'year': 2020})

# This chart changes with a slider that shows up underneath
slider_change = alt.Chart(
    t_df[(t_df['percentile'].isin(percentiles)) & (t_df.value>0)]
).mark_bar(tooltip=True).encode(
    alt.Y('sum(value):Q', title = 'Income', scale=alt.Scale(type='log')),
    alt.X('percentile', sort=percentiles),
).interactive().transform_filter(
    alt.datum.year < selector.year
).add_selection(
    selector
).properties(
    width=1000,
    height=500
)

st.write(slider_change)
st.write('Note: This plot does not show unemployed individuals.')
st.write('The gap between the rich and poor has only increased over the last several decades.')

# st.write(single_percentile_vs_years \
#     & all_percentiles_single_year.transform_filter(single))

# st.altair_chart(
#     single_percentile_vs_years \
#     & all_percentiles_single_year.transform_filter(single),
#     use_container_width=True
# )


# test=alt.Chart(
#     t_df[t_df.percentile.isin(percentiles)]
# ).mark_bar(tooltip=True).encode(
#     alt.Y('sum(value)', title = 'Income'),
#     alt.X('percentile'),
# )

# st.altair_chart(test)
# st.write(all_percentiles_single_year)
# print(alt.__version__)

st.markdown("This project was created by [Naman](mailto:namanarora@cmu.edu) and [Nate](mailtondf@andrew.cmu.edu) for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
