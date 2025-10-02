import dash
from dash import html, dcc
import plotly.graph_objs as go
import json
from services.cache import get_latest_risk
from services.location_lookup import get_location_name

app = dash.Dash(__name__)

locations = [
  {"lat": 29.721345, "lon": -95.342013},
  {"lat": 29.758828, "lon": -95.370804}
]

def fetch_latest_risks():
  risk_levels = []
  labels = []
  timestamps = []
  for loc in locations:
    result = get_latest_risk(loc["lat"], loc["lon"])
    if result:
      location_name = get_location_name(loc["lat"], loc["lon"])
      data = json.loads(result)
      risk_levels.append(data["risk"]["risk_level"])
      labels.append(location_name if location_name else 'Unknown')
      timestamps.append(data["timestamp"])
  return labels, risk_levels, timestamps


app.layout = html.Div([
  html.H1("Latest Risk by Location", style={"textAlign": "center"}),
  html.Div(id='risk-gauges', style={"textAlign": "center"}),
  dcc.Interval(
    id='interval-component',
    interval=5*1000,  # Update every 30 seconds
    n_intervals=0
  )
])


# Color coding for risk levels
def risk_color(level):
  if level == 1:
    return "#2ecc40"  # Green
  elif level == 2:
    return "#f1c40f"  # Yellow
  elif level == 3:
    return "#ff851b"  # Orange
  elif level == 4:
    return "#ff4136"  # Red
  elif level == 5:
    return "#85144b"  # Dark Red
  else:
    return "#dddddd"  # Default gray

@app.callback(
  dash.dependencies.Output('risk-gauges', 'children'),
  [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_gauges(n):
  labels, risk_levels, timestamps = fetch_latest_risks()
  gauges = []
  for i in range(len(labels)):
    gauges.append(
      html.Div([
        html.H3(labels[i]),
        dcc.Graph(
          figure=go.Figure(
            go.Indicator(
              mode="gauge+number",
              value=risk_levels[i],
              gauge={
                "axis": {"range": [1, 5]},
                "bar": {"color": risk_color(risk_levels[i])},
                "steps": [
                  {"range": [1, 2], "color": "#2ecc40"},
                  {"range": [2, 3], "color": "#f1c40f"},
                  {"range": [3, 4], "color": "#ff851b"},
                  {"range": [4, 5], "color": "#ff4136"}
                ]
              },
              number={"font": {"color": risk_color(risk_levels[i]), "size": 32}},
              domain={"x": [0, 1], "y": [0, 1]},
              title={"text": f"Risk Level ({timestamps[i]})"}
            )
          ),
          style={"height": "300px", "width": "400px"}
        )
      ], style={"display": "inline-block", "margin": "20px", "verticalAlign": "top"})
    )
  return gauges

if __name__ == "__main__":
  app.run(debug=True)