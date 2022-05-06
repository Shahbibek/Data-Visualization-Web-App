from tkinter.tix import Tree
import pandas as pd
import plotly_express as px
import matplotlib.pyplot as plt
import streamlit as st
import yfinance as yf
import numpy as np
import datetime



PAGE_CONFIG = {"page_title":"Data Visualization","page_icon":"chart_with_upwards_trend:", "layout":"centered"}
st.set_page_config(**PAGE_CONFIG)

def showGraphList():
    """This function will return all the graph available"""    
    graph = ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot"]
    # graph = {0: "Line Chart", 1:"Bar Chart"}
    # opt = ""
    opt = st.radio("Select to ",graph)
    # for i in graph:
    #     opt = st.checkbox(i)
    return opt

def sidebar():
    global df, filename, option, opt, columnList 
    df = None
    allowedExtension =['csv', 'xlsx']
    # linegraph = ""
    with st.sidebar:
        uploaded_file = st.sidebar.file_uploader(label="Upload your csv or excel file (200 MB Max).", type=['csv','xlsx'])
        # uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            filename = uploaded_file.name   
            extension = filename[filename.index(".")+1:]
            filename = filename[:filename.index(".")]
            # print(filename)
            # print(extension)
            if extension in allowedExtension:
                df = pd.read_csv(uploaded_file)     # Can be used wherever a "file-like" object is accepted:
                columnList = df.columns.values.tolist()     # to get list of columns
                option = st.selectbox("Select Column", columnList)
                st.subheader("Filters ")
                opt = showGraphList()
            else:
                st.write("File Format is not supported")
def getIndexes(columnName, value):
    # st.write(df[columnName])
    # st.write(value)
    count = -1
    for i in df[columnName]:
        count += 1
        # print(i, value)
        if i == value:
            # print(count)
            # print(True, value, "index = ",  count)
            # st.write(count) 
            return count



def mainContent():
    st.header("Visualize Your Data")
    if df is not None:
        st.write(df)
        # graph = ["Line Chart", "Bar Chart"]
        if opt == "Line Chart":
            label = "Line Chart for {}".format(filename)
            st.header(label)
            st.line_chart(df[option])
        elif opt == "Bar Chart":
            label = "Bar Chart for {}".format(filename)
            st.header(label)
            st.bar_chart(df[option])
        elif opt == "Pie Chart":
            label = "Pie Chart for {}".format(filename)
            st.header(label)
            # st.write(df[option][5])
            # st.write(columnList[0])
            
            
            selectOption = []           
            # data = []
            for i in df[columnList[0]]:
                selectOption.append(i)
            selectedData = st.multiselect(f"Choose {columnList[0]} to see", selectOption)
            
            dataToVisualize = []
            for i in selectedData:
                # st.write(getIndexes(columnList[0], i))                
                index = getIndexes(columnList[0], i)
                # st.write(df[option][index])
                dataToVisualize.append(df[option][index])
            
            x = np.array(dataToVisualize, 'f')
            # st.write(x)
            fig = plt.figure()
            plt.pie(x, labels = selectedData, autopct='%0.f%%')  # %).f%% means no of digit show after decimal

            st.balloons()
            # st.write(option)
            plt.legend(title = option)
            st.pyplot(fig)

        elif opt == "Scatter Plot":
            label = "Scatter Plot for {}".format(filename)
            st.header(label)
            x_values = st.sidebar.selectbox('X axis', options=columnList)
            y_values = st.sidebar.selectbox('Y axis', options=columnList)
            plot = px.scatter(data_frame=df, x=x_values, y=y_values)            
            st.plotly_chart(plot)
        # else:
        #     st.write("Loading data")
    else:
        st.write("There is nothing to show!! please add file to see data")



def liveData():
    dropdown = 0
    st.title('Live Yahoo Finance Dashboard')
    tickers = ('TSLA', 'AAPL', 'MSFT', 'BTC-USD', 'ETH-USD')
    dropdown = st.multiselect('Pick your assests (It is only showing on date basis)', tickers)
    start = st.date_input('Start', value=pd.to_datetime('2021-01-01'))
    end = st.date_input('End', value=pd.to_datetime('today'))
    
    def relativeret(dc):
        rel = dc.pct_change()
        cumret = (1+rel).cumprod()-1
        cumret = cumret.fillna(0)
        return cumret

    if len(dropdown) > 0:
        # dc = yf.download(dropdown, start, end)['Adj Close']
        dc = relativeret(yf.download(dropdown, start, end)['Adj Close'])
        # st.write(dc)
        st.line_chart(dc)

if __name__ == "__main__":
    sidebar()
    liveData()
    mainContent()
