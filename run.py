import folium
import pandas as pd 
import numpy as np
import branca
from folium import plugins
import matplotlib.pyplot as plt
import openaq
from scipy.interpolate import griddata
import geojsoncontour
from datetime import date
import scipy as sp
import scipy.ndimage

api = openaq.OpenAQ()

city = input("Enter the city you want to analyze: ")
parameter = input("Enter the pollutant i.e PM2.5 (Input PM25), CO, PM10, O3, NO2, BC, SO2: ")
parameter = parameter.lower()
data = api.measurements(city=city, parameter=parameter, df=True)


#Uncomment the line below to plot for Entire India (PM2.5)

#data = pd.read_csv("openaq india pm2.5.csv")
data = data.drop(['city','country','date.utc','location','parameter','unit'],axis=1)
data.columns=['latitude','longitude','value']


colors = ['#d7191c',  '#fdae61',  '#ffffbf',  '#abdda4',  '#2b83ba']
colors = colors[::-1]
levels = len(colors)
vmin=data['value'].min()
vmax=data['value'].max()
cm = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax).to_step(levels)

x_orig = np.asarray(data.longitude.tolist())
y_orig = np.asarray(data.latitude.tolist())
z_orig = np.asarray(data.value.tolist())

x_arr = np.linspace(np.min(x_orig), np.max(x_orig), 5000)
y_arr = np.linspace(np.min(y_orig), np.max(y_orig), 5000)
x_mesh, y_mesh = np.meshgrid(x_arr, y_arr)

z_mesh = griddata((x_orig, y_orig), z_orig, (x_mesh, y_mesh), method='linear')
sigma = [5, 5]
z_mesh = sp.ndimage.filters.gaussian_filter(z_mesh, sigma, mode='constant')

contourf = plt.contourf(x_mesh, y_mesh, z_mesh, levels, alpha=0.5, colors=colors, linestyles='None', vmin=vmin, vmax=vmax)

geojson = geojsoncontour.contourf_to_geojson(
    contourf=contourf,
    min_angle_deg=3.0,
    ndigits=5,
    stroke_width=1,
    fill_opacity=0.5)

geomap = folium.Map([data.latitude.mean(), data.longitude.mean()], zoom_start=10, tiles="cartodbpositron")

folium.GeoJson(
    geojson,
    style_function=lambda x: {
        'color':     x['properties']['stroke'],
        'weight':    x['properties']['stroke-width'],
        'fillColor': x['properties']['fill'],
        'opacity':   0.6,
    }).add_to(geomap)

parameter=parameter.upper()
cm.caption = parameter+' Levels'
geomap.add_child(cm)
#plugins.Fullscreen(position='topright', force_separate_button=True).add_to(geomap)
