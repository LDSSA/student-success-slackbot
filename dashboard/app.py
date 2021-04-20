import os

import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    os.environ['DB_URI'].replace('postgres', 'postgresql'),
    pool_size=3,
    pool_timeout=10
)

df = pd.read_sql(
    "select * from submission_db where length(slack_id) = 11",
    engine
)
df_plot = (
    df
    .groupby('learning_unit')
    .slack_id
    .count()
    .to_frame()
    .rename(columns={'slack_id': 'Number of students who have submitted'})
)

st.dataframe(df_plot, width=1000, height=1000)

ax = df_plot.plot.bar(
    rot=0,
    title='How many students have completed each Learning Unit'
)
st.pyplot(
    ax.get_figure()
)

df_table = (
    df
    .loc[:, ['learning_unit', 'slack_id']]
    .sort_values(['learning_unit', 'slack_id'], ascending=[False, True])
    .reset_index(drop=True)
    .to_html()
)

st.markdown(
    df_table,
    unsafe_allow_html=True
)

engine.dispose()
