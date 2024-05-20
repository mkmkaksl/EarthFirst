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
from django.utils.html import strip_tags
from django.core.mail import EmailMessage, get_connection, EmailMultiAlternatives

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
    countries = elec_intensity["country"]
    locations = [(country, country) for country in countries]

    location = forms.CharField(widget=forms.Select(choices=locations))
    energy = forms.FloatField(label="Average Weekly Energy Used(Kilowatt hours): ", min_value=0)

class TransportationForm(forms.Form):
    #Public Transportation
    transport_types = [
        ("Taxi", "Taxi"),
        ("Bus", "Bus"),
        ("Coach", "Coach"),
        ("Subway", "Subway"),
        ("Light Rail", "Light Rail"),
        ("National Train", "National Train")
    ]
    transport_type = forms.CharField(widget=forms.Select(choices=transport_types), label="Transportation Type: ")
    distance = forms.FloatField(label="Average Weekly Distance Traveled(Kilometers): ")

class FlightForm(forms.Form):
    #Flight
    flight_types = [
        ("Domestic Flight", "Domestic Flight"),
        ("Short Economy Class Flight", "Short Economy Class Flight"),
        ("Short Business Class Flight", "Short Business Class Flight"),
        ("Long Economy Class Flight", "Long Economy Class Flight"),
        ("Long Business Class Flight", "Long Business Class Flight"),
    ]
    flight_type = forms.CharField(widget=forms.Select(choices=flight_types), label="Flight Type: ")
    flight_dist = forms.FloatField(label="Average Yearly Distance Traveled(Kilometers): ")

class CarForm(forms.Form):
    #Car
    cars = "Diesel Car,Petrol Car,Hybrid Car,Petrol Van,Diesel Van".split(",")
    carOptions = [(car, car) for car in cars]

    car_type = forms.CharField(widget=forms.Select(choices=carOptions), label="Car Type: ")
    car_dist = forms.FloatField(label="Average Weekly Distance Travelled(Kilometers): ")


# Create your views here.
def index(request):
    return render(request, "greenClean/index.html")

def solutions(request):
    return render(request, "greenClean/solutions.html")

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
            marker_line_width = 1,
            showscale=False,
        )
    )

    new_col = " ".join((col.split("_"))).title()
    title_text = new_col + " From " + str(year)

    fig.update_layout(
        title_text = title_text,
        title_x = 0.5,
        title_y = 0.98,
        title_font=dict(family="Gills", color="black", size=30),
<<<<<<< HEAD
=======
        
>>>>>>> 1fded25054dcded0c4ca023b39eb536ae4147a71
        geo=dict(
            showframe = False,
            showcoastlines = False,
            projection_type = 'equirectangular',
            bgcolor = "rgba(0, 0, 0, 0)",
        ),
        autosize=True,
        width=None,
        height=None,
        margin=dict(l=0, r=0, t=30, b=0),
        dragmode=False
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

    if request.method == "POST":
        data = request.POST
        print(data)
        energyData = {
            "location": data["location"],
            "energy": data["energy"]
        }
        energyForm = EnergyForm(energyData)

        transitData = {
            "transport_type": data["transport_type"],
            "distance": data["distance"]
        }
        transportForm = TransportationForm(transitData)

        flightData = {
            "flight_type": data["flight_type"],
            "flight_dist": data["flight_dist"]
        }
        flightForm = FlightForm(flightData)

        carData = {
            "car_type": data["car_type"],
            "car_dist": data["car_dist"]
        }
        carForm = CarForm(carData)

        print("Energy Data:")
        print(data["energy_co2"])
        total_prod = int(data["energy_co2"])
        total_prod += int(data["transport_co2"]) + int(data["flight_co2"]) + int(data["car_co2"])

    else:
        energyForm = EnergyForm()
        transportForm = TransportationForm()
        flightForm = FlightForm()
        carForm = CarForm()
        total_prod = 0

    return render(request, "greenClean/carbonFootprint.html", {
        "energyForm": energyForm,
        "transportForm": transportForm,
        "flightForm": flightForm,
        "carForm": carForm,
        "elec_intensities": elec_intensities_str,
        "total_prod": (total_prod / 1000)
    })

def tips(request):
    return render(request, "greenClean/tips.html")

def contact(request):
    if request.method == "POST":
            data = request.POST
            print(data)
            try:
                fName = data["fName"]
                lName = data["lName"]
                sender = data["sender"]
                subject = data["subject"]
                body = data["mail-body"]
            except KeyError:
                return render(request, "greenClean/contact.html", {
                                    "message": "Please make sure to fill out all the fields!"
                                })

            if not "@" in sender:
                return render(request, "greenClean/contact.html", {
                                    "message": "Input a valid email!"
                                })

            name = fName.title() + " " + lName.title()

            with get_connection(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT,
                username=settings.EMAIL_HOST_USER,
                password=settings.EMAIL_HOST_PASSWORD,
                use_tls=settings.EMAIL_USE_TLS
            ) as connection:
                html_message = f"""
<html>
<body>
<h4 style='font-size: 1.2rem;'> Dear {name}, </h4>
<p> Thank you for contacting us through the form on our website. We will evaluate & respond to your concerns within 2-3 business days. Thank you for your time.</p>
<p>Sincerely,</p>
<p>The Earth First Team.</p>
</body>
</html>
                """
                message = strip_tags(html_message)
                recipients = [sender]
                email = EmailMultiAlternatives("Thank you for reaching out to us", message, settings.EMAIL_HOST_USER, recipients, connection=connection)
                email.attach_alternative(html_message, "text/html")
                email.send()

                email = EmailMessage(subject, f"By {name} ({sender}),\n" + body, sender, [settings.EMAIL_HOST_USER], connection=connection).send()

    return render(request, "greenClean/contact.html", {
        "contacted": True
    })

def moreinfo(request):
<<<<<<< HEAD
    return render(request, "greenClean/moreInfo.html")
=======
    return render(request, "greenClean/moreinfo.html")
def documentation(request):
    return render(request, "greenClean/documentation.html")
>>>>>>> 1fded25054dcded0c4ca023b39eb536ae4147a71
