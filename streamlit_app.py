import streamlit as st

def page2():
    st.title("Second page")

pg = st.navigation({
    "Movie Analyzer": [
                        st.Page("page_1.py", title="Distribution Analysis", icon=":material/home:"),
                        st.Page("page_2.py", title="Chronological Analysis", icon=":material/calendar_month:"),
                        ]                    
}, position="sidebar")

pg.run()