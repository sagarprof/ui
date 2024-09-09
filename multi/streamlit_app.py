import streamlit as st


Bot = st.Page(
    "chatbots/bot.py", title="Bots", icon=":material/search:", default=True
)

Insights = st.Page("insights/dataframes.py", title="Insights", icon=":material/dashboard:")

pg = st.navigation(
    {
        "Chatbots": [Bot],
        "Dataframes": [Insights],
    }
)
# userid='sp111'


# https//128.10.0.1:8080/{userid}/Bot
# https//128.10.0.1:8080/{userid}/
pg.run()