import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page configuration
st.set_page_config(page_title="Data Sweeper 🧹", layout="wide")

# Custom CSS 
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;  
        color: white;              

    .stApp {
        background: #0e1117;       
        padding: 30px;
        border-radius: 15px;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white;           
    }
    p, div, span, label {
        color: white;           
    
    .stButton>button {
        background: linear-gradient(45deg, #1f77b4, #2ca02c); 
        color: white;  
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 5px 15px rgba(31, 119, 180, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(44, 160, 44, 0.6);
    }
    .stDownloadButton>button {
        background:  #1f77b4;
        color: white;       
        font-size: 16px;
        padding: 10px 20px;
        border-radius: 10px;
        transition: transform 0.3s, box-shadow 0.3s;
        box-shadow: 0 5px 15px rgba(255, 0, 0, 0.4);
    }
    .stDownloadButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 20px rgba(255, 0, 0, 0.6);
    }
    .stDataFrame {
        background: rgba(255, 255, 255, 0.2);
        color: white;                          
        border-radius: 10px;
        padding: 15px;
    }
    .stSuccess {
        color: #00ff00;  
    }
    .stError {
        color: #ff0000;  
    }
    .result-box {
        font-size: 20px;
        font-weight: bold;
        text-align: center;
        background: rgba(255, 255, 255, 0.2);  
        color: white;
        padding: 25px;
        border-radius: 10px;
        margin-top: 20px;
        box-shadow: 0 5px 15px rgba(31, 119, 180, 0.3);
    }
    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 14px;
        color: white;
    }
    .icon {
        display: inline-block;
        margin: 0 10px;
        font-size: 24px;
        color: #1f77b4;  
        transition: color 0.3s;
    }
    .icon:hover {
        color: lightblue;  
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# description
st.title("🧹 Data Sweeper - Sterling Integrator")
st.write("Transform files between CSV and Excel formats with built-in data cleaning and visualization. Creating the project for quarter 3!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (accepts CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type. Please upload a CSV or Excel file: {file_ext}")
            continue

        # File details
        st.write(f"### Preview the head of the DataFrame: {file.name}")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🔧 Data Cleaning Options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success(f"Duplicates removed for {file.name}!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success(f"Missing values filled for {file.name}!")

            # Select columns to keep
            st.subheader("📂 Select Columns to Keep")
            columns = st.multiselect(f"Choose columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show visualization for {file.name}"):
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                st.bar_chart(numeric_df.iloc[:, :2])  # Show the first two numeric columns
            else:
                st.warning("No numeric columns found for visualization.")

        # Conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to", ["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)  
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label="Download Final Text Case Report",  
                data=buffer,
                file_name=file_name,
                mime=mime_type,
            )
            st.success(f"Conversion successful for {file.name}!")

st.success("All files processed successfully! 🎉")

# Footer 
st.markdown(
    """
    <div class='footer'>
        Developed by Muhammad Hamza Khan😎<br>
        <a href="https://github.com/MuhammadHamzaKhan786" target="_blank" class="icon"><i class="fab fa-github"></i></a>
        <a href="https://www.linkedin.com/in/muhammad-hamza-khan-6234772bb/" target="_blank" class="icon"><i class="fab fa-linkedin"></i></a>
        <a href="https://personal-portfolio-hamza.vercel.app/" target="_blank" class="icon"><i class="fas fa-globe"></i></a>
    </div>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
    """,
    unsafe_allow_html=True,
)