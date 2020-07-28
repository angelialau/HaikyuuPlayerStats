import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Haikyuu!! Stats'
server = app.server


########### Set up the chart
# load data
METRICS = ['Game Sense', 'Jumping', 'Power', 'Speed', 'Stamina', 'Technique']
METRICS_COLORSCALE = [
    [0.0, 'rgb(245,255,235)'],[0.2, 'rgb(245,255,235)'],
    [0.2, 'rgb(253,212,158)'],[0.4, 'rgb(253,212,158)'],
    [0.4, 'rgb(253,141,60)'],[0.6, 'rgb(253,141,60)'],
    [0.6, 'rgb(217,72,1)'],[0.8, 'rgb(217,72,1)'],
    [0.8, 'rgb(127,39,4)'],[1.0, 'rgb(127,39,4)']
]
METRICS_TICKTEXT = [1,2,3,4,5]
METRICS_TICKVALS = [val+0.5 for val in METRICS_TICKTEXT]
DATA_CSV = './data/haikyuu_players.csv'
DATA = pd.read_csv(DATA_CSV, index_col=0)
POSITIONS = DATA.Position.unique()
POSITION_LABELS = {
    'S': 'Setter',
    'Li': 'Libero',
    'WS': 'Wing Spiker',
    'MB': 'Middle Blocker'
}


########### Set up the layout
app.layout = html.Div(style={'width':'75%', 'margin':'auto'}, children=[
    html.H1('Haikyuu!! Player Stats'),
    html.Div(children=[
        html.H5('Filter by:'),
        dcc.RadioItems(
            options=[
                {'label': 'Position', 'value': 'Position'},
                {'label': 'School', 'value': 'School'},
                # {'label': 'No filter', 'value': 'no_filter'}, # TODO
            ],
            value='Position',
            labelStyle={'display': 'inline-block'},
            id='filterRadio'
        )
    ]),
    html.Div(children=[
        html.H5('Options:'),
        dcc.Dropdown( # TODO: set default values
            id='positionDropdown'
        )
    ]),
    dcc.Graph(
        id='positionHeatmap',
        config={'displayModeBar': False}
    ),
    html.Div(children=[
        html.A('Read about this project', href='https://angelia.substack.com/p/project-idea-haikyuu-player-stats'),
        html.Br(),
        html.A('Github', href='https://github.com/angelialau/HaikyuuPlayerStats'),
        html.Br(),
        html.A('LinkedIn', href='https://www.linkedin.com/in/angelia-lau/'),
    ]),
    ]
)


@app.callback(
    Output('positionDropdown', 'options'),
    [Input('filterRadio', 'value')])
def updateDropdownOptions(filterType):
    if filterType=='Position':
        return [{'label': POSITION_LABELS[pos], 'value': pos} for pos in POSITIONS]
    elif filterType=='School':
        return [{'label': sch, 'value': sch} for sch in sorted(DATA.School.unique())]
    return None


def filterDataByPosition(selectedPosition):
    '''Transforms data and returns the necessary data for the heatmap graph
    object, given the specified player position'''
    data = DATA[DATA.Position==selectedPosition]
    data['Total Score'] = data[METRICS].sum(axis=1)
    data = data.sort_values('Total Score', ascending=True) # descending order in viz
    text_annot = []
    for player in data.index:
        player_entry = []
        for metric in METRICS:
            annot = f"School: {data.loc[player, 'School']}<br>"
            annot += f"Position: {POSITION_LABELS[selectedPosition]}<br>"
            annot += f"Total Score: {data.loc[player, 'Total Score']}<br>"
            player_entry.append(annot)
        text_annot.append(player_entry)
    filteredData = {
        'data': data,
        'x': METRICS,
        'y': data.index,
        'z': data[METRICS].values,
        'annot': text_annot
    }
    return filteredData


def filterDataBySchool(selectedSchool):
    '''Transforms data and returns the necessary data for the heatmap graph
    object, given the specified school'''
    data = DATA[DATA.School==selectedSchool]
    data['Total Score'] = data[METRICS].sum(axis=1)
    data = data.sort_values('Total Score', ascending=True) # descending order in viz
    text_annot = []
    for player in data.index:
        player_entry = []
        for metric in METRICS:
            annot = f"School: {selectedSchool}<br>"
            annot += f"Position: {POSITION_LABELS[data.loc[player, 'Position']]}<br>"
            annot += f"Total Score: {data.loc[player, 'Total Score']}<br>"
            player_entry.append(annot)
        text_annot.append(player_entry)
    filteredData = {
        'data': data,
        'x': METRICS,
        'y': data.index,
        'z': data[METRICS].values,
        'annot': text_annot
    }
    return filteredData


@app.callback(
    Output('positionHeatmap', 'figure'),
    [Input('positionDropdown', 'value'),
     Input('filterRadio', 'value')])
def updateHeatmap(selectedVal, filterType):
    if filterType=='Position':
        filteredData = filterDataByPosition(selectedVal)
    elif filterType=='School':
        filteredData = filterDataBySchool(selectedVal)
    heatmap = {
        'type':'heatmap',
        'z':filteredData['z'],
        'x':filteredData['x'],
        'y':filteredData['y'],
        'text':filteredData['annot'],
        'hovertemplate':"Player: %{y}<br>" \
                        + "%{text}" \
                        + "%{x}: %{z}<br>" \
                        + "<extra></extra>",
        'xgap':2,'ygap':2,
        'zmin': min(METRICS_TICKTEXT),'zmax':max(METRICS_TICKTEXT)+1,
        'colorscale':METRICS_COLORSCALE,
        'colorbar': dict(thickness=25,
                         ticktext=METRICS_TICKTEXT,
                         tickvals=METRICS_TICKVALS),
        }

    layout = {
        'height': 10*len(filteredData['y']) | 400,
        'xaxis': {'title': 'Metrics', 'side': 'top'},
        'yaxis': {'title': 'Player'}
        }

    fig = go.Figure(data=[heatmap], layout=layout)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
