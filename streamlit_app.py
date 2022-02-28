import streamlit as st
import pandas as pd
import altair as alt

st.title("Where do the $$$ go?")

@st.cache  # add caching so we load the data only once
def load_data():
    '''
    Load the processed master data set
    '''
    master_url = './datasets/wid-all/us-master.csv'
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

# Load the data
with st.spinner(text="Loading data..."):
    us = load_data()
    meta = load_meta()

# Display data if user wants 
if st.checkbox('Show data'):
    st.write(us[:20])    
    st.write('Only first 20 rows were loaded.')
    if st.checkbox('Show entire data (may be slow)'):
        slice_age = st.slider(
            'Select a range of indices', 
            0, len(us), 
            (0, 50)
        )
        min_range, max_range = slice_age
        st.write(us[min_range:max_range+1])





# st.write("Hmm 🤔, is there some correlation between body mass and flipper length? Let's make a scatterplot with [Altair](https://altair-viz.github.io/) to find.")

# chart = alt.Chart(df).mark_point().encode(
#     x=alt.X("body_mass_g", scale=alt.Scale(zero=False)),
#     y=alt.Y("flipper_length_mm", scale=alt.Scale(zero=False)),
#     color=alt.Y("species")
# ).properties(
#     width=600, height=400
# ).interactive()

# st.write(chart)

st.markdown("This project was created by [Naman](mailto:namanarora@cmu.edu) and [Nate](ndf@andrew.cmu.edu) for the [Interactive Data Science](https://dig.cmu.edu/ids2022) course at [Carnegie Mellon University](https://www.cmu.edu).")
