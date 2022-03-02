
import streamlit as st
import pandas as pd
import altair as alt
from pathlib import Path

st.set_page_config(layout="wide")
st.title("Where does the $$$ go?")
st.write(
    'These interactive displays highlight the growth of income inequality in the United States.\n'
)
st.write(
    'They were inspired by the work of Dr. Thomas Piketty in his seminal work "Capital in the 21st Century"'
)
st.write(
    'Another inspiration was the words of President James Madison that we use to frame our analysis:'
)
st.write(
    '\"We are free today substantially but the day will come when our Republic will be an impossibility. It will be impossibility because wealth will be concentrated in the hands of a few. A republic cannot stand upon bayonets, and when that day comes, when the wealth of the nation will be in the hands of a few, then we must rely upon the wisdom of the best elements in the country to readjust the laws of the nation to the changed conditions.\"'
)
st.write(
    'The data comes from the World Inequality Database and is available at https://wid.world/'
)


@st.cache  # add caching so we load the data only once
def load_data():
    '''
    Load the processed master data set\n
    If the file is available locally, it is loaded. \n
    Else, the file is fetched from a self-hosted Azure blob
    '''
    local_file = './datasets/wid-all/us-master.csv'
    #local_file = r"datasets\wid-all\us-master.csv"
    my_file = Path(local_file)
    if my_file.is_file():
        master_url = local_file
    else:
        master_url = 'https://metashady.blob.core.windows.net/public/us-master.csv'
    us = pd.read_csv(master_url)
    us['percentile'] = us.percentile.str.replace("p", "-").str.slice(1, ) + "th"
    return us

@st.cache  # caching for faster access
def load_meta():
    '''
    Load the metadata dataset
    '''
    meta_url = './datasets/wid-all/WID_metadata_US.csv'
    return pd.read_csv(
        meta_url,
        sep=';',
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
        st.write(us[min_range:max_range + 1])

st.subheader(
    '\"The day will come when our Republic will be an impossibility because wealth will be concentrated'
    'in the hands of a few.\"'
)

st.subheader("Has that day arrived?")

st.write(
    "Let's first look at how the income has changed for each individual section of the population\n" +
    "This should give us a perspective into inflation, and the overall growth of a country."
)
st.write(
    "You can select a year in the first chart to see all the income distributions in the second."
)

englishPercentiles = ["Bottom 1%", "Bottom 10%", "10-20th percentile", "20-30th percentile", "30-40th percentile",
                      "40-50th percentile","50-60th percentile","60-70th percentile","70-80th percentile",
                      "80-90th percentile","Top 10%","Top 1%", "Top 0.1%"]

# percentiles = ['p0p1'] + [i + j for i, j in zip(
#     ['p' + str(i) for i in range(9, 100, 10)],
#     ['p' + str(i) for i in range(10, 101, 10)]
# )] + ['p99.9p100']

percentiles = ['0-1th'] + [i + j for i, j in zip(
    [str(i) for i in range(0, 100, 10)],
    ['-' + str(i) + 'th' for i in range(10, 101, 10)]
)] + ['99.9-100th']

englishToPercentileDict = dict(zip(englishPercentiles, percentiles))

percentileToEnglishDict = dict(zip(percentiles, englishPercentiles))

percentile_brush = st.select_slider(
    'Select a percentile you want to explore!',
    englishPercentiles, 'Top 1%'

)

print(percentile_brush)

year_brush = st.slider(
    'Select a range of years to display',
    1900,
    int(us.year.max()),
    (1970, 2021)
)

# year_brush_a, year_brush_b = year_brush

single = alt.selection_single(encodings=['x'])

print(single)

# Single percentile selected via drop down and trend seen across all years
single_percentile_vs_years = alt.Chart(
    get_slice(
        'Pre-tax national income',
        {'percentile': englishToPercentileDict.get(percentile_brush)}
    ),
).mark_bar(tooltip=True).encode(
    alt.Y('value:Q', title='Income'),
    alt.X('year:O', scale=alt.Scale(zero=False)),
).properties(
    width=800,
    height=400
).transform_filter(
    alt.FieldRangePredicate(field='year', range=list(year_brush)),
).add_selection(
    single
).encode(
    color=alt.condition(single, alt.value("steelblue"), alt.value("grey"))
)


t_df = get_slice('Pre-tax national income', {})
# Slider used to select a single year
slider = alt.binding_range(min=1920, max=2021, step=1, name='year:')
# Setting up a selector for the year using the value from slider
selector = alt.selection_single(name="SelectorName", fields=['year'],
                                bind=slider, init={'year': 2020})

# This chart changes with a slider that shows up underneath
slider_change = alt.Chart(
    t_df[(t_df['percentile'].isin(percentiles)) & (t_df.value > 0)]
).mark_bar(tooltip=True).encode(
    alt.Y('mean(value):Q', title='Income'),#, scale=alt.Scale(type='log')),
    alt.X('percentile', sort=percentiles, title="Income Percentile", axis=alt.Axis(labelAngle=0)),
).properties(
    width=800,
    height=500
)

if percentile_brush == englishPercentiles[0]:
    st.subheader('Question: What\' the income of the bottom 1%')
    st.header('The chart is empty! The data is based on taxable income, and the bottom 1% are below the tax threshold.')
else:
    st.altair_chart(single_percentile_vs_years & slider_change.transform_filter(alt.datum.year < single.year))
    st.subheader('Question: What\' the income of the bottom 1%')

st.write('Note: This plot does not show unemployed individuals.')
st.write('The gap between the rich and poor has only increased over the last several decades.')

st.write('')
st.subheader("\"The wealth of the nation will be in the hands of a few, then we must rely upon the wisdom of the best elements in the country to readjust the laws of the nation to the changed conditions\"")
st.write('The corporations of US have seen some immense growth over the last 5 decades')
st.write('Have we readjusted laws for the social good? ')
st.subheader('What has this meant for the poor?')

benefits_and_corporate_earnings = get_slice_full(['msopgo999i', 'mcwboo999i'])
benefits_vs_corporations = pd.pivot_table(
    data=benefits_and_corporate_earnings,
    values='value',
    index='year',
    columns='variable',
    aggfunc='sum'
).set_axis(['Book_value_of_corporations', 'Social_Protection'], axis=1)
# Remove nulls
benefits_vs_corporations = benefits_vs_corporations.loc[
    ~benefits_vs_corporations.Social_Protection.isna()
]
# Change unit to $Trillion
benefits_vs_corporations['Book_value_of_corporations'] = benefits_vs_corporations['Book_value_of_corporations'].apply(
    lambda x: x / 10 ** 12
)
# Unit to billion
benefits_vs_corporations['Social_Protection'] = benefits_vs_corporations['Social_Protection'].apply(
    lambda x: x / 10 ** 9
)

social_corporate = alt.Chart(
    benefits_vs_corporations.reset_index(),
    title='The Trickle of Cash'
).mark_circle(size=100, opacity=1, color='green').encode(
    alt.X(
        'Book_value_of_corporations',
        title='Book Value of US Corporations ($ Trillion)',
        scale=alt.Scale(zero=False)
    ),
    alt.Y('Social_Protection', title='Social Protection Spending ($ Billion)'),
    alt.Tooltip('year')
).interactive().properties(
    width=1000,
    height=500
)

st.altair_chart(social_corporate, use_container_width=True)
st.write('We can notice an odd trend. Social Protection spending has continued to grow \
steadily regardless of the economic situation of the country\'s corporations.')
st.write('We can also notice some major drops in corporate cash during periods of recession, the attacks of 9/11, etc.')
st.write(
    'It can also be noted that the growth of corporations over the past 10 years has been quite fast, while social spending has remained somewhat constant.')

st.subheader('\"A Republic cannot stand upon bayonets.\"')
st.subheader('Let us see if the military spending has been impacted by any major occurrences in history')
st.write('We wll be plotting the personal income tax to get an idea of the government\'s inflow of cash')
defense_df = get_slice_full(['mdefgo999i', 'mtiwho999i'])[['variable', 'year', 'value']]
defense_df.value = defense_df.value.apply(lambda x: x / 10 ** 9)
defense_df.variable = defense_df.variable.str.replace('mdefgo999i', 'Defence').replace('mtiwho999i', 'Personal_tax')
def_chart = alt.Chart(defense_df, title='Strong and consistent defenses').mark_bar(opacity=0.7, tooltip=True).encode(
    x='year:O',
    y=alt.Y('value:Q', stack=None, title='$ Billion'),
    color='variable'
).interactive().properties(
    width=1000,
    height=500
)

st.write('We can see that the defense spending has been on a steady rise ever since 9/11')
st.write('Even though the US economy suffered, defenses did not go down.')
st.altair_chart(def_chart, use_container_width=True)

st.markdown(
    "This project was created by [Naman](mailto:namanarora@cmu.edu) and [Nate](mailto:ndf@andrew.cmu.edu) for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")