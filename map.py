import folium
import pandas as pd


# Determine the color of the map point based on violation score
def getIconColor(score):
    
    if score < 60:
        return 'yellow'
    elif score < 70:
        return 'orange'
    else:
        return 'red'


# Declare the base map
map = folium.Map(location=[47.7257376,-122.219145549968], zoom_start=8, tiles='Mapbox Bright')

# The map FeatureGroup is a container that holds like features
violations_feature_group = folium.FeatureGroup(name='Violations')
geojson_feature_group = folium.FeatureGroup(name="Population")

df_violations = pd.read_csv('inspections.csv')
df_violations = df_violations[df_violations['inspection_score'] >= 50]

# Add the violation information to the feature group
for _, row in df_violations.iterrows():
    print("lat: {0}, lon: {1}, name: {2}".format(row['latitude'], row['longitude'], row['name']))
	
    violations_feature_group.add_child(folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=6,
        tooltip=row['name'],
        fill_color=getIconColor(row['inspection_score']),
        color='grey',
        fill=True,
        fill_opacity=1.0))

		
geojson_feature_group.add_child(folium.GeoJson(
    data=open("world.json", 'r', encoding="utf-8-sig").read(),
    style_function=lambda x: {"fillColor":"yellow"}))

# Add the feature groups to the map
map.add_child(violations_feature_group)
map.add_child(geojson_feature_group)

# Add the layer control feature to select which layers are visible
map.add_child(folium.LayerControl())

map.save('Violations_map.html')