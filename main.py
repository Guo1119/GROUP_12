import streamlit as st
import sys
import os
sys.path.append(os.path.abspath("pages")) 

pg = st.navigation({
    "Movie Analyzer": [
                        st.Page("./pages/page_1.py", title="Distribution Analysis", icon=":material/home:"),
                        st.Page("./pages/page_2.py", title="Chronological Analysis", icon=":material/calendar_month:"),
                        st.Page("./pages/page_3.py", title="I'm Feeling Lucky", icon=":material/shuffle:")
                        ]                    
}, position="sidebar")

pg.run()