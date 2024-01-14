from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.staticfiles import finders
from django.conf import settings
from django import forms

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

maxYear = max(country_sorted["year"])
minYear = min(country_sorted["year"])

# Mapping choice to it's visual text for select field
categories = [
    ('biofuel_consumption', 'Primary energy consumption from biofuels(terawatt-hours)'),
    ('biofuel_electricity', 'Electricity generation from bioenergy(terawatt-hours)'),
    ('biofuel_share_elec', 'Share of electricity that comes from bioenergy(percentage of total electricity)'),
    ('coal_cons_per_capita', 'Coal consumption per capita(kilowatt-hours per person)')
]

class MapForm(forms.Form):
    year = forms.IntegerField(label="Year", required=True, initial=maxYear, min_value=minYear, max_value=maxYear, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(widget=forms.Select(choices=categories, attrs={"class": "form-select"}))

# Create your views here.
def index(request):
    return render(request, "greenClean/index.html")

def mapForm(request):

    form = MapForm()

    return render(request, "greenClean/map.html", {
        "form": form,
    })

def mapView(request, year):

    if year > maxYear or year < minYear:
        print("Out of bounds")
        return HttpResponseRedirect(reverse("index"))
    
    col = "coal_electricity"

    mask = country_sorted["year"].astype(int) == year
    year_countries = (country_sorted.loc[mask]) # get all rows with year equal to inputted year
    year_countries = year_countries.dropna(subset=[col]) # Drop all country rows where the value is null, so they will be gray in the visualization

    col_countries = country_sorted.dropna(subset=[col])
    col_countries = col_countries[col_countries.iso_code != 0].sort_values(by="year")

    fig = go.Figure(
        data=go.Choropleth(
            locations=year_countries["country"], 
            locationmode="country names",
            z=year_countries[col],
            colorscale = 'Greens',
            marker_line_color = 'black',
            marker_line_width = 1
        )
    )

    fig.update_layout(
        title_text = col.title() + " From " + str(year),
        title_x = 0.5,
        geo=dict(
            showframe = False,
            showcoastlines = False,
            projection_type = 'equirectangular'
        )
    )

    #Creating the visualization timelapse, we use px
    # fig = px.choropleth(col_countries,
    #     locations="country",
    #     locationmode = "country names",
    #     color=col,
    #     hover_name="country",
    #     animation_frame="year"
    # )

    # fig.update_layout(
    #     title_text = col.title() + " Change",
    #     title_x = 0.5,
    #     geo=dict(
    #         showframe = False,
    #         showcoastlines = False,
    #     )
    # )

    return render(request, "greenClean/map.html", {
        "map": fig.to_html(full_html=False),
    })

def tips(request):
    return render(request, "greenClean/tips.html")