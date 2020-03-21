import pandas as pd
from urllib.request import urlopen
import json
import plotly.express as px
with urlopen('https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_municipalities.geojson') as response:
    municipalities = json.load(response)
giroDB = pd.read_csv('sediTappa.csv')

italianCitiesDB = giroDB[giroDB.Comune != 'Estero']
italianCitiesDB.drop(["Sede di Tappa", "Località"], axis = 1)
data = italianCitiesDB.groupby(by='Comune').max()['Ultima apparizione']
DB = italianCitiesDB.groupby(by='Comune').sum()
DB['Ultima apparizione'] = data
DB['Comune'] = list(DB.index)

for i in range(0, len(municipalities['features'])):
  municipalities['features'][i]['id'] = str(i)
DB['ID'] = '100000'
for municipality in municipalities['features']:
  if(municipality['properties']['name'] in DB['Comune']):
    DB['ID'][DB['Comune'] == municipality['properties']['name']] = municipality['id']

fig = px.choropleth_mapbox(DB, geojson=municipalities, locations='ID',
                           color='Totale',
                           color_continuous_scale="Viridis",
                           range_color=(1, 20),
                           mapbox_style="carto-positron",
                           zoom=4, center = {"lat": 42.875555, "lon": 12.524437},
                           opacity=0.5,
                           labels={'Totale':'Sedi di tappa'},
                           hover_name="Comune",
                           hover_data=["Partenze", "Arrivi", "Ultima apparizione"]
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()