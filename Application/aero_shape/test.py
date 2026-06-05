import streamlit as st

# Create containers
container1 = st.container()
container2 = st.container()
container3 = st.container()
container4 = st.container()

# Arrange in 2x2 grid using columns
col1, col2 = st.columns(2)

with col1:
    with container1:
        st.write("Top Left")
    with container3:
        st.write("Bottom Left")

with col2:
    with container2:
        st.write("Top Right")
    with container4:
        st.write("Bottom Right")
