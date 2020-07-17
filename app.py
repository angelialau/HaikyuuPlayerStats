import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd

########### Set up the chart
# load data
METRICS = ['Game Sense', 'Jumping', 'Power', 'Speed', 'Stamina', 'Technique']
data = pd.read_csv('haikyuu_players.csv', index_col=0).head(10)
data = data.sort_values('Position')[METRICS]

# generate heatmap
heatmap = go.Heatmap(z=data.values,
                     x=METRICS,
                     y=data.index,
                     xgap=2,ygap=2,
                     zmin=1,zmax=6,
                     colorscale=[[0.0, '#445582'],[0.2, '#445582'],
                                 [0.2, '#835699'],[0.4, '#835699'],
                                 [0.4, '#CA4C8C'],[0.6, '#CA4C8C'],
                                 [0.6, '#FA4F5D'],[0.8, '#FA4F5D'],
                                 [0.8, '#FF7B00'],[1.0, '#FF7B00']
                                 ],
                     colorbar=dict(thickness=25,
                                   tickvals=(1.5, 2.5, 3.5, 4.5, 5.5),
                                   ticktext=(1,2,3,4,5),
                                   )
                     )
fig = go.Figure(data=heatmap)
fig.update_xaxes(side='top', title='Metrics')
fig.update_yaxes(title='Player')


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
