import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Hello World, I'm Dash"),
    html.Div([
        "Input: ",
        dcc.Input(id="my-input", value="initial value", type="text"),
    ]),
    html.Br(),
    html.Div(id="my-output"),
    html.Iframe(
        src="https://google.com",
    ),
])

@app.callback(
    Output("my-output", "children"),
    Input("my-input", "value"),
)
def update_output_div(input_value):
    return f"Output: {input_value}"

if __name__ == "__main__":
    app.run_server(debug=True)
