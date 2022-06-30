# # %%
# import geopy
# geolocator = geopy.Nominatim(user_agent="4adgapplication")
# location = geolocator.geocode(query='Asia',geometry='geojson', language='en')
# print(location.latitude, location.longitude)

# # %%
# import folium
# import os
# import io
# x = io.open('europe.json','r')

# m = folium.Map(
#     location=[-59.1759, -11.6016],
#     tiles="cartodbpositron",
#     zoom_start=2,
# )

# folium.GeoJson(x.read(), name="geojson").add_to(m)


# %%
import pandas as pd
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
d3_data

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
i=0
for customer in d3_data['children']:
    # print(customer['name'])
    G.add_node("customer_"+customer['name'],name=customer['name'], image=images["customer"])
    pos["customer_"+customer['name']]=[0, i*3]
    for application in customer['children']:
        G.add_node("application_"+application['name'], name=application['name'], image=images["application"])
        G.add_edge("customer_"+customer['name'],"application_"+application['name'])
        pos["application_"+application['name']]=[3, i*3]
        for volume in application['children']:
            G.add_node("volume_"+volume['name'], name=volume['name'], image=images["volume"])
            G.add_edge("application_"+application['name'],"volume_"+volume['name'])        
            pos["volume_"+volume['name']]=[6, i*3]
            for snapshot in volume['children']:
                G.add_node("snapshot_"+snapshot['name'], name=snapshot['name'], image=images["snapshot"])
                G.add_edge("volume_"+volume['name'],"snapshot_"+snapshot['name'])        
                pos["snapshot_"+snapshot['name']]=[9, i*3]
                i=i+2
                
        
    

# G.add_node("application", image=images["application"])
# for i in range(1, 4):
#     G.add_node(f"volume_{i}", image=images["volume"])
#     for j in range(1, 4):
#         G.add_node("snapshot_" + str(i) + "_" + str(j), image=images["snapshot"])

# G.add_edge("router", "volume_1")
# G.add_edge("router", "volume_2")
# G.add_edge("router", "volume_3")
# for u in range(1, 4):
#     for v in range(1, 4):
#         G.add_edge("volume_" + str(u), "snapshot_" + str(u) + "_" + str(v))

# Get a reproducible layout and create figure
# pos = nx.spring_layout(G, seed=1734289230)
fig, ax = plt.subplots()
print(pos['customer_CUST_00'])

# Note: the min_source/target_margin kwargs only work with FancyArrowPatch objects.
# Force the use of FancyArrowPatch for edge drawing by setting `arrows=True`,
# but suppress arrowheads with `arrowstyle="-"`
nx.draw_networkx_edges(
    G,
    pos=pos,
    ax=ax,
    arrows=True,
    arrowstyle="-",
    min_source_margin=15,
    min_target_margin=15,
    # connectionstyle="Arc3,rad=0.2"
)

# Transform from data coordinates (scaled between xlim and ylim) to display coordinates
tr_figure = ax.transData.transform
# Transform from display to figure coordinates
tr_axes = fig.transFigure.inverted().transform

# Select the size of the image (relative to the X axis)
icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.0025
icon_center = icon_size / 2.0
# Add the respective image to each node

# for n in G.nodes:
#     print(G.nodes[n])

for n in G.nodes:
    xf, yf = tr_figure(pos[n])
    xa, ya = tr_axes((xf, yf))
    # get overlapped axes and plot icon
    a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])
    a.imshow(G.nodes[n]["image"])
    a.axis("off")

plt.show()
