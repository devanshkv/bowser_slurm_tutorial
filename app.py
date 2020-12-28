#!/usr/bin/env python3

import streamlit as st
from jinja2 import Environment, FileSystemLoader
import datetime
import base64
import uuid
import re


def download_button(
    object_to_download, download_filename, button_text  # , pickle_it=False
):
    """
    Generates a link to download the given object_to_download.

    From: https://discuss.streamlit.io/t/a-download-button-with-custom-css/4220
    Params:
    ------
    object_to_download:  The object to be downloaded.
    download_filename (str): filename and extension of file. e.g. mydata.csv,
    some_txt_output.txt download_link_text (str): Text to display for download
    link.
    button_text (str): Text to display on download button (e.g. 'click here to download file')
    pickle_it (bool): If True, pickle file.
    Returns:
    -------
    (str): the anchor tag to download object_to_download
    Examples:
    --------
    download_link(your_df, 'YOUR_DF.csv', 'Click to download data!')
    download_link(your_str, 'YOUR_STRING.txt', 'Click to download text!')
    """
    try:
        # some strings <-> bytes conversions necessary here
        b64 = base64.b64encode(object_to_download.encode()).decode()
    except AttributeError as e:
        b64 = base64.b64encode(object_to_download).decode()

    button_uuid = str(uuid.uuid4()).replace("-", "")
    button_id = re.sub("\d+", "", button_uuid)

    custom_css = f""" 
        <style>
            #{button_id} {{
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background-color: rgb(255, 255, 255);
                color: rgb(38, 39, 48);
                padding: .25rem .75rem;
                position: relative;
                text-decoration: none;
                border-radius: 4px;
                border-width: 1px;
                border-style: solid;
                border-color: rgb(230, 234, 241);
                border-image: initial;
            }} 
            #{button_id}:hover {{
                border-color: rgb(246, 51, 102);
                color: rgb(246, 51, 102);
            }}
            #{button_id}:active {{
                box-shadow: none;
                background-color: rgb(246, 51, 102);
                color: white;
                }}
        </style> """

    dl_link = (
        custom_css
        + f'<a download="{download_filename}" id="{button_id}" href="data:file/txt;base64,{b64}">{button_text}</a><br><br>'
    )

    st.markdown(dl_link, unsafe_allow_html=True)


def show():
    input_dict = {}
    st.write("### Type")
    input_dict["type_of_code"] = st.selectbox("", ["Script", "One Liner"])

    st.write("### Partition")
    input_dict["partition"] = st.selectbox("", ["batch", "gpu"])

    st.write("### Number of compute nodes")
    if input_dict["partition"] == "batch":
        input_dict["no_of_nodes"] = st.number_input(
            "", min_value=1, max_value=10, value=1
        )
    else:
        input_dict["no_of_nodes"] = st.number_input(
            "", min_value=1, max_value=5, value=1
        )
    st.write("Use 1 unless running a distributed-memory parallel application")

    st.write("### Number of processor cores per node")
    if input_dict["partition"] == "batch":
        input_dict["nproc"] = st.number_input("", min_value=1, max_value=24, value=1)
        st.write("All nodes have 24 cores")
    else:
        input_dict["nproc"] = st.number_input("", min_value=1, max_value=40, value=1)
        st.write("All nodes have 40 cores")

        st.write("### Number of GPUs:")
        input_dict["ngpu"] = st.number_input("", min_value=1, max_value=4, value=1)

    st.write("### Memory per compute node:")
    if input_dict["partition"] == "batch":
        input_dict["memory"] = st.number_input(
            "", min_value=1, max_value=64, value=10, step=1
        )
        st.write("All nodes have 64 GB")
    else:
        input_dict["memory"] = st.number_input(
            "", min_value=1, max_value=256, value=10, step=1
        )
        st.write("All nodes have 256 GB")

    st.write("### Wall Time")
    input_dict["days_requested"] = st.number_input(
        "Days", min_value=0, max_value=60, step=1, value=0
    )
    input_dict["hours_requested"] = st.time_input("Hours", value=datetime.time(hour=7))

    st.write("### Command")
    if input_dict["partition"] == "batch":
        input_dict["command"] = st.text_area("", value="sleep 60")
    else:
        input_dict["command"] = st.text_area("", value="nvidia-smi")

    st.write("### Job name:")
    input_dict["job_name"] = st.text_input("", key="job_name")
    st.write("Default is the job script name. Displayed by the `squeue` command.")

    st.write("### Output file:")
    input_dict["out_name"] = st.text_input("", key="out_name")
    st.write("Default is 'slurm-%j.out', where %j is the job ID.")

    return input_dict


# Set page title and favicon.
st.set_page_config(
    page_title="Code Generator for Slurm on Bowser",
)

with st.sidebar:
    inputs = show()
"""
# Code Generator for Slurm on Bowser
"""
html_icons = """
<center>
<a href="https://github.com/devanshkv/bowser_slurm_tutorial/issues"><img alt="GitHub issues" src="https://img.shields.io/github/issues/devanshkv/bowser_slurm_tutorial?style=social"></a>
<a href="https://github.com/devanshkv/bowser_slurm_tutorial/network"><img alt="GitHub forks" src="https://img.shields.io/github/forks/devanshkv/bowser_slurm_tutorial?style=social"></a>
<a href="https://github.com/devanshkv/bowser_slurm_tutorial/stargazers"><img alt="GitHub stars" src="https://img.shields.io/github/stars/devanshkv/bowser_slurm_tutorial?style=social"></a>
<a href="https://www.twitter.com/devanshkv"><img alt="Follow" src="https://img.shields.io/twitter/follow/devanshkv?style=social"></a>
</center>
"""
st.markdown(html_icons, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)
"""
Jumpstart your research:

1. Specify details in the sidebar *(click on **>** if closed)*

2. Code will be generated below

3. Download and do magic! :sparkles:
---
"""
env = Environment(
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True,
)

template = env.get_template("slurm.sh.jinja")
code = template.render(**inputs)
col1, col2, col3 = st.beta_columns(3)
with col2:
    download_button(code, "generated-code.sh", "🐍 Download (.sh)")
st.code(code)
