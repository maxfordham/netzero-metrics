# Examples for Testing and Comprehension

## calc_area_weighted_target

```py
import numpy as np
from netzero_metrics.calcs import calc_area_weighted_target

trgt = np.array([10, 20, 30])
area = np.array([1, 2, 3])
print(calc_area_weighted_target(trgt, area))
#> 23.333333333333332
```

## [mdpd-#50](https://github.com/kyoto7250/mdpd/issues/50)

```py
import mdpd

areas = mdpd.from_md(
    """
|   GrossInternalArea | BuildingType                          | ConstructionMethod   | BuildingName   |
|--------------------:|:--------------------------------------|:---------------------------|:---------------|
|                  10 | Office - General                      | newbuild                   | A              |
|                  10 | Office - General                      | retrofit-in-one-go         | A              |
|                  20 | Commercial Resi - Student Residential | newbuild                   | B              |
|                  20 | Commercial Resi - Student Residential | retrofit-in-one-go         | B              |
"""
)
print(areas["GrossInternalArea"].dtype)
#> object



areas["GrossInternalArea"] = areas["GrossInternalArea"].astype(int)
print(areas["GrossInternalArea"].dtype)
#> int64

```

## plot_great_tables_targets

```py
from netzero_metrics.calcs import (
    get_area_and_target_summaries,
)
from netzero_metrics.tables import plot_great_tables_targets
import mdpd

df_all_building_targets = mdpd.from_md("""
|    | TargetName      | BuildingName   |   Target |
|---:|:----------------|:---------------|---------:|
|  0 | UK NZC Standard | Block A        | 137.3    |
|  1 | ambitious!      | Block A        |  40.0701 |
|  2 | UK NZC Standard | Block B        | 251.333  |
|  3 | ambitious!      | Block B        |  65.3333 |
""")

df_all_project_targets = mdpd.from_md("""
|    | TargetName      |   ProjectTarget |
|---:|:----------------|----------------:|
|  0 | UK NZC Standard |         165.526 |
|  1 | ambitious!     |          43.837 |
""")

ch = plot_great_tables_targets(df_all_building_targets, df_all_project_targets)
print(ch._tbl_data.to_pandas().to_markdown())
"""
|    | TargetName      |   Block A |   Block B |   Project |
|---:|:----------------|----------:|----------:|----------:|
|  0 | UK NZC Standard |  137.3    |  251.333  |   165.526 |
|  1 | ambitious!      |   40.0701 |   65.3333 |    43.837 |
"""
```

## plot_great_tables_area_summary

```py
import mdpd
from netzero_metrics.tables import (
    plot_great_tables_area_summary,
)

area = mdpd.from_md("""
|    | BuildingId   |   GrossInternalArea | BuildingType                          | ConstructionMethod   | BuildingName   |   TargetYear |
|---:|:-------------|--------------------:|:--------------------------------------|:---------------------------|:---------------|-------------:|
|  0 | BLDG-1       |                  50 | Office - General                      | newbuild                   | Block A        |         2025 |
|  1 | BLDG-1       |                 300 | Commercial Resi - Student Residential | retrofit-in-one-go         | Block A        |         2025 |
|  2 | BLDG-2       |                  50 | Hotel                                 | newbuild                   | Block B        |         2030 |
|  3 | BLDG-1       |                  50 | Office - Trading Floors               | newbuild                   | Block A        |         2025 |
|  4 | BLDG-1       |                   3 | Office - General                      | newbuild                   | Block A        |         2025 |
|  5 | BLDG-2       |                 100 | Hotel                                 | retrofit-in-one-go         | Block B        |         2030 |
|  6 | BLDG-1       |                 400 | Healthcare                            | retrofit-in-one-go         | Block A        |         2025 |
"""
)
area["GrossInternalArea"] = area["GrossInternalArea"].astype(float)
ch = plot_great_tables_area_summary(
    area,
)
print(ch._tbl_data.to_pandas().to_markdown())
"""
|    | BuildingType                          | ConstructionMethod   |   Block A |   Block B |   Total |
|---:|:--------------------------------------|:---------------------|----------:|----------:|--------:|
|  0 | Commercial Resi - Student Residential | retrofit-in-one-go   |       300 |         0 |     300 |
|  1 | Healthcare                            | retrofit-in-one-go   |       400 |         0 |     400 |
|  2 | Hotel                                 | newbuild             |         0 |        50 |      50 |
|  3 | Hotel                                 | retrofit-in-one-go   |         0 |       100 |     100 |
|  4 | Office - General                      | newbuild             |        53 |         0 |      53 |
|  5 | Office - Trading Floors               | newbuild             |        50 |         0 |      50 |
|  6 | Total                                 |                      |       803 |       150 |     953 |
"""
```

## plot_energy_consumption

```py
import pandas as pd
from IPython.display import display
from netzero_metrics.plots import (
    plot_energy_consumption,
)
df = pd.DataFrame([
    {
       'FuelType': 'Electricity',
       'EnergyConsumption': 100.0,
       'ReportingPeriod': '2019/20',
       'EnergyEndUse': 'Heating',
       'EnergyEndUseTags': '[]',
   },
   {
       'FuelType': 'Electricity',
       'EnergyConsumption': 50.0,
       'ReportingPeriod': '2019/20',
       'EnergyEndUse': 'Cooling',
       'EnergyEndUseTags': '[]',
   },
])
plot = plot_energy_consumption(df)
display(plot)
print(plot)
#> alt.Chart(...)
```
