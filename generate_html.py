 
color_sequence = ["#32DACF","#7630EF","#00526F","#7FF9E2","#C14DFF","#FF8300","#FEC901"]

# from IPython.display import HTML
 
import pandas as pd
import os

vols_df = pd.read_csv('sunburst_data.csv')
snaps_orphaned = vols_df[vols_df.VolumeId.isnull()]
vols_df = vols_df[vols_df.VolumeId.notnull()]
#vols_df

def create_html(figure, name):
    if(os.path.exists("data/"+name+".html")):
        os.remove("data/"+name+".html")
    
    figure.write_html("data/"+name+".html")


# ## Statistics and Counters 
#     # Volumes, Snapshots, Un attached and Attached EBS Volumes
#     # Volumes, Snapshots for On Prem Volumes

 
EBSVols = vols_df[vols_df['volumeType']=='EBS']
onPremVols = vols_df[vols_df['volumeType']=='OnPrem']
ebsVolCount = EBSVols['VolumeId'].nunique()
ebsVOLSnapshots = EBSVols['snapshotId'].nunique()
onPremVolCount = onPremVols['VolumeId'].nunique()
onPremVOLSnapshots = onPremVols['snapshotId'].nunique()
unattachedEBSVols = EBSVols[EBSVols['isAttached']==False]['VolumeId'].nunique()
unattachedOnPremVols = onPremVols[onPremVols['isAttached']==False]['VolumeId'].nunique()
from tabulate import tabulate
infoEBS = {'Volume Type': ['Total Volumes', 'Unattached EBS Volumes', 'Total Snapshots', 'Orphaned Snapshots'], 
        'EBS': [ebsVolCount, unattachedEBSVols, ebsVOLSnapshots, snaps_orphaned.nunique().snapshotId ]}
infoOnPrem = {'Volume Type': ['Total Volumes', 'Unattached OnPrem Volumes', 'Total Snapshots'], 
        'OnPrem': [onPremVolCount, unattachedOnPremVols, onPremVOLSnapshots ]}
print(tabulate(infoEBS, headers='keys',tablefmt='fancy_grid'))
print(tabulate(infoOnPrem, headers='keys',tablefmt='fancy_grid'))

 
#vols_df['vol_creation_time']= pd.to_datetime(vols_df['vol_creation_time'], utc=True).ini_time_for_now
from datetime import datetime, timedelta
vols_df['vol_creation_time'] = vols_df['vol_creation_time'].apply(lambda x: pd.to_datetime(x).tz_localize(None))
# Using current time
ini_time_for_now = datetime.utcnow()
vols_df['volumeAgeDays']=vols_df['vol_creation_time'].apply(lambda x: (ini_time_for_now -x ).days)
#vols_df.info()
#vols_df
# print( type(vols_df['vol_creation_time'][0]))

 
import plotly.io as pio
pio.renderers.default = "notebook"

# ## Region Distribution of EBS Volumes - Stack Rank by Volume age vs IOPS
# 
#     # This graph shows the distribution of the EBS volumes in different Regions and stack ranks between IOPS and Volume Age
#     # Shows volume age vs iops distribution for different regions

 


 
import plotly.express as px


fig = px.scatter(vols_df, x="volumeAgeDays", y="iops",
	         size="volumeSize", color="Region",
                 hover_name="VolumeId", log_x=True, size_max=60, color_discrete_sequence=color_sequence)
create_html(fig,"region_distribution")

 #  # fig.show()

# ## Consumption EBS and OnPrem Volume
# 
# - Displays the size footprint for various asset types( Attached/Unattached EBS and OnPrem Volumes)

 
import plotly.express as px
import numpy as np
vols_grouped = vols_df.groupby(['volumeType','isAttached'])
vols_grouped = vols_grouped.sum().reset_index()
vols_grouped
vols_grouped['assetType'] = np.where((vols_grouped['volumeType'] == 'EBS') & (vols_grouped['isAttached'] == True), 'AttachedEBS',
                   np.where((vols_grouped['volumeType'] == 'OnPrem') & (vols_grouped['isAttached'] == True), 'AttachedOnPrem',
                   np.where((vols_grouped['volumeType'] == 'EBS') & (vols_grouped['isAttached'] == False), 'UnattachedEBS', 'UnattachedOnPrem')))
vols_grouped
fig = px.bar(vols_grouped, x='assetType', y='volumeSize',
             hover_data=['Cost', 'volumeSize'], color='assetType',
             height=400, color_discrete_sequence=color_sequence)

create_html(fig,"consumption_1")

 # fig.show()

#df = px.data.tips() # replace with your own data source


# fig_consumption = px.pie(vols_grouped,  hole=.3)
# fig_consumption.show()

 
import plotly.express as px
vols_grouped = vols_df.groupby(['volumeType','isAttached'])
vols_grouped = vols_grouped.sum().reset_index()
vols_grouped
vols_grouped['assetType'] = np.where((vols_grouped['volumeType'] == 'EBS') & (vols_grouped['isAttached'] == True), 'AttachedEBS',
                   np.where((vols_grouped['volumeType'] == 'OnPrem') & (vols_grouped['isAttached'] == True), 'AttachedOnPrem',
                   np.where((vols_grouped['volumeType'] == 'EBS') & (vols_grouped['isAttached'] == False), 'UnattachedEBS', 'UnattachedOnPrem')))
vols_grouped
fig = px.pie(vols_grouped, hole=.8, values='volumeSize', names='assetType', title='Distribution of attached/unattached EBS, Onprem volumes', hover_data=['Cost'], color_discrete_sequence=color_sequence)

create_html(fig,"consumption_2")

 # fig.show()


# ## Trends on EBS Volume Consumption and IOPS 
# - Displays avg EBS volume footprint and IOPS trends

 
import plotly.graph_objects as go
vols_capacity_trend_df = pd.read_csv('volume_capacity_iops_trend.csv')
vols_capacity_trend_df_final = vols_capacity_trend_df.sort_values('reportDate')
Date = vols_capacity_trend_df_final['reportDate']
IOps = vols_capacity_trend_df_final['iops_avg']
read_iops = vols_capacity_trend_df_final['read_iops_avg']
write_iops = vols_capacity_trend_df_final['write_iops_avg']
GiB = vols_capacity_trend_df_final['volumeUsedSize(GiB)']

# centre = (min(IOps)+max(IOps))/2
# mul=0.7

# for i in range(len(IOps)):
# #     print(val)
#     val=IOps[i]
#     if val>centre:
#         val = val - abs(val-centre)*mul
#     else:
#         val = val + abs(val-centre)*mul
#     IOps[i]=val

# print(IOps)

df = pd.DataFrame(list(zip( IOps , GiB, read_iops, write_iops )),
                  index = Date ,
                columns = [ 'IOps' , 'GiB', 'read_iops', 'write_iops' ]).reset_index()  
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig = make_subplots()

# Add traces
fig.add_trace(
    go.Scatter(x=df['reportDate'], y=df['IOps'], name="IOPS",line=dict(shape='spline',color=color_sequence[1]))
)

# Add figure title
# fig.update_layout(
#     title_text="Volume footprint and IOPS trends"
# )

# Set x-axis title
fig.update_xaxes(title_text="Report Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>IOPS</b>")

create_html(fig,"trend_1_1")

 # fig.show()

 
fig = make_subplots()

# Add trace
fig.add_trace(
    go.Scatter(x=df['reportDate'], y=df['GiB'], name="Volume used capacity(GB)",line=dict(shape='spline',color=color_sequence[5]))
)

# Add figure title
# fig.update_layout(
#     title_text="Volume footprint and IOPS trends"
# )

# Set x-axis title
fig.update_xaxes(title_text="Report Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Used capacity (GB)</b>")

create_html(fig,"trend_1_2")

 # fig.show()

#   [markdown]
# ##  EBS volumes Read IO and write IO Trends 
#  - Displays avg EBS volume footprint and IOPS trends

 
fig = make_subplots()

# Add traces
fig.add_trace(
    go.Scatter(x=df['reportDate'], y=df['read_iops'], name="Avg Read IOPS",line=dict(shape='spline',color=color_sequence[1])),
)

# Add figure title
fig.update_layout(
    title_text="Volume Read IOPS trends"
)

# Set x-axis title
fig.update_xaxes(title_text="Report Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Read IOPS</b>")

create_html(fig,"trend_2_1")

 # fig.show()

 
fig = make_subplots()

# Add traces

fig.add_trace(
    go.Scatter(x=df['reportDate'], y=df['write_iops'], name="Avg Write IOPS",line=dict(shape='spline',color=color_sequence[5])),
)

# Add figure title
fig.update_layout(
    title_text="Volume Write IOPS trends"
)

# Set x-axis title
fig.update_xaxes(title_text="Report Date")

# Set y-axes titles
fig.update_yaxes(title_text="<b>Write IOPS</b>")

create_html(fig,"trend_2_2")

 # fig.show()

#   [markdown]
# ## Stack Rank IOPS, Age on EBS and OnPrem
# - Shows age of the volumes vs the IOPS (Bubble size correspons to the volume size)

 
import plotly.express as px


fig = px.scatter(vols_df, x="volumeAgeDays", y="iops",
	         size="volumeSize", color="volumeType",
                 hover_name="VolumeId", log_x=True, size_max=60,color_discrete_sequence=color_sequence)

create_html(fig,"trend_3")

 # fig.show()

#   [markdown]
# ## EBS Volume and Snapshot distributions for a customer 
# (Green for attached, Orange for unattached). 
# - Shows the customer lineage (Customer -> Volumes(Attached/ Unattached) -> Snapshots

 
import plotly.express as px
customerId = vols_df['CustomerId']
volumeId = vols_df['VolumeId']
snapshotId = vols_df['snapshotId']
isAttached = vols_df['isAttached']
df_final = pd.DataFrame(
    dict(customerId=customerId, volumeId=volumeId,snapshotId=snapshotId,isAttached = isAttached)
)
df_final
fig1 = px.treemap(df_final, path=['customerId', 'volumeId', 'snapshotId'], color='isAttached',
                 hover_data=['customerId', 'volumeId', 'snapshotId']
                  ,color_discrete_sequence=color_sequence)
#                 color_discrete_map={False:'blue', True:'lightgreen'})
fig1.update_traces(root_color="blue")
fig1.update_layout(margin = dict(t=50, l=25, r=25, b=25))

create_html(fig1,"trend_4")

# fig1.show("notebook")

#   [markdown]
# ##   Cost Distribution  EBS Vs OnPrem
# - Shows volumetype distribution(EBS/OnPrem) based on cost and the corresponding snapshot lineage

 
import plotly.express as px
import numpy as np

continous_color_pallete = [color_sequence[3],color_sequence[0],color_sequence[1],color_sequence[2]]

fig = px.sunburst(vols_df, path=['volumeType', 'VolumeId','snapshotId'], width=750, height=750,
                    color_continuous_scale=continous_color_pallete
#                   color_continuous_scale="RdYlGn"
                  ,values='Cost', color='Cost')

create_html(fig,"cost_1")

 # fig.show()

#   [markdown]
# ## Volume Consumption  OnPrem Vs EBS
# - Shows volumetype distribution(EBS/OnPrem) based on volumeSize and the corresponding snapshot lineage

 

import plotly.express as px
import numpy as np
fig = px.sunburst(vols_df, path=['volumeType', 'VolumeId','snapshotId'], width=750, height=750,
                  color_continuous_scale=continous_color_pallete
#                   color_continuous_scale="RdBu"
                  ,values='volumeSize', color='volumeSize')

create_html(fig,"cost_2")

 # fig.show()

 
# vols_df

 
# # !jupyter nbconvert --to html ElasticBlockStore-Demo-Sriram.ipynb

month_list = ['April','April','May','May','June','June']
cost_list = [1400,1740,1320,1570,790,1030]
type_list = ['EBS','OnPrem','EBS','OnPrem','EBS','OnPrem']
costs_df = pd.DataFrame(list(zip(type_list, cost_list, month_list)),columns=['type','cost','month'])
fig = px.bar(costs_df, x="month", y="cost", color="type",color_discrete_sequence=[color_sequence[2],color_sequence[0]])
create_html(fig,'cost_3')
