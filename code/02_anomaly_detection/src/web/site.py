import streamlit as st
import requests
import pandas as pd
import json
import plotly.express as px
import plotly.graph_objects as go
import ast

st.set_page_config(layout="wide")

@st.cache_data
def process(server_url, method, num, sensitivity_score, max_fraction_anomalies, debug, input_data_set):
    full_server_url = f"{server_url}/{method}/{num}?sensitivity_score={sensitivity_score}&max_fraction_anomalies={max_fraction_anomalies}&debug={debug}"
    r = requests.post(
        full_server_url,
        data=input_data_set,
        headers={"Content-Type": "application/json"}
    )
    return r

# Used as a helper method for creating lists from JSON.
@st.cache_data
def convert_multivariate_list_to_json(multivariate_str):
    mv_ast = ast.literal_eval(multivariate_str)
    return json.dumps([{"key": k, "vals": v} for idx,[k,v] in enumerate(mv_ast)])

def main():
    st.write(
    """
    # Implementing Multivariate Outlier Detection in Python

    This is an outlier detection application based, in part, on the book Finding Ghosts in Your Data (Apress, 2022).  The purpose of this site is to provide a simple interface for interacting with the outlier detection API we build over the course of a talk.

    ## Instructions
    First, select the method you wish to use for outlier detection.  Then, enter the dataset you wish to process.  This dataset should be posted as a JSON array with the appropriate attributes.

    If you switch between methods, you will see a sample dataset corresponding to the expected structure of the data.  Follow that pattern for your data.
    """
    )

    server_url = "http://localhost/detect"
    method = "multivariate"
    st.write(
    """
    There are three multivariate models we will look at over the course of this talk:

    1. Only use Connectivity-Based Outlier Factor (COF)
    2. Use COF and Local Correlation Integral (LOCI)
    3. Use COF, LOCI, and Copula-Based Outlier Detection (COPOD)

    The "final" version of this is option 3 but to make it easy to compare along the way, we have code for each version.
    """
    )
    num = st.selectbox(label="Choose the method you wish to use.", options = ("1", "2", "3"))
    sensitivity_score = st.slider(label = "Choose a sensitivity score.", min_value=1, max_value=100, value=50)
    max_fraction_anomalies = st.slider(label = "Choose a max fraction of anomalies.", min_value=0.01, max_value=1.0, value=0.3)
    debug = st.checkbox(label="Run in Debug mode?")
    convert_to_json = st.checkbox(label="Convert data in list to JSON format?  If you check this box, enter data as a comma-separated list of values.")
    
    starting_data_set = """[
        {"key":"1","vals":[22.46, 17.69, 8.04, 14.11]},
        {"key":"2","vals":[22.56, 17.69, 8.04, 14.11]},
        {"key":"3","vals":[22.66, 17.69, 8.04, 14.11]},
        {"key":"4","vals":[22.76, 17.69, 8.04, 14.11]},
        {"key":"5","vals":[22.896, 17.69, 8.04, 14.11]},
        {"key":"6","vals":[22.9, 22.69, 8.04, 14.11]},
        {"key":"7","vals":[22.06, 17.69, 8.04, 14.11]},
        {"key":"8","vals":[22.16, 17.69, 9.15, 14.11]},
        {"key":"9","vals":[22.26, 17.69, 8.04, 14.11]},
        {"key":"10","vals":[22.36, 178.69, 8.04, 14.11]},
        {"key":"11","vals":[22.46, 17.69, 8.04, 14.11]},
        {"key":"12","vals":[22.56, 17.69, 8.04, 14.11]},
        {"key":"13","vals":[22.66, 17.69, 8.04, 14.11]},
        {"key":"14","vals":[22.76, 17.69, 8.04, 14.11]},
        {"key":"15","vals":[22.86, 17.69, 8.04, 14.11]},
        {"key":"16","vals":[22.76, 17.69, 8.04, 14.11]},
        {"key":"17","vals":[22.66, 17.69, 8.04, 14.11]},
        {"key":"18","vals":[22.56, 17.69, 8.04, 14.11]},
        {"key":"19","vals":[22.46, 17.69, 8.04, 14.11]},
        {"key":"20","vals":[22.36, 17.69, 8.04, 14.11]},
        {"key":"21","vals":[22.26, 17.69, 8.04, 14.11]}
    ]"""
    input_data = st.text_area(label = "Data to process (in JSON format):", value=starting_data_set, height=300)

    if st.button(label="Detect!"):
        if convert_to_json:
            input_data = convert_multivariate_list_to_json(input_data)
        resp = process(server_url, method, num, sensitivity_score, max_fraction_anomalies, debug, input_data)
        res = json.loads(resp.content)
        df = pd.DataFrame(res['anomalies'])

        if 'anomaly_score_loci' not in df:
            df['anomaly_score_loci'] = "NA"

        if 'anomaly_score_copod' not in df:
            df['anomaly_score_copod'] = "NA"

        st.header('Anomaly score per data point')
        colors = {True: '#481567', False: '#3CBB75'}
        df = df.sort_values(by=['anomaly_score'], ascending=False)
        g = px.bar(df, x=df["key"], y=df["anomaly_score"], color=df["is_anomaly"], color_discrete_map=colors,
                    hover_data=["vals", "anomaly_score_cof", "anomaly_score_loci", "anomaly_score_copod"], log_y=True)
        st.plotly_chart(g, use_container_width=True)


        tbl = df[['key', 'vals', 'anomaly_score', 'is_anomaly', 'anomaly_score_cof', 'anomaly_score_loci', 'anomaly_score_copod']]
        st.write(tbl)

        if debug:
            col11, col12 = st.columns(2)

            with col11:                
                st.header("Tests Run")
                st.write(res['debug_details']['Tests run'])
                st.write(res['debug_details']['Test diagnostics'])

            with col12:
                st.header("Outlier Determinants")
                st.write(res['debug_details']['Outlier determination'])

            st.header("Full Debug Details")
            st.json(res['debug_details'])


if __name__ == "__main__":
    main()