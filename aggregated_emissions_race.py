import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation,PillowWriter
from matplotlib.ticker import ScalarFormatter,FuncFormatter


data=pd.read_csv("./input/data.csv")
data=data[(data.Code!="OWID_WRL")&(pd.notna(data.Code))]
data=data[(data.Year>=1900)]
fig,ax=plt.subplots(figsize=(10,5))
ax.set_xticks([]) #######
codes=pd.DataFrame()

codes["Code"]=data["Code"].unique() 
codes["colors"]=np.linspace(0, 1, len(data["Code"].unique()))
data=data.merge(codes,on="Code",how="left")

#print(data)

data['Aggregated emissions'] = data.groupby('Code')['Annual CO₂ emissions'].cumsum()
print(data)
def func(year):
    ax.clear()
    cumulative_data=pd.pivot_table(data=data,values="Aggregated emissions",index="Year",columns="Code",aggfunc="sum")
    cumulative_data=cumulative_data[(cumulative_data["Year"]<=year)].sort_values("Aggregated emissions").tail(10)
    ax.set_ylabel("Million tons of CO2e",size=14)
    label=cumulative_data.loc[cumulative_data.Year<=year,"Year"]
    h=cumulative_data.loc[cumulative_data["Year"]<=year, "Aggregated emissions"] 
    #ax.set_ylim(0,cumulative_data.loc[(cumulative_data["Year"]==year),"Aggregated emissions"].max()*11/10)

    ax.set_title(f"Cumulative emissions from 1900 until {year}",size=18,weight="bold")
    colormap=cm.viridis(cumulative_data["colors"])
    ax.scatter(x=label,y=h,color=colormap)
    ax.yaxis.set_major_formatter(ScalarFormatter())
    formatter = ScalarFormatter()
    formatter.set_scientific(False)  # Disable scientific notation
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000000):,}"))
    ax.yaxis.set_minor_formatter(formatter)
    ax.tick_params(axis='both', which='major', labelsize=14)

animation=FuncAnimation(fig,func,frames=sorted(data["Year"].unique()))
animation.save("./aggregated_emissions.gif",dpi=100,writer=PillowWriter(fps=5))
plt.show()

