import dash
from dash import dcc, html, dash_table
import requests
from dash.dependencies import Input, Output, State

# Initialize the Dash app
app = dash.Dash(__name__)

# API URL
API_URL = "https://carsmoviesinventoryproject-production.up.railway.app/api/v1/carsmovies?page=0&size=5&sort=carMovieYear,desc"

# Fetch data from the API
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        return data["Movies"]
    else:
        return []

# Fetch the movies data
movies_data = fetch_data()

# Layout of the app
app.layout = html.Div([
    html.H1("Cars Movies Dashboard", style={"textAlign": "center"}),
    dash_table.DataTable(
        id="movies-table",
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Name", "id": "carMovieName"},
            {"name": "Year", "id": "carMovieYear"},
            {"name": "Duration (min)", "id": "duration"}
        ],
        data=movies_data,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "padding": "5px"},
        style_header={"backgroundColor": "lightgrey", "fontWeight": "bold"}
    )
    
])
# Add a form to input new movie details
app.layout.children.append(html.Div([
        html.H3("Add a New Movie"),
        html.Div([
            html.Label("Name:"),
            dcc.Input(id="input-name", type="text", placeholder="Enter movie name"),
        ]),
        html.Div([
            html.Label("Year:"),
            dcc.Input(id="input-year", type="number", placeholder="Enter movie year"),
        ]),
        html.Div([
            html.Label("Duration (min):"),
            dcc.Input(id="input-duration", type="number", placeholder="Enter duration"),
        ]),
        html.Button("Add Movie", id="add-movie-button", n_clicks=0),
        html.Div(id="add-movie-status", style={"marginTop": "10px", "color": "green"})
    ]))
# Callback to handle adding a new movie
@app.callback(
        Output("add-movie-status", "children"),
        Output("movies-table", "data"),
        Input("add-movie-button", "n_clicks"),
        State("input-name", "value"),
        State("input-year", "value"),
        State("input-duration", "value"),
        State("movies-table", "data")
    )
def add_movie(n_clicks, name, year, duration, current_data):
        if n_clicks > 0:
            if not name or not year or not duration:
                return "Please fill in all fields.", current_data
            
            new_movie = {
                "id": len(current_data) + 1,  # Generate a new ID
                "carMovieName": name,
                "carMovieYear": year,
                "duration": duration
            }
            updated_data = current_data + [new_movie]
            return "Movie added successfully!", updated_data
        return "", current_data

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


   