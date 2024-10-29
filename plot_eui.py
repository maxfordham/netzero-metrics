import pandas as pd
import altair as alt
from constants import PTH_EUI

def get_order(df):
    order = df[df.year == 2050]
    order = order[order["unit"] == "kWh/m²GIA/yr"]
    order = order[order["construction-delivery-type"] == "newbuild"]
    order = order.sort_values("benchmark-target", ascending=False)["building-type"].to_list()
    a, b = [f"{i} - RETROFIT" for i in order], [f"{i} - NEWBUILD" for i in order]
    return [j for i in zip(a,b) for j in i]
     
def plot_eui(fpth=PTH_EUI, save_png=True):
    df = pd.read_csv(fpth)
    order = get_order(df)
    data = df[df.unit == "kWh/m²GIA/yr"]

    data["construction-delivery-type"] = data["construction-delivery-type"].str.split("-", expand=True)[0]
    data["building-type"] = data["building-type"] + " - " + data["construction-delivery-type"].str.upper()

    chart = alt.Chart(data).mark_circle().encode(
        y= alt.Y("building-type", title=None, axis=alt.Axis(titleAlign="left", labelLimit=400, labelAlign="right")).sort(order),
        x= alt.Y("benchmark-target", title="Benchmark Target (KWHr / m2(GIA) / yr)"),
        color=alt.Color("year").scale(scheme="redblue")
    ).properties(height=700, 
                 title=alt.Title("Energy Use Intensity (EUI) Benchmarks",
                    subtitle=[
                        "EUI Benchmark in KWHr / m2(GIA) / yr (x-axis)",
                        "for new-build and retrofit-in-one-go buildings categorised by building type (y-axis)",
                        "with targets indicated by year, between now and 2050 (color)",
                        ])
                 ) 

    # chart.configure_title(
    #     fontSize=20,
    #     font='Courier',
    #     anchor='start',
    #     color='gray'
    # )
    

    if save_png:
        chart.save('eui-benchmarks.png', ppi=200)
        chart.save('eui-benchmarks.json')
    return chart

if __name__ == "__main__":
    plot_eui()