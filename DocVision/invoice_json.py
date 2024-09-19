import streamlit as st
import base64
from langchain_upstage import ChatUpstage
from langchain_core.messages import HumanMessage
import pandas as pd
import json
UPSTAGE_API_KEY = st.secrets["UPSTAGE_API_KEY"]


st.title("Automating Invoice Data Extraction: Invoice ➡️ JSON ➡️ CSV Export")

## 1 --- upload file --- ##

st.subheader("1. Upload your Invoice")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:

    img_base64 = base64.b64encode(uploaded_file.read()).decode("utf-8")

    ## 2 --- JSON format --- ##

    solar_docvision = ChatUpstage(api_key=UPSTAGE_API_KEY, model="solar-docvision")
    msg = HumanMessage(
    content=[
        {"type": "text", 
            "text": 
            "Retrieve invoice items table data. Return response in JSON format. Header as 'Description', 'Quantity, 'unit_price', 'amount' the rows should be 'rows' and header should be'header'"
        },
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"},
        },
    ],
    )
    response = solar_docvision.invoke([msg])
    json_response = response.content
    json_response = json_response.replace("'", '"')

    # st.write(json_response)    
    st.subheader("2. JSON format Output")

    st.json(json_response)


    ## 3 --- DataFrame from JSON output --- ##
    st.subheader("3. Convert it into a Table")

    json_dict = json.loads(json_response)

    df = pd.DataFrame(json_dict["rows"], columns=json_dict["header"])
    st.dataframe(df, use_container_width=True)
    
    ## 4 --- Download in a CSV file --- ##
    st.subheader("4. Download the a CSV file")

    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')

    csv = convert_df(df)
    st.download_button(
        "Press to Download CSV file",
        csv,
        "file.csv",
        "text/csv",
        key='download-csv'
    )




