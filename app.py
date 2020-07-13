import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go

########### Set up the chart



########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title='Haikyuu!! Stats'

########### Set up the layout
app.layout = html.Div(children=[
    html.H1('Haikyuu Player Stats'),
    # dcc.Graph(
    #     id='graph_id',
    #     figure=fig_obj
    # ),
    html.A('Read about this project', href='https://angelia.substack.com/p/project-idea-haikyuu-player-stats'),
    html.Br(),
    html.A('Github', href='https://github.com/angelialau/HaikyuuPlayerStats'),
    html.Br(),
    html.A('LinkedIn', href='https://www.linkedin.com/in/angelia-lau/'),
    ]
)

if __name__ == '__main__':
    app.run_server()
