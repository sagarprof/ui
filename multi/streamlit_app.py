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


pg.run()