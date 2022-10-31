import dash
from dash import html,dcc
from dash.dependencies import Input ,Output
import pandas as pd
import plotly.express as px
import random as rd
from datetime import date

df = pd.DataFrame({
    "Date":[f"08/{n}/2022" for n in range(1,30)],
    "Account":[rd.choice(["Income","Expense","Income","MISC","Salary"]) for i in range(1,30)],
    "Amount":[rd.randint(500,20000) for i in range(1,30)]
})
df["Date"] = pd.DatetimeIndex(df["Date"])

dz = df.groupby(["Account"])["Amount"].agg("sum").reset_index()



fig3 = px.bar(df,x = "Account",y = "Amount",title = "Account sum expenses")

app = dash.Dash()


app.layout = html.Div(children = [
    
    html.Div(children = [html.Div(dcc.Dropdown(id = "drop",options  = ["Salary","Expense","MISC","Income"],value  = ["Salary"],multi = True),style = {"width":"40%","height":"50px","float":"left"}),
                         html.Div(dcc.DatePickerRange(id = "date",
                                             min_date_allowed=date(2022, 8, 1),
                                             max_date_allowed=date(2022, 8, 30),
                                             #initial_visible_month=date(2022, 8, 1),
                                             start_date=date(2022, 8, 1),
                                             end_date=date(2022, 8, 30)
                                             ),style = {"width":"40%","height":"50px","float":"left"})
                         ],style = {"width":"80%","height":"50px","background-color":"red","Display":"inline-block"} ),
    html.Div(dcc.Graph(id = "fig1"),style ={"display":"inline-block","width":"50%","height":"400px","background-color":"blue"}),
    html.Div(children = [dcc.Graph(id = "fig2")],style ={"display":"inline-block","width":"50%","height":"400px","background-color":"yellow"}),
    html.Div(dcc.Graph(id = "fig3",figure = fig3),style = {"width":"100%","height":"400px","background-color":"red","display":"inline-block"}),
  
    
])


@app.callback(
    Output(component_id = "fig1",component_property = "figure"),
    Input(component_id = "drop",component_property = "value")
)
def update_plot(input_acc):
    acc = "Salary"
    dy = df.copy(deep = True)
    if input_acc:
        acc = input_acc
        dy =dy[dy["Account"].isin(input_acc)] 
    dy2 = dy.groupby(["Account"])["Amount"].agg("mean").reset_index()
    fig1 = px.pie(dy2,names = "Account",values = "Amount",title = "Account mean expenses")
    return fig1

@app.callback(
    Output(component_id = "fig2",component_property = "figure"),
    Input('date', 'start_date'),
    Input('date', 'end_date')
)
def update_plot(start_date,end_date):
    dy = df.copy(deep = True)
    start = date(2022, 8, 1)
    end = date(2022, 8, 30)
    if start_date:
        dy1 = dy[(dy["Date"]<=end_date) & (dy["Date"]>=start_date)]
        fig2 = px.line(dy1,x = "Date",y = "Amount",title = "All accounts August")
        
    else:
        dy1 = dy[(dy["Date"]<=end) & (dy["Date"]>=start)]
        fig2 = px.line(dy1,x = "Date",y = "Amount",title = "All accounts August")
    fig2.update_yaxes(rangemode="tozero")
    return fig2
        

if __name__ =="__main__":
    app.run_server(debug = True)