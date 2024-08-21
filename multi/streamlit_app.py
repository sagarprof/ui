import streamlit as st


APM = st.Page(
    "chatbots/APM.py", title="APM", icon=":material/dashboard:", default=True
)
Rules1 = st.Page("chatbots/Rules1.py", title="Rules1", icon=":material/bug_report:")
Rules2 = st.Page(
    "chatbots/Rules2.py", title="Rules2", icon=":material/notification_important:"
)

Insights = st.Page("insights/Dataframes.py", title="Insights", icon=":material/search:")

pg = st.navigation(
    {
        "Chatbots": [APM, Rules1, Rules2],
        "Dataframes": [Insights],
    }
)


pg.run()