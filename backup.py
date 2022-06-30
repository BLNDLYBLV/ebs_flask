# %%
import pandas as pd
import geopy
import random
from shapely.geometry import shape, Point
import json
import folium
import os
import io

vols_df = pd.read_csv('sunburst_data_v2.csv')


x = io.open('continents.json','r')
y=json.load(x);

continents_shape = {}
continents_centroid = {}
geolocator = geopy.Nominatim(user_agent="4adgapplication")

for (key, item) in y.items():
    continents_shape[key] = shape(item['geometry'])
    loc = geolocator.geocode(query=key,geometry='geojson', language='en')
    continents_centroid[key] = [loc.latitude,loc.longitude]


# %%
unique_vols_df = vols_df.groupby('VolumeId')
points=[]
for id, item in unique_vols_df:
    region = item["Region"].unique()[0]
    centroid = continents_centroid[region]
    cur_shape = continents_shape[region]
    x=centroid[0]+random.randint(-10,10)
    y=centroid[1]+random.randint(-10,10)
    i=0
    while(i<10 and cur_shape.contains(Point(x,y))=='False'):
        x=centroid[0]+random.randint(-10,10)
        y=centroid[1]+random.randint(-10,10)
        i = i+1
    points.append([x,y])    

# %%
x = io.open('europe.json','r')

m = folium.Map(
    location=[-59.1759, -11.6016],
    tiles="cartodbpositron",
    zoom_start=2,
)
for p in points:
    # folium.Circle(p,20000).add_to(m)
    folium.CircleMarker(p,5,fill=True,color='#000000', opacity=0, stroke=False).add_to(m)

# folium.PolyLine([random_europe[0],random_europe[1]]).add_to(m)
# folium.GeoJson(x.read(), name="geojson").add_to(m)
m

# %%
from shapely.geometry import MultiPolygon, shape, Point
import json
x = io.open('europe.json','r')

y=json.load(x);
t=y['geometry']['coordinates']
z = shape(y['geometry'])
# p = Point((t[5][0][0][0]+t[5][0][10][0]+t[5][0][2][0])/3,(t[5][0][0][1]+t[5][0][1][1]+t[5][0][2][1])/3)
for point in random_europe:
    p = Point(point[1],point[0])
    print(z.contains(p), p)


# %%
import os

vols_df = pd.read_csv('sunburst_data_v2.csv')

vols_df[0:10]

order = ['CustomerId', 'ApplicationId', 'VolumeId', 'snapshotId']

def make_heirarchy(items, p_id, i):
    id_data = {
        "name" :  p_id,
        "children" : []
    }
    for id, item in items:
        if i!= (len(order)):
            res = make_heirarchy(item.groupby(order[i]), id, i+1)
            id_data["children"].append(res)
        else:
            id_data["children"].append({
                "name" : id,
                "size": int(float(item['volumeSize'].to_string(index=False))),
                "isAttached" : bool(item['isAttached'].to_string(index=False))
            })
    return id_data

d3_data=make_heirarchy(vols_df.groupby(order[0]), 'Data',1)
# d3_data

# %%
import matplotlib.pyplot as plt
import networkx as nx
import PIL

# Image URLs for graph nodes
icons = {
    "customer": "static/images/customer.png",
    "application": "static/images/application.png",
    "volume": "static/images/volume.png",
    "snapshot": "static/images/snapshot.png",
}

# Load images
images = {k: PIL.Image.open(fname) for k, fname in icons.items()}

# Generate the computer network graph
G = nx.Graph()
pos = {};
c_num = 0
a_num = 0
v_num = 0
s_num = 0
for customer in d3_data['children']:  
    c_num = c_num + 1
    G.add_node("customer_"+customer['name'],name=customer['name'], type="customer", image=images["customer"])
    for application in customer['children']:
        a_num = a_num + 1
        G.add_node("application_"+application['name'], name=application['name'], type="application", image=images["application"])
        G.add_edge("customer_"+customer['name'],"application_"+application['name'])
        for volume in application['children']:
            v_num = v_num + 1
            G.add_node("volume_"+volume['name'], name=volume['name'], type="volume", image=images["volume"])
            G.add_edge("application_"+application['name'],"volume_"+volume['name'])        
            for snapshot in volume['children']:
                s_num = s_num + 1 
                G.add_node("snapshot_"+snapshot['name'], name=snapshot['name'], type="snapshot", image=images["snapshot"])
                G.add_edge("volume_"+volume['name'],"snapshot_"+snapshot['name'])        



# %%

c_cur = c_num
c_mul = 30
a_cur = a_num
a_mul = 20
v_cur = v_num
v_mul = 20
s_cur = s_num
s_mul = 5

for customer in d3_data['children']:  
    pos["customer_"+customer['name']]=[0, (c_num/2 - c_cur)*c_mul]
    c_cur = c_cur - 1
    for application in customer['children']:
        pos["application_"+application['name']]=[1, (a_num/2 - a_cur)*a_mul]
        a_cur = a_cur - 1
        for volume in application['children']:
            pos["volume_"+volume['name']]=[2, (v_num/2 - v_cur)*v_mul]
            v_cur = v_cur - 1
            for snapshot in volume['children']:
                pos["snapshot_"+snapshot['name']]=[3, (s_num/2 - s_cur)*s_mul]
                s_cur = s_cur - 1


# %%
fig, ax = plt.subplots()
ax.set_xlim(-1,4)

nx.draw_networkx_edges(
    G,
    pos=pos,
    ax=ax,
    arrows=True,
    arrowstyle="-",
    min_source_margin=30,
    min_target_margin=30,
    connectionstyle="Arc3,rad=0.01"
)

tr_figure = ax.transData.transform
tr_axes = fig.transFigure.inverted().transform

icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.005
icon_center = icon_size / 2.0

for n in G.nodes:
    xf, yf = tr_figure(pos[n])
    xa, ya = tr_axes((xf, yf))
    if(G.nodes[n]["type"]=='snapshot'):
        a = plt.axes([xa - icon_center*0.5, ya - icon_center*0.5, icon_size*0.5, icon_size*0.5])
    else:
        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
    a.imshow(G.nodes[n]["image"])
    if(G.nodes[n]["type"]=='snapshot'):
        a.text(50, 30, G.nodes[n]["name"])
    if(G.nodes[n]["type"]=='volume'):
        a.text(-10, 80, G.nodes[n]["name"])
    if(G.nodes[n]["type"]=='application'):
        a.text(20, 80, G.nodes[n]["name"])
    if(G.nodes[n]["type"]=='customer'):
        a.text(5, 70, G.nodes[n]["name"])
    a.axis("off")

f = plt.gcf()
plt.show()
plt.draw()
# os.remove('cust_00.png')
f.savefig('cust_00.png',dpi=100)


