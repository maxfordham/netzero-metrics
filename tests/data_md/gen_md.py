import pathlib
import pandas as pd
import duckdb
from netzero_metrics.constants import nzdata

fdir = pathlib.Path(__file__).parent
fpth_md = fdir / "_test_data.md"

blngs = pd.read_csv((fdir / "bldgs.csv"))
areas = pd.read_csv((fdir / "areas.csv"))
areas_w_yr = areas.set_index("BuildingName")
areas_w_yr["TargetYear"] = blngs.set_index("Name")["TargetYear"]
areas_w_yr = areas_w_yr.reset_index()

eui_custom = pd.read_csv(fdir / "eui-custom.csv")
eui_uknzcb = nzdata.energy_use_intensity

q = """
SELECT * FROM eui_uknzcb
WHERE BuildingType IN (SELECT BuildingType FROM areas_w_yr)
AND ConstructionMethod IN (SELECT ConstructionMethod FROM areas_w_yr)
AND Year IN (SELECT TargetYear FROM areas_w_yr)
AND Unit = 'kWh/m²GIA/yr'
"""
eui_uknzcb_f = duckdb.sql(q).df()
s = f"""
# Buildings

{blngs.to_markdown(index=False)}

# Areas

{areas.to_markdown(index=False)}

# Areas with Year

{areas_w_yr.to_markdown(index=False)}

# Custom Energy Use Intensities

{eui_custom.to_markdown(index=False)}

# UKNZCB Energy Use Intensities

{eui_uknzcb_f.to_markdown(index=False)}

"""


fpth_md.write_text(s)