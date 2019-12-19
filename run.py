import folium
import pandas as pd 
import folium
from folium.plugins import HeatMap

hmap = folium.Map(location=[20.6, 79], zoom_start=4, legend_name = 'Number of incidents per district',)

data = pd.read_csv("openaq india 19-12-2019.csv")
data = for_map.drop(['location','city','country','utc','local','parameter','unit','attribution'],axis=1)

max_amount = float(data['value'].max())


hm_wide = HeatMap( list(zip(data.latitude.values, data.longitude.values, data.value.values)),
                   min_opacity=0.5,
                   max_val=max_amount,
                   radius=17, blur=5, 
                   max_zoom=1,
                   
                 )

hmap.add_child(hm_wide)
