from flask import Flask
from flask import render_template, redirect
from flask import request
import pandas as pd
import geopandas as gpd  
import matplotlib.pyplot as plt  
import json
import plotly.express as px
import plotly.io as pio
import plotly.utils
from jinja2 import Template


app = Flask(__name__)
app.app_context().push()
@app.route("/", methods=['GET', 'POST'])
def index():
  x = request.form.get('para')
  para = 'cond'
  if x == 'temp':
    para = 'temp'
  elif x == 'do':
    para = 'do'
  elif x == 'ph':
    para = 'ph'
  elif x == 'cond':
    para = 'cond'
  elif x == 'bod':
    para = 'bod'
  elif x == 'nit':
    para = 'nit'
  elif x == 'fcol':
    para = 'fcol'
  elif x == 'tcol':
    para = 'tcol'

  pio.renderers.default="browser"
  india_states=json.load(open("states_india.geojson","r"))
  state_id_map={}
  for feature in india_states['features']:
      feature["id"]= feature["properties"]["state_code"]
      state_id_map[feature["properties"]["st_nm"]]=feature["id"]
  df=pd.read_csv('mean.csv')
  df["state"]=df["state"].str.upper().str.title()
  df = df.replace("Delhi", "NCT of Delhi")
  fig=px.choropleth(df,locations="id", geojson=india_states,color=df[para], scope="asia")
  fig.update_geos(fitbounds="locations", visible=False)
  graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
  return render_template("plot.html", fig=graphJSON)

if __name__ == '__main__':
  app.run()
