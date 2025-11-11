"""Calculations for Net Zero Energy Use Intensity targets.

The same test data is used throughout the docs as follows:

```{python}
from netzero_metrics.calcs import get_test_data
_area, _bldg, area, eui_custom = get_test_data()
import ipywidgets as w
from ipydatagrid import DataGrid

def grid(df): return DataGrid(df, auto_fit_columns=True, layout=w.Layout(height="200px"))

w.Tab(
    [grid(_area), grid(_bldg), grid(area), grid(eui_custom)],
    titles=["_area", "_bldg", "area", "eui_custom"]
)
```
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import duckdb
import numpy as np
import pandas as pd

from netzero_metrics.constants import EUI_DATA, NZC_TARGET_NAME

if TYPE_CHECKING:
    from netzero_metrics.models import (
        AreaDataFrame,
        EuiTargetDataFrame,
        EuiTargetUknzcbDataFrame,
    )


def get_test_data() -> tuple[pd.DataFrame, pd.DataFrame, AreaDataFrame, pd.DataFrame]:
    """Return test data for the calculations."""
    _area = pd.DataFrame({
        "BuildingId": [1,1,2,2,2],
        "GrossInternalArea": [10, 10, 20, 20, 20],
        "BuildingType": [
            "Office - General",
            "Office - General",
            "Commercial Resi - Student Residential",
            "Commercial Resi - Student Residential",
            "Commercial Resi - Student Residential",
        ],
        "ConstructionMethod": [
            "newbuild",
            "retrofit-in-one-go",
            "newbuild",
            "retrofit-in-one-go",
            "retrofit-in-one-go",
        ],
        "BuildingName": ["A", "A", "B", "B", "B"],
    })
    _bldg = pd.DataFrame({
        "BuildingId": [1, 2],
        "TargetYear": [2025, 2030],
        "Name": ["A", "B"],
    })
    area = attach_target_year_to_area(_area, _bldg)
    eui_custom = pd.DataFrame({
        "BuildingType": [
            "Office - General",
            "Office - General",
            "Office - Trading Floors",
            "Hotel",
            "Hotel",
            "Commercial Resi - Student Residential",
            "Healthcare",
        ],
        "Target": [70.0, 70.0, 70.0, 70.0, 70.0, 70.0, 70.0],
        "Description": [
            "better than NZC target!",
            "better than NZC target!",
            "better than NZC target!",
            "better than NZC target!",
            "better than NZC target!",
            "better than NZC target!",
            "better than NZC target!",
        ],
        "TargetName": [
            "ambitious!",
            "ambitious!",
            "ambitious!",
            "ambitious!",
            "ambitious!",
            "ambitious!",
            "ambitious!",
        ],
        "ConstructionMethod": [
            "newbuild",
            "newbuild",
            "newbuild",
            "newbuild",
            "retrofit-in-one-go",
            "retrofit-in-one-go",
            "retrofit-in-one-go",
        ],
    })
    return _area, _bldg, area, eui_custom


# -
def calc_area_weighted_target(trgt: np.array, area: np.array) -> float:
    """Return the weighted average target.

    This is calculated by taking the summation of "the product of the area weights times the targets" divided by
    "the sum of the area weights". If all the area weights are same, weighted average is equivalent to the average.

    ```python
    # noqa: D100
    import numpy as np
    from netzero_metrics.calcs import (
        calc_area_weighted_target,
    )

    trgt = np.array([1, 2])
    area = np.array([1, 2])
    print(
        calc_area_weighted_target(trgt, area)
    )  # noqa: T201
    #> 1.6666666666666665
    ```
    """
    area_w = area / area.sum()
    return (trgt * area_w).sum()

def attach_target_year_to_area(
    _area: pd.DataFrame,
    _bldg: pd.DataFrame,
) -> AreaDataFrame:
    """Attach building `TargetYear` onto area.

    ```{python}
    # docs display
    from netzero_metrics.calcs import attach_target_year_to_area, get_test_data
    _area, _bldg, area, eui_custom = get_test_data()
    import ipywidgets as w
    from ipydatagrid import DataGrid
    def grid(df): return DataGrid(df, auto_fit_columns=True, layout=w.Layout(height="200px"))

    area = attach_target_year_to_area(_area, _bldg)
    display(w.Tab([grid(_area), grid(_bldg), grid(area)], titles=["_area", "_bldg", "area"]))
    ```

    ```python
    # noqa: D100
    # pytest-examples
    from netzero_metrics.calcs import (
        attach_target_year_to_area,
        get_test_data,
    )

    _area, _bldg, area, eui_custom = get_test_data()
    area = attach_target_year_to_area(_area, _bldg)
    print(area.TargetYear.to_list())  # noqa: T201
    #> [2025, 2025, 2030, 2030, 2030]
    ```
    """
    duckdb.register("_area", _area)
    duckdb.register("_bldg", _bldg)
    q = """
    SELECT            _area.BuildingId, GrossInternalArea, BuildingType, ConstructionMethod, BuildingName, TargetYear
    FROM              _area
    INNER JOIN        _bldg
    ON                _area.BuildingId=_bldg.BuildingId"""
    return duckdb.sql(q).df()


def get_project_eui_targets(
    area: AreaDataFrame,
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
    *,
    filter_year: bool = True,
) -> pd.DataFrame:
    """Return the project EUI targets. Doesn't do any area weighting.

    Filters the UKNZBC data to get only the targets relevant to the `areas` in project.

    ```python
    # noqa: D100
    # pytest-examples
    from netzero_metrics.calcs import (
        attach_target_year_to_area,
        get_test_data,
    )

    _area, _bldg, area, eui_custom = get_test_data()
    area = attach_target_year_to_area(_area, _bldg)
    print(area.TargetYear.to_list())  # noqa: T201
    #> [2025, 2025, 2030, 2030, 2030]
    ```
    """
    duckdb.register("area", area)
    duckdb.register("eui", eui)
    q = """
    SELECT DISTINCT  Year, BuildingType, ConstructionMethod, Target, TargetYear, BuildingName
    FROM (
        SELECT       *
        FROM         eui
        INNER JOIN   area
        ON           area.BuildingType=eui.BuildingType
        AND          area.ConstructionMethod=eui.ConstructionMethod);"""
    if filter_year:
        and_yr = """
        AND         area.TargetYear=eui.Year);"""
        q = q[:-2] + and_yr
    return duckdb.sql(q).df()


def get_eui_target( # TODO: get_area_weighted_eui_target
    area: AreaDataFrame,
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
    *,
    filter_year: bool = True,
) -> float:
    """Return the energy use target.

    When `filter_year` is True, the target is filtered by the year in the area DataFrame.
    """
    duckdb.register("area", area)
    duckdb.register("eui", eui)
    q = """
    SELECT      GrossInternalArea, Target
    FROM        area
    INNER JOIN  eui
    ON          area.ConstructionMethod=eui.ConstructionMethod
    AND         area.BuildingType=eui.BuildingType"""

    if filter_year:
        and_yr = """
        AND         area.TargetYear=eui.Year"""
        q = q + and_yr
    _df = duckdb.sql(q).df()
    p_trgt, p_area = _df.Target, _df.GrossInternalArea
    return calc_area_weighted_target(p_trgt, p_area)


def get_eui_targets(
    area: AreaDataFrame,
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
    *,
    filter_year: bool = True,
) -> dict[str, float]:
    """Return EUI targets for buildings and the project.

    When `filter_year` is True, the target is filtered by the year in the area DataFrame.
    """
    li_bldgs = list(area.BuildingName.unique())
    di_eui_targets = {}
    for bldg in li_bldgs:
        duckdb.register(
            "area",
            area,
        )  # Ensure the table is registered in each iteration
        _area = duckdb.execute("SELECT * FROM area WHERE BuildingName=?", (bldg,)).df()
        di_eui_targets[bldg] = get_eui_target(_area, eui, filter_year=filter_year)
    di_eui_targets["Project"] = get_eui_target(area, eui, filter_year=filter_year)
    return di_eui_targets


def get_building_yearly_eui_uknzcb_targets(
    area: AreaDataFrame,
    eui_uknzcb: EuiTargetUknzcbDataFrame,
) -> pd.DataFrame:
    """Return UK NZC targets for each year for a single building."""
    if len(area.BuildingName.unique()) > 1:
        msg = "Area DataFrame must contain only one building."
        raise ValueError(msg)
    duckdb.register("area", area)
    duckdb.register("eui_uknzcb", eui_uknzcb)
    building_name = area.BuildingName.unique()[0]
    q = """
    SELECT      GrossInternalArea, Target, Year
    FROM        area
    INNER JOIN  eui_uknzcb
    ON          area.ConstructionMethod=eui_uknzcb.ConstructionMethod
    AND         area.BuildingType=eui_uknzcb.BuildingType
    """
    df = duckdb.sql(q).df()
    p_trgt, p_area = df.Target, df.GrossInternalArea
    results = []
    for year, group in df.groupby("Year"):
        p_trgt, p_area = group.Target.to_numpy(), group.GrossInternalArea.to_numpy()
        weighted_target = calc_area_weighted_target(p_trgt, p_area)
        results.append(
            {
                "Year": year,
                "Target": weighted_target,
                "BuildingName": building_name,
            },
        )
    results = pd.DataFrame(results)
    results["TargetName"] = NZC_TARGET_NAME
    return results


def get_all_buildings_yearly_eui_uknzcb_targets(
    area: AreaDataFrame,
    eui_uknzcb: EuiTargetUknzcbDataFrame,
) -> pd.DataFrame:
    """Return UK NZC targets for each year for all buildings."""
    li_bldgs = list(area.BuildingName.unique())
    results = []
    for bldg in li_bldgs:
        duckdb.register("area", area)
        _area = duckdb.execute("SELECT * FROM area WHERE BuildingName=?", (bldg,)).df()
        results.append(get_building_yearly_eui_uknzcb_targets(_area, eui_uknzcb))
    return pd.concat(results, ignore_index=True)


def get_project_targets(
    area: AreaDataFrame,
    eui_uknzcb: EuiTargetUknzcbDataFrame,
    eui_custom: EuiTargetDataFrame,
) -> dict[str, dict[str, float]]:
    """Return EUI targets for buildings and the project."""
    di_eui_trgts = {}
    if not eui_custom.empty:
        li_targets = list(eui_custom.TargetName.unique())
        for trgt in li_targets:
            duckdb.register("eui_custom", eui_custom)
            di_eui_trgts[trgt] = duckdb.execute(
                "SELECT * FROM eui_custom WHERE TargetName=?",
                (trgt,),
            ).df()
    eui_uknzcb_project = get_project_eui_targets(
        area,
        eui_uknzcb,
        filter_year=True,
    )  # filter out targets from ref data relevant to project
    targets = {}
    targets[NZC_TARGET_NAME] = get_eui_targets(area, eui_uknzcb_project)
    for k, v in di_eui_trgts.items():
        targets[k] = get_eui_targets(area, v, filter_year=False)
    return targets


def get_khwr_per_m2_gia_only(
    eui_uknzcb: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
) -> EuiTargetUknzcbDataFrame | EuiTargetDataFrame:
    """Return only the GIA targets from the EUI data."""
    duckdb.register("eui_uknzcb", eui_uknzcb)
    return duckdb.sql("SELECT * FROM eui_uknzcb WHERE Unit='kWh/m²GIA/yr'").df()


def pivot_eui_data_for_construction_delivery_type(
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
    construction_delivery_type: str,
) -> pd.DataFrame:
    """Pivot the EUI data for a specific construction method."""
    duckdb.register("eui", eui)
    df = pd.pivot_table(
        duckdb.execute(
            "SELECT * FROM eui WHERE ConstructionMethod=?",
            (construction_delivery_type,),
        ).df(),
        index=["BuildingType"],
        columns=["Year"],
        values=["Target"],
    ).fillna(0)
    # TODO: use https://duckdb.org/docs/stable/clients/python/dbapi#prepared-statements
    df.columns = [x[1] for x in df.columns]
    return df.sort_values(by=df.columns[0])


def get_eui_uknzcb_targets_pivot(
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
) -> list[pd.DataFrame]:
    """Return the pivoted EUI data for each construction method."""
    return [
        pivot_eui_data_for_construction_delivery_type(eui, x)
        for x in eui.ConstructionMethod.unique()
    ]


# +
def get_area_summary(area: pd.DataFrame) -> pd.DataFrame:
    """Return the area summary for the project buildings."""
    return pd.pivot_table(
        area,
        index=["BuildingType", "ConstructionMethod"],
        columns=["BuildingName"],
        values=["GrossInternalArea"],
        aggfunc="sum",
    ).fillna(0)


def get_area_weights(df_area_summary: pd.DataFrame) -> dict:
    """Calculate the area weights of the project buildings for each area."""
    return {
        x: np.round(df_area_summary[x] / df_area_summary[x].sum(), 2).dropna().to_dict()
        for x in df_area_summary.columns
    }


def get_project_area_weights(df_area_summary: pd.DataFrame) -> dict:
    """Calculate the area weight for each project building."""
    return {
        k[1]: v
        for k, v in (df_area_summary.sum() / df_area_summary.sum().sum())
        .to_dict()
        .items()
    }


def get_df_targets(di_targets: dict[str, dict[str, float]]) -> pd.DataFrame:
    """Return the DataFrame of targets."""
    _ = pd.DataFrame(di_targets).T
    _.index.name = "TargetName"
    return _


# -
def get_area_and_target_summaries(
    df_project_buildings: pd.DataFrame,
    df_area: pd.DataFrame,
    df_project_energy_targets: pd.DataFrame,
    df_eui: pd.DataFrame = EUI_DATA,
) -> tuple:
    """Return area and target summaries."""
    df_eui = get_khwr_per_m2_gia_only(df_eui)  # TODO: remove non GIA from data
    df_area = attach_target_year_to_area(df_area, df_project_buildings)
    df_area_summary = get_area_summary(df_area)
    di_area_weights = get_area_weights(df_area_summary)
    di_project_area_weights = get_project_area_weights(df_area_summary)

    df_nzc_standard_building_year_targets = get_all_buildings_yearly_eui_uknzcb_targets(
        df_area,
        df_eui,
    )

    di_targets = get_project_targets(df_area, df_eui, df_project_energy_targets)
    df_targets = get_df_targets(di_targets)
    df_all_project_targets = df_targets[["Project"]].reset_index()
    df_all_project_targets.columns = ["TargetName", "ProjectTarget"]

    df_all_building_targets = df_targets.copy(deep=True)
    del df_all_building_targets["Project"]
    df_all_building_targets = pd.melt(
        df_all_building_targets.reset_index(),
        id_vars=["TargetName"],
        var_name="BuildingName",
        value_name="Target",
    )
    return (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    )
