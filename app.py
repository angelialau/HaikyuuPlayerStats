import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

########### Set up the chart
# load data
PLAYER_CSV = './data/haikyuu_players.csv'
METRICS = ['Game Sense', 'Jumping', 'Power', 'Speed', 'Stamina', 'Technique']
data = pd.read_csv(PLAYER_CSV, index_col=0)

def filterDataByPosition(data, selectedPosition):
    '''Transforms data and returns the necessary data for the heatmap graph
    object, given the specified player position'''
    data = data[data.Position==selectedPosition]
    data['Total Score'] = data[METRICS].sum(axis=1)
    data = data.sort_values('Total Score', ascending=True) # descending order in viz
    score_matrix = [[data.loc[player, 'Total Score'] for metric in METRICS] for player in data.index]
    school_matrix = [[data.loc[player, 'School'] for metric in METRICS] for player in data.index]
    filteredData = {
        'data': data,
        'x': METRICS,
        'y': data.index,
        'z': data[METRICS].values,
        'scores': score_matrix,
        'schools': school_matrix
    }
    return filteredData


# generate default heatmap
selectedPosition = 'S'
defaultData = filterDataByPosition(data, selectedPosition)
heatmap = go.Heatmap(z=defaultData['z'],
                     x=defaultData['x'],
                     y=defaultData['y'],
                     text = defaultData['scores'],
                     customdata=defaultData['schools'],
                     hovertemplate="Player: %{y}<br>" \
                                    + "School: %{customdata}<br>" \
                                    + f"Position: {selectedPosition}<br>" \
                                    + "%{x}: %{z}<br>" \
                                    + "Total Score: %{text}<br>" \
                                    + "<extra></extra>",
                     xgap=2,ygap=2,
                     zmin=1,zmax=6,
                     colorscale=[[0.0, 'rgb(245,255,235)'],[0.2, 'rgb(245,255,235)'],
                                 [0.2, 'rgb(253,212,158)'],[0.4, 'rgb(253,212,158)'],
                                 [0.4, 'rgb(253,141,60)'],[0.6, 'rgb(253,141,60)'],
                                 [0.6, 'rgb(217,72,1)'],[0.8, 'rgb(217,72,1)'],
                                 [0.8, 'rgb(127,39,4)'],[1.0, 'rgb(127,39,4)']
                                 ],
                     colorbar=dict(thickness=25,
                                   tickvals=(1.5, 2.5, 3.5, 4.5, 5.5),
                                   ticktext=(1,2,3,4,5),
                                   )
                     )
fig = go.Figure(data=heatmap)
fig.update_xaxes(side='top', title='Metrics')
fig.update_yaxes(title='Player')
fig.update_layout(height=700)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Haikyuu!! Stats'
server = app.server


########### Set up the layout
app.layout = html.Div(children=[
    html.H1('Haikyuu!! Player Stats'),
    dcc.Graph(
        figure=fig
    ),
    html.A('Read about this project', href='https://angelia.substack.com/p/project-idea-haikyuu-player-stats'),
    html.Br(),
    html.A('Github', href='https://github.com/angelialau/HaikyuuPlayerStats'),
    html.Br(),
    html.A('LinkedIn', href='https://www.linkedin.com/in/angelia-lau/'),
    ]
)

if __name__ == '__main__':
    app.run_server()
