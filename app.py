#imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from io import BytesIO

#set up the app
st.set_page_config(page_title='📀Data Sweeper', layout='wide')
st.title('📀Data Sweeper')
st.write("We convert your files between CSV and Excel with seamless data cleaning and visualization.")

uploaded_files = st.file_uploader("Upload your files here (CSV or Excel):" , type=["csv","xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
           df = pd.read_csv(file)
        elif file_ext==".xlsx":
            df=pd.read_excel(file)
        else:
            st.error(f'unsupported file format: {file_ext}') #f is a formatted string which allows variable input.
            continue
    
    #display the file deets
    st.write(f"File.Name : {file.name}")
    st.write(f"File.Size : {file.size/1024}")

    #display first 5 rows of our df
    st.write("Preview the head of your data frame")
    st.dataframe(df.head())

    #options for cleaning data
    st.subheader("Options for Data cleaning")
    if st.checkbox(f"Clean data for {file.name}"):
       col1 , col2 = st.columns(2)

       with col1:
           if st.button(f"Remove duplicates from {file.name}"):
              df.drop_duplicates(inplace=True)
              st.write("✔ Duplicates Removed!")

       with col2:
           if st.button(f"Fill missing values for {file.name}"):
              numeric_cols = df.select_dtypes(include=["number"]).columns
              df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
              st.write("✔ Missing values have been filled!")

        #choose specific columns to keep or convert 
    st.subheader("Select columns to convert")
    columns = st.multiselect(f"Select columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]

#data visualization
    st.subheader("📊Data Visualizations")
    if st.checkbox(f"Show visualizations for {file.name}"):
        st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])
   
    #coversion of files from csv -> excel
    st.subheader("🔁Conversion Options")
    conversion_type= st.radio(f"Convert {file.name}:",["CSV","Excel"], key=file.name)
    if st.button(f"Convert {file.name}"):
        buffer= BytesIO()
        if conversion_type == "CSV":
            df.to_csv (buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"

        elif conversion_type== "Excel":
            df.to_excel (buffer,index=False)
            file_name = file.name.replace(file_ext,".xlsx")
            mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        buffer.seek(0)

        #download button
        st.download_button(
            label = f"⬇Download {file.name} as {conversion_type}",
            data = buffer,
            file_name = file_name,
            mime = mime_type
                           )

        st.success("🎉All Files Processed")