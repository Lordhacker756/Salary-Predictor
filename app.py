import streamlit as st
from predict_page import show_predict_page
from explore import show_explore_page

st.sidebar.selectbox('Explore or Predict?', ('Explore', 'Predict'))

if page == 'Explore':
    show_explore_page()
else:
    show_predict_page()
