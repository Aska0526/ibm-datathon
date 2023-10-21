import pandas as pd
from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px

import openai
import time


def CallDash(sector):
    openai.api_key = 'xxxxxxxx'

    messages = [{"role": "system", "content":
        "I want you to act as a data science instructor. You will explain energy consumption data as an expert."}]

    def ChatRun(message):
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.pop()
        return reply

    def PromptEng():
        ChatRun("you are a python developer")
        time.sleep(20)
        ChatRun("when I ask you any code related questions, only output the code, without any text.")
        time.sleep(20)
        ChatRun("Dont include any text in your answer, only the code")
        time.sleep(20)
        ChatRun("When I ask further questions, do it like the last response. No explanation, only the code")
        time.sleep(20)
        ChatRun("no text at the end, only the code")

    xls = pd.ExcelFile('./ECUK_2022_Consumption_tables_27102022_cleaned.xlsx')
    sheet_names = xls.sheet_names
    all_sheets_data = {}
    for sheet in sheet_names:
        all_sheets_data[sheet] = pd.read_excel(xls, sheet)

    df = all_sheets_data['Table C1']
    labels = df.isna().all(axis=0).cumsum()
    grouped = df.groupby(labels, axis=1)
    small_dataframes = []
    for _, group in grouped:
        small_df = group.dropna(axis=1, how='all')
        small_dataframes.append(small_df)

    PlotDict = {}
    for i in range(len(small_dataframes)):
        key = f"{small_dataframes[i].iloc[-1][0]}"
        value = small_dataframes[i]
        PlotDict[key] = value
    #print(PlotDict)

    df_plot = PlotDict[sector]
    response = ChatRun(f"Please write a report based on the following dataframe. The unit of the data is thousand tonnes of oil equivalen.\
    The dataframe is about Energy Consumption in {sector} in the UK from 1970-2021. \
    The report should summerise the content, show the trends, do comparisions, and give conclusion and future outlook at the end. \
    The report should be less than 300 words. Don't show the title of the report. Make sure each statement is supported by data and numbers. \
    I know the data are from the past and may not be useful to predict the future, so don't say it in the report. The dataframe is:"+str(df_plot))

    app = Dash(__name__)


    # Layout of the Dash application

    app.layout = html.Div([
        html.H1(children=f'UK Final Energy Consumption by sector and fuel 1970-2021 - {sector} | Unit: Thousand tonnes of oil equivalent', style={'textAlign':'center'}),
        dcc.Dropdown(df_plot.columns[1:], 'Coal', id='dropdown-selection'),
        dcc.Graph(id='graph-content'),
        dcc.Textarea(
            id='textarea-example',
            value=str(response),
            style={'width': '100%', 'height': 300},
        )
    ])

    @callback(
  Output('graph-content', 'figure'),
        Input('dropdown-selection', 'value')
    )
    def update_graph(value):
        return px.line(df_plot, x=df_plot.columns[0], y=str(value))

    ##if __name__ == '__main__':
    app.run(debug=False)

#CallDash('Domestic')