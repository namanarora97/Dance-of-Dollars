import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Where do the $$$ go?")
st.write(
    'We are attempting to highlight the wealth inequality that has plagued the US for decades.\n' +
    ''
)
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
    
@st.cache
def get_slice_full(variable):
    df = us[us.variable.isin(variable)]
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


st.header(
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

st.altair_chart(single_percentile_vs_years, use_container_width=True)

st.header('Has the distribution of wealth changed over time?')
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

st.altair_chart(slider_change, use_container_width=True)
st.write('Note: This plot does not show unemployed individuals.')
st.write('The gap between the rich and poor has only increased over the last several decades.')

st.write('')
st.header('The corporations of US have seen some immense growth over the last 5 decades')
st.subheader('What has this meant for the poor? - "The Trickle of Cash"')

benefits_and_corporate_earnings = get_slice_full(['mssbho999i', 'mcwboo999i'])
benefits_vs_corporations = pd.pivot_table(
    data = benefits_and_corporate_earnings,
    values = 'value',
    index = 'year',
    columns = 'variable',
    aggfunc='sum'
).set_axis(['Book_value_of_corporations', 'Social_Benefits_Sanctioned'], axis=1)
# Remove nulls
benefits_vs_corporations = benefits_vs_corporations.loc[
    ~benefits_vs_corporations.Social_Benefits_Sanctioned.isna()
]
# Change unit to $Trillion
benefits_vs_corporations = benefits_vs_corporations.apply(
    lambda x : x/10**12
)

social_corporate = alt.Chart(
    benefits_vs_corporations.reset_index(),
    title = 'The Trickle of Cash'
).mark_circle(size = 100, opacity = 1, color='green').encode(
    alt.X(
        'Book_value_of_corporations', 
        title = 'Book Value of US Corporations ($ Trillion)',
        scale = alt.Scale(zero=False)
    ),
    alt.Y('Social_Benefits_Sanctioned', title = 'Social Benefits Spending ($ Trillion)'),
    alt.Tooltip('year')
).interactive().properties(
    width=1000,
    height=500
)

st.altair_chart(social_corporate, use_container_width=True)
st.write('We can notice an odd trend. Social spending has continued to grow \
steadily regardless of the economic situation of the country\'s corporations.')
st.write('We can also notice some major drops in corporate cash during periods of recession, the attacks of 9/11, etc.')
st.write('It can also be noted that the growth of corporations over the past 10 years has been quite fast, while social spending has remained somewhat constant.')

st.markdown("This project was created by [Naman](mailto:namanarora@cmu.edu) and [Nate](mailtondf@andrew.cmu.edu) for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")