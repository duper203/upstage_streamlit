import streamlit as st

create_page = st.Page("DocVision/invoice_json.py", title="Invoice", icon="📄")
page_two = st.Page("DocVision/page_two.py", title="Invoice", icon=":material/add_circle:")

pg = st.navigation(
        {
            "DocVision": [create_page, page_two],
        }
    )
pg.run()