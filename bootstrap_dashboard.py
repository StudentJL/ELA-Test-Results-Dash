import pandas as pd
import plotly.express as px  # (version 4.7.0 or higher)
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output  # pip install dash (version 2.0.0 or higher)
import datetime
import numpy as np
import dash_bootstrap_components as dbc


app = Dash(__name__, external_stylesheets=[dbc.themes.VAPOR])

# Import your data
b2018_lc = pd.read_csv("data/ELA_test_scores_by_borough.csv")
d2018_lc = pd.read_csv("data/ELA_test_scores_by_district.csv")
c2018_lc = pd.read_csv("data/ELA_test_scores_by_city.csv")

d2018_lc['Grade'] = d2018_lc['Grade'].astype(str)
b2018_lc['Grade'] = b2018_lc['Grade'].astype(str)
c2018_lc['Grade'] = c2018_lc['Grade'].astype(str)

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("My Github", href="https://github.com/StudentJL")),
    ],
    brand="JL's Dashboard Site",
    brand_href="#",
    color="primary",
    dark=True,
)

# ------------------------------------------------------------------------------
# App layout
app.layout = html.Div([
    navbar,

    html.Br(),

    html.H1("ELA Test Results Dashboard", style={'text-align': 'center'}),
    html.P("of NYC Students Grades 3 to 8", style={'text-align': 'center'}),
    
    html.Br(),

    html.P("Welcome!", style={'text-align': 'center'}),
    html.P("This is a Dashboard devoted to displaying the trends of ELA Test results" +
        "across locations and over time.", style={'text-align': 'center'}),
    html.P("The Goal of this Dashboard is to answer the question of: " + 
        "Have the english language skills of NYC's children been at satisfactory levels?", style={'text-align': 'center'}),
    html.P("Below are visualizations made from ELA Test Results datasets obtained from NYC OpenData," + 
        " with statistics from the Department of Education (DOE).", style={'text-align': 'center'}),
    html.P("You can zoom in by click & drag.", style={'text-align': 'center'}),

    html.Br(),

    html.P("First, let us observe their Mean Scale Scores across grades & locations:", style={'text-align': 'center'}),

    # --------------------------------------------------------------------------------
    # First Chart

    # First we include a dropdown selector
    html.P("Demographic:"),
    dcc.Dropdown(id="selected_demographic",
                options=['Borough','District','City'],
                value='City',
                multi=False,
                style={'width':'40%'}
                ),
    html.P("Year:"),
    dcc.Dropdown(id="selected_year",
                 options=[2013,2014,2015,2016,2017,2018],
                 value=2018,
                 multi=False,
                 style={'width': "40%"}
                 ),

    #  Now we include the bar graph.
    dcc.Graph(
        id='my_bar_graph',
        figure={}),



    # --------------------------------------------------------------------------------
    # Second and Third Charts

    html.Br(),

    html.P("Next, let us see what percentage of students have satisfactory scores.", style={'text-align': 'center'}),
    html.P("NYS has given 4 performance levels, which apply for their grades:", style={'text-align': 'center'}),
    html.P("Level 1: Insufficient", style={'text-align': 'center'}),
    html.P("Level 2: Partially Proficient", style={'text-align': 'center'}),
    html.P("Level 3: Proficient", style={'text-align': 'center'}),
    html.P("Level 4: Excellent!", style={'text-align': 'center'}),
    html.Br(),

    dcc.Graph(
        id='my_pie_graph',
        figure={}),


    # --------------------------------------------------------------------------------
    # Third Chart

    html.Br(),

    html.P("Lastly, let us see how these scores and percentages have changed over the years.", style={'text-align': 'center'}),

    html.P("Measurement:"),
    dcc.Dropdown(id="selected_measurement",
                 options=['Mean Scale Score','Level 1 %', 'Level 2 %', 'Level 3 %', 'Level 4 %'],
                 value='Mean Scale Score',
                 multi=False,
                 style={'width': "40%"}
                 ),

    dcc.Graph(
        id='my_line_graph',
        figure={}),
]) 
# @end of app.layout
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# First chart and connecting the Plotly graphs with Dash Components
@app.callback(
    Output(component_id='my_bar_graph', component_property='figure'), 
    [Input(component_id='selected_demographic', component_property='value'), 
    Input(component_id='selected_year', component_property='value')]
)
def bar_graph(selected_demographic, selected_year):
    print(selected_demographic)
    print(type(selected_demographic))
    print(selected_year) # only to check things on the terminal
    print(type(selected_year))

    if (selected_demographic == 'Borough'):
        temp_df = b2018_lc[(b2018_lc['Year'] == selected_year)]
        fig = px.bar(temp_df, x=selected_demographic, y='Mean Scale Score', color='Grade', barmode='group') 
        fig.update_layout(yaxis_range=[0,650]) # setting a y axis range to keep the y axis consistent
        fig.update_layout(title_text="Mean Scale Scores across %ss in %d" % (selected_demographic, selected_year), title_x=0.5)
    elif (selected_demographic == 'District'):
        temp_df = d2018_lc[(d2018_lc['Year'] == selected_year)]
        fig = px.bar(temp_df, x=selected_demographic, y='Mean Scale Score', color='Grade', barmode='group') 
        fig.update_layout(xaxis = dict(tickmode = 'linear', tick0 = 0, dtick = 1))
        fig.update_layout(yaxis_range=[0,650])
        fig.update_layout(title_text="Mean Scale Scores across %ss in %d" % (selected_demographic, selected_year), title_x=0.5)
    elif (selected_demographic == 'City'):
        temp_df = c2018_lc[(c2018_lc['Year'] == selected_year)]
        fig = px.bar(temp_df, x='Grade', y='Mean Scale Score', color='Grade')
        fig.update_layout(yaxis_range=[0,650])
        fig.update_layout(title_text="Mean Scale Score across NYC in %d" % (selected_year), title_x=0.5, showlegend=False)

    return fig


# ----------------------------------------------------------------
# Pie Graph 
@app.callback(
    Output(component_id='my_pie_graph', component_property='figure'), 
    [Input(component_id='selected_demographic', component_property='value'), 
    Input(component_id='selected_year', component_property='value')])

def pie_graph(selected_demographic, selected_year):

    if (selected_demographic == 'Borough'):
        fig = make_subplots(rows=2, cols=3, specs=[[{'type':'domain'}, {'type':'domain'}, {'type':'domain'}],
            [{'type':'domain'}, {'type':'domain'}, {'type':'domain'}]])
        row_count=1
        column_count=1
        for selected_borough in ['MANHATTAN','BROOKLYN','QUEENS','BRONX','STATEN ISLAND']:
            temp_df = b2018_lc[(b2018_lc['Year'] == selected_year) & (b2018_lc['Borough'] == selected_borough)]
            temp_pt = temp_df.pivot_table(columns=['Borough', 'Year'], values=['Level 1 %', 'Level 2 %', 'Level 3 %', 'Level 4 %'], aggfunc='mean')
            temp_df = pd.DataFrame(temp_pt).reset_index()
            # start adding pie charts
            fig.add_trace(go.Pie(labels=temp_df['index'], values=temp_df[selected_borough][selected_year], textinfo='none', marker_colors=['red','magenta','cyan','blue']),row_count,column_count)
            if column_count < 3: 
                column_count+=1
            elif column_count == 3:
                row_count+=1
                column_count=1
        fig.update_traces(hole=.4, hoverinfo="label+percent+name")
        fig.update_layout(title_text="Level Percentages across %ss in %d (Averaging All Grades)" % (selected_demographic, selected_year), title_x=0.5,
            autosize=False, height=500,
            annotations=[dict(text='Manhattan', x=0.12, y=0.82, font_size=10, showarrow=False), dict(text='Brooklyn', x=0.5, y=0.82, font_size=10, showarrow=False), dict(text='Queens', x=0.87, y=0.82, font_size=10, showarrow=False), 
            dict(text='Bronx', x=0.12, y=0.19, font_size=10, showarrow=False), dict(text='Staten Island', x=0.5, y=0.19, font_size=10, showarrow=False)], 
            showlegend=True)
    elif (selected_demographic == 'District'):
        specs=[]
        for num in range(11):
            specs.append([{'type':'domain'}, {'type':'domain'}, {'type':'domain'}])

        fig = make_subplots(rows=11, cols=3, specs=specs)

        row_count=1
        column_count=1
        for selected_district in range(1,33,1):
            temp_df = d2018_lc[(d2018_lc['Year'] == selected_year) & (d2018_lc['District'] == selected_district)]
            temp_pt = temp_df.pivot_table(columns=['District', 'Year'], values=['Level 1 %', 'Level 2 %', 'Level 3 %', 'Level 4 %'], aggfunc='mean')
            temp_df = pd.DataFrame(temp_pt).reset_index()
            # start adding pie charts
            fig.add_trace(go.Pie(labels=temp_df['index'], values=temp_df[selected_district][selected_year], textinfo='none', marker_colors=['red','magenta','cyan','blue']),row_count,column_count)
            if column_count < 3: 
                column_count+=1
            elif column_count == 3:
                row_count+=1
                column_count=1

            fig.update_traces(hole=.4, hoverinfo="label+percent+name")
            fig.update_layout(title_text="Level Percentages across %ss in %d (Averaging All Grades)" % (selected_demographic, selected_year), title_x=0.5,
                autosize=False, height=2500, 
                annotations=[dict(text='1', x=0.14, y=0.97, font_size=10, showarrow=False), dict(text='2', x=0.5, y=0.97, font_size=10, showarrow=False), dict(text='3', x=0.86, y=0.97, font_size=10, showarrow=False), 
                dict(text='4', x=0.14, y=0.875, font_size=10, showarrow=False), dict(text='5', x=0.5, y=0.875, font_size=10, showarrow=False), dict(text='6', x=0.86, y=0.875, font_size=10, showarrow=False), 
                dict(text='7', x=0.14, y=0.785, font_size=10, showarrow=False), dict(text='8', x=0.5, y=0.785, font_size=10, showarrow=False), dict(text='9', x=0.86, y=0.785, font_size=10, showarrow=False), 
                dict(text='10', x=0.14, y=0.69, font_size=10, showarrow=False), dict(text='11', x=0.5, y=0.69, font_size=10, showarrow=False), dict(text='12', x=0.86, y=0.69, font_size=10, showarrow=False), 
                dict(text='13', x=0.14, y=0.595, font_size=10, showarrow=False), dict(text='14', x=0.5, y=0.595, font_size=10, showarrow=False), dict(text='15', x=0.86, y=0.595, font_size=10, showarrow=False), 
                dict(text='16', x=0.14, y=0.5, font_size=10, showarrow=False), dict(text='17', x=0.5, y=0.5, font_size=10, showarrow=False), dict(text='18', x=0.86, y=0.5, font_size=10, showarrow=False), 
                dict(text='19', x=0.14, y=0.41, font_size=10, showarrow=False), dict(text='20', x=0.5, y=0.41, font_size=10, showarrow=False), dict(text='21', x=0.86, y=0.41, font_size=10, showarrow=False), 
                dict(text='22', x=0.14, y=0.31, font_size=10, showarrow=False), dict(text='23', x=0.5, y=0.31, font_size=10, showarrow=False), dict(text='24', x=0.86, y=0.31, font_size=10, showarrow=False), 
                dict(text='25', x=0.14, y=0.22, font_size=10, showarrow=False), dict(text='26', x=0.5, y=0.22, font_size=10, showarrow=False), dict(text='27', x=0.86, y=0.22, font_size=10, showarrow=False), 
                dict(text='28', x=0.14, y=0.125, font_size=10, showarrow=False), dict(text='29', x=0.5, y=0.125, font_size=10, showarrow=False), dict(text='30', x=0.86, y=0.125, font_size=10, showarrow=False), 
                dict(text='31', x=0.14, y=0.03, font_size=10, showarrow=False), dict(text='32', x=0.5, y=0.03, font_size=10, showarrow=False)], 
                showlegend=True)

    elif (selected_demographic == 'City'):
        temp_df = c2018_lc[(c2018_lc['Year'] == selected_year)]
        temp_pt = temp_df.pivot_table(columns=['Year'], values=['Level 1 %', 'Level 2 %', 'Level 3 %', 'Level 4 %'], aggfunc='mean')
        temp_df = pd.DataFrame(temp_pt).reset_index()
        fig = go.Figure(data=[go.Pie(labels=temp_df['index'], values=temp_df[selected_year], textinfo='none', marker_colors=['red','magenta','cyan','blue'], hoverinfo='label+percent', hole=0.3)])
        fig.update_layout(title_text="Level Percentages across NYC in %d (Averaging All Grades)" % (selected_year), title_x=0.5,
            autosize=False, height=400,
            annotations=[dict(text='NYC', x=0.5, y=0.5, font_size=20, showarrow=False)], showlegend=True)

    return fig



# ----------------------------------------------------------------
# Line Graph
@app.callback(
    Output("my_line_graph", "figure"),
    [Input(component_id='selected_demographic', component_property='value'), 
    Input(component_id='selected_measurement', component_property='value')]
    )

def line_graph(selected_demographic, selected_measurement):

    if (selected_demographic == 'Borough'):
        temp_pt = b2018_lc.pivot_table(columns=[selected_demographic, 'Year'], values=[selected_measurement], aggfunc='mean').T
        temp_df = pd.DataFrame(temp_pt).reset_index()
        fig = px.line(temp_df, x='Year', y=selected_measurement, color=selected_demographic, markers=True)
        fig.update_layout(title_text="Change in %s among %ss from 2013 to 2018 (Averaging All Grades)" % (selected_measurement, selected_demographic), title_x=0.5)
    elif (selected_demographic == 'District'):
        temp_pt = d2018_lc.pivot_table(columns=[selected_demographic, 'Year'], values=[selected_measurement], aggfunc='mean').T
        temp_df = pd.DataFrame(temp_pt).reset_index()
        fig = px.line(temp_df, x='Year', y=selected_measurement, color=selected_demographic, markers=True)
        fig.update_layout(title_text="Change in %s among %ss from 2013 to 2018 (Averaging All Grades)" % (selected_measurement, selected_demographic), title_x=0.5)
    elif (selected_demographic == 'City'):
        temp_pt = d2018_lc.pivot_table(columns=['Year'], values=[selected_measurement], aggfunc='mean').T
        temp_df = pd.DataFrame(temp_pt).reset_index()
        fig = px.line(temp_df, x='Year', y=selected_measurement, markers=True)
        fig.update_layout(title_text="Change in %s within NYC from 2013 to 2018 (Averaging All Grades)" % (selected_measurement), title_x=0.5)

    return fig


# ------------------------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=True, port=6969)