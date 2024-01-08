from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.staticfiles import finders
from django.conf import settings
# for map visualization
import numpy as np
import pandas as pd
import plotly as py
import os
import requests
from io import StringIO
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

worldData = requests.get("https://energy-data.netlify.app/").text
world_csv = pd.read_csv(StringIO(worldData))
#data cleaning
world_csv = world_csv.drop('gdp', axis=1) #remove gdp column
world_csv = world_csv.drop('population', axis=1) #remove population column

country_sorted = world_csv.groupby(['country', 'year']).sum().reset_index().sort_values('year', ascending=False)

# Create your views here.
def index(request):
    return render(request, "greenClean/index.html")

def map(request, year):

    maxYear = max(country_sorted["year"])
    minYear = 1985 #because our data doesn't have very accurate data from before this
    if year > maxYear or year < minYear:
        print("Out of bounds")
        return HttpResponseRedirect(reverse("index"))
    
    col = "coal_electricity"

    mask = country_sorted["year"].astype(int) == year
    # year_countries = (country_sorted.loc[mask])
    # year_countries = year_countries.dropna(subset=[col])
    # year_countries = year_countries[year_countries.iso_code != 0]

    col_countries = country_sorted.dropna(subset=[col])
    col_countries = col_countries[col_countries.iso_code != 0].sort_values(by="year")

    # fig = go.Figure(
    #     data=go.Choropleth(
    #         locations=year_countries["country"], 
    #         locationmode="country names",
    #         z=year_countries[col],
    #         colorscale = 'Greens',
    #         marker_line_color = 'black',
    #         marker_line_width = 1
    #     )
    # )

    # fig.update_layout(
    #     title_text = col.title() + " From " + str(year),
    #     title_x = 0.5,
    #     geo=dict(
    #         showframe = False,
    #         showcoastlines = False,
    #         projection_type = 'equirectangular'
    #     )
    # )

    #Creating the visualization
    fig = px.choropleth(col_countries,
        locations="country",
        locationmode = "country names",
        color=col,
        hover_name="country",
        animation_frame="year"
    )

    fig.update_layout(
        title_text = col.title() + " Change",
        title_x = 0.5,
        geo=dict(
            showframe = False,
            showcoastlines = False,
        )
    )

    return render(request, "greenClean/index.html", {
        "map": fig.to_html(full_html=False),
    })