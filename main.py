import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation,PillowWriter
data=pd.read_csv("./input/data.csv")
data=data[(data.Code!="OWID_WRL")&(pd.notna(data.Code))]

fig,ax=plt.subplots()
ax.set_xticks([]) #######
plt.xticks(rotation=45,ha="right")
codes=pd.DataFrame()

codes["Code"]=data["Code"].unique() 
codes["colors"]=np.linspace(0, 1, len(data["Code"].unique()))
data=data.merge(codes,on="Code",how="left")

print(data)

def func(year):
    ax.clear()
    yearly_data=data[(data["Year"]==year)&(pd.notna(data["Code"]))]
    

    yearly_data=data[(data["Year"]==year)&(pd.notna(data["Code"]))].sort_values("Annual CO₂ emissions").tail(10)
    label=yearly_data.loc[yearly_data.Year==year,"Code"]
    h=yearly_data.loc[yearly_data["Year"]== year, "Annual CO₂ emissions"]
    ax.set_ylim(0,data["Annual CO₂ emissions"].max())
    ax.set_title(f"Yearly emissions in {year}")
    colormap=cm.viridis(yearly_data["colors"])
    ax.bar(x=label,height=h,color=colormap)


animation=FuncAnimation(fig,func,frames=sorted(data["Year"].unique()))
#animation.save("./animation.gif",dpi=50,writer=PillowWriter())
plt.show()

