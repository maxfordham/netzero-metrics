import pandas as pd
from constants import PTH_EUI_IN, PTH_EUI, PTH_BUILDING_TYPES

def get_sheet_data(PTH, sheet_name):
    construction_deleivery_type = sheet_name
    meta = pd.read_excel(PTH, sheet_name=sheet_name, nrows=2)
    meta = (
        meta.set_index("building-type-shorthand")
        .T.reset_index(drop=False)
        .rename(columns={"year": "building-type", "index": "building-type-shorthand"})
    )
    data = pd.read_excel(PTH, sheet_name=sheet_name, skiprows=2)
    data = pd.melt(
        data, id_vars="year", var_name="building-type", value_name="benchmark-target"
    )

    data = data.join(meta.set_index('building-type'), on="building-type")
    data["construction-delivery-type"] = construction_deleivery_type
    cols = ["building-type","building-type-shorthand","unit","construction-delivery-type"]
    for x in cols:
        data[x] = data[x].str.strip()

    data["building-type"] = data["building-type"].str.replace(" (GIA)", "")
    data["building-type"] = data["building-type"].str.replace(" (NIA)", "")
    return data

sheet_names = ["newbuild", "retrofit-in-one-go"]
data = pd.concat([get_sheet_data(PTH_EUI_IN, sheet_name=s) for s in sheet_names], axis=0) 

data.to_csv(PTH_EUI, index=False)
li_types = list(data["building-type"].unique())
PTH_BUILDING_TYPES.write_text("\n".join(li_types))