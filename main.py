import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.animation import FuncAnimation,PillowWriter
from matplotlib.ticker import ScalarFormatter,FuncFormatter
data=pd.read_csv("./input/data.csv")
data=data[(data.Code!="OWID_WRL")&(pd.notna(data.Code))]
data=data[(data.Year>=1900)]
fig,ax=plt.subplots(figsize=(9,5))
ax.set_xticks([]) #######
codes=pd.DataFrame()

codes["Code"]=data["Code"].unique() 
codes["colors"]=np.linspace(0, 1, len(data["Code"].unique()))
data=data.merge(codes,on="Code",how="left")

print(data)

def func(year):
    ax.clear()
    yearly_data=data[(data["Year"]==year)&(pd.notna(data["Code"]))]
    ax.set_ylabel("Million tons of CO2e",size=14)
    yearly_data=data[(data["Year"]==year)&(pd.notna(data["Code"]))].sort_values("Annual CO₂ emissions").tail(10)
    label=yearly_data.loc[yearly_data.Year==year,"Code"]
    h=yearly_data.loc[yearly_data["Year"]== year, "Annual CO₂ emissions"]
    ax.set_ylim(0,data["Annual CO₂ emissions"].max())

    ax.set_title(f"Yearly emissions in {year}",size=18,weight="bold")
    colormap=cm.viridis(yearly_data["colors"])
    ax.bar(x=label,height=h,color=colormap)
    ax.yaxis.set_major_formatter(ScalarFormatter())
    formatter = ScalarFormatter()
    formatter.set_scientific(False)  # Disable scientific notation
    ax.yaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x/1000000):,}"))
    ax.yaxis.set_minor_formatter(formatter)
    ax.tick_params(axis='both', which='major', labelsize=14)

animation=FuncAnimation(fig,func,frames=sorted(data["Year"].unique()))
animation.save("./animation.gif",dpi=100,writer=PillowWriter(fps=5))
plt.show()

