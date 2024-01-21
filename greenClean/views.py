from django.shortcuts import render

# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib.staticfiles import finders
# from django.conf import settings

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.staticfiles import finders
from django.conf import settings
from django.core.files.storage import default_storage
from django import forms

# for map visualization
# import numpy as np
import pandas as pd
# import plotly as py
# import os
import requests
from io import StringIO
# import plotly.express as px
import plotly.graph_objs as go
# from plotly.subplots import make_subplots
# from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

worldData = default_storage.path("energyData.csv")
world_csv = pd.read_csv(worldData)

#data cleaning
world_csv = world_csv.drop('gdp', axis=1) #remove gdp column
world_csv = world_csv.drop('population', axis=1) #remove population column

country_sorted = world_csv.groupby(['country', 'year']).sum().reset_index().sort_values('year', ascending=False)

# maxYear = max(country_sorted["year"])
# minYear = min(country_sorted["year"])
maxYear = 2022
minYear = 1986

mask = world_csv["year"].astype(int) == 2022 # world_csv is not sorted by year so i'm using that rather than country_sorted
latestCountries = (world_csv.loc[mask])
elec_intensity = latestCountries.dropna(subset=['carbon_intensity_elec'])

# Mapping every country to it's carbon intensity of electricity value
elec_intensities_dict = pd.Series(elec_intensity["carbon_intensity_elec"].values, index=elec_intensity["country"]).to_dict()

elec_intensities_str = str(elec_intensities_dict).replace("'", '\"')

print(elec_intensities_str)

# Mapping choice to it's visual text for select field
categories = [
    ('biofuel_consumption', 'Primary energy consumption from biofuels(terawatt-hours)'),
    ('biofuel_electricity', 'Electricity generation from bioenergy(terawatt-hours)'),
    ('biofuel_share_elec', 'Share of electricity that comes from bioenergy(percentage of total electricity)'),
    ('coal_cons_per_capita', 'Coal consumption per capita(kilowatt-hours per person)'),
    ('coal_consumption', 'Primary energy consumption fomr coal(terawatt-hours)'),
    ('coal_elec_per_capita', 'Electricity generation from coal per person(kilowatt-hours per person)'),
    ('coal_electricity', 'Electricity generation from coal(terawatt-hours)'),
    ('coal_production', 'Coal production(terwatt-hours)'),
    ('electricity_demand', 'Electricity demand(terawatt-hours)'),
    ('electricity_generation', 'Total electricity generation(terawatt-hours)'),
    ('energy_per_capita', 'Primary energy consumption per capita(kilowatt-hours per person)'),
    ('fossil_elec_per_capita', 'Electricity generation from fossil fuels per person(kilowatt-hours per person)'),
    ('fossil_electricity', 'Electricity generation from fossil fuels(terawatt-hours)'),
    ('fossil_fuel_consumption', 'Primary energy consumption from fossil fuels(terawatt-hours)'),
    ('gas_consumption', 'Primary energy consumption from gas(terawatt-hours)'),
    ('gas_elec_per_capita', 'Electricity generation from gas per person(kilowatt-hours per person)'),
    ('gas_electricity', 'Electricity generation from gas(terawatt-hours)'),
    ('greenhouse_gas_emissions', "Emissions from electricity generation(megatonnes of CO2 equivalents)"),
    ('hydro_consumption', 'Primary energy consumption from hydropower(terawatt-hours, using substitution method)'),
    ('hydro_electricity', 'Electricity generation from hydropower(terawatt-hours)'),
    ("low_carbon_electricity", "Electricity generation from low-carbon sources(terawatt-hours)"),
    ('nuclear_electricity', 'Electricity generation from nuclear power(terawatt-hours)'),
    ('oil_electricity', 'Electricity generation from oil(terawatt-hours)'),
    ('renewables_electricity', 'Electricity generation from renewables(terawatt-hours)'),
    ('solar_electricity', 'Electricity generation from solar power(terawatt-hours)'),
    ('wind_electricity', 'Electricity generation from wind power(terawatt-hours)')
]

class MapForm(forms.Form):
    year = forms.IntegerField(label="Year", required=True, initial=maxYear, min_value=minYear, max_value=maxYear, widget=forms.TextInput(attrs={"class": "form-control"}))
    category = forms.CharField(widget=forms.Select(choices=categories, attrs={"class": "form-select"}))

class EnergyForm(forms.Form):
    #Energy Section
    # locations = [
    #     ("USA", "USA"),
    #     ("Canada", "Canada"),
    #     ("UK", "United Kingdom"),
    #     ("Europe", "Europe"),
    #     ("Africa", "Africa"),
    #     ("LatinAmerica", "Latin America"),
    #     ("MiddleEast", "Middle East"),
    #     ("OtherCountry", "Other")
    # ]
    countries = elec_intensity["country"]
    locations = [(country, country) for country in countries]

    location = forms.CharField(widget=forms.Select(choices=locations))
    energy = forms.FloatField(label="Average Weekly Energy Used(Kilowatt hours): ")

class TransportationForm(forms.Form):
    #Public Transportation
    transport_types = [
        ("Taxi", "Taxi"),
        ("ClassicBus", "Bus"),
        ("Coach", "Coach"),
        ("Subway", "Train"),
        ("LightRail", "LightRail")
    ]
    transport_type = forms.CharField(widget=forms.Select(choices=transport_types), label="Transportation Type: ")
    distance = forms.FloatField(label="Distance Traveled in KM: ")

class FlightForm(forms.Form):
    #Flight
    flight_types = [
        ("DomesticFlight", "Domestic Flight"),
        ("ShortEconomyClassFlight", "Short Economy Class Flight"),
        ("ShortBusinessClassFlight", "Short Business Class Flight"),
        ("LongEconomyClassFlight", "Long Economy Class Flight"),
        ("LongBusinessClassFlight", "Long Business Class Flight"),
    ]
    flight_type = forms.CharField(widget=forms.Select(choices=flight_types), label="Flight Type: ")
    flight_dist = forms.FloatField(label="Distance Traveled in KM: ")

class CarForm(forms.Form):
    #Car
    car_dist = forms.FloatField(label="Distance Travelled in KM: ")

class FuelForm(forms.Form):
    #Fuel
    fuel_type = forms.CharField(widget=forms.Select(choices=[("Petrol", "Petrol"), ("Diesel", "Diesel")]), label="Fuel Type: ")
    fuel_amount = forms.FloatField(label="Litres of fuel: ")



# Create your views here.
def index(request):
    return render(request, "greenClean/index.html")

def map(request):
    if request.method == "POST":
        form = MapForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            col = data["category"]
            year = data["year"]
    else:
        form = MapForm()
        col = "biofuel_consumption"
        year = 2022

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

    new_col = " ".join((col.split("_"))).title()
    title_text = new_col + " From " + str(year)

    fig.update_layout(
        title_text = title_text,
        title_x = 0.5,
        geo=dict(
            showframe = False,
            showcoastlines = False,
            projection_type = 'equirectangular'
        ),
        geo_bgcolor="#FFF"
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
        "form": form,
        "col": new_col,
        "year": year,
    })

def footprintCalculator(request):

    energyForm = EnergyForm()
    transportForm = TransportationForm()
    flightForm = FlightForm()
    carForm = CarForm()
    fuelForm = FuelForm()

    return render(request, "greenClean/carbonFootprint.html", {
        "energyForm": energyForm,
        "transportForm": transportForm,
        "flightForm": flightForm,
        "carForm": carForm,
        "fuelForm": fuelForm,
        "elec_intensities": elec_intensities_str
    })

def tips(request):
    return render(request, "greenClean/tips.html")