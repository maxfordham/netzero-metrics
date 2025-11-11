""""Plotting functions for netzero-metrics package."""
import altair as alt
import pandas as pd
from netzero_metrics.constants import nzdata
from palettable.cartocolors.qualitative import Prism_10

from netzero_metrics.constants import EUI_DATA, NZC_TARGET_NAME
from netzero_metrics.models import (
    BuildingTargetDataFrame,
    EuiTargetDataFrame,
    ProjectTargetDataFrame,
)

# -

color_energy_end_use = nzdata.color_energy_end_use


def plot_energy_consumption(
    df: pd.DataFrame,
    x_name: str = "ReportingPeriod",
    direction: str = "vertical",
):
    if direction == "horizontal":
        x = alt.X(
            "sum(EnergyConsumption)",
            title="Total Energy Consumption (kWhr/m2/yr)",
        )
        y = alt.Y(x_name, title=None)
    elif direction == "vertical":
        y = alt.X(
            "sum(EnergyConsumption)",
            title="Total Energy Consumption (kWhr/m2/yr)",
        )
        x = alt.Y(x_name, title=None)
    else:
        msg = f"{direction} not supported."
        raise ValueError(msg)
    unique_energy_end_use = (
        df["EnergyEndUse"].unique().tolist() if "EnergyEndUse" in df.columns else []
    )
    color_scale = alt.Scale(
        domain=unique_energy_end_use,
        range=[
            v["Color"]
            for v in color_energy_end_use
            if v["EnergyEndUse"] in unique_energy_end_use
        ],
    )
    return (
        alt.Chart(df)
        .mark_bar()
        .encode(
            x=x,
            y=y,
            color=alt.Color(
                "EnergyEndUse",
                scale=color_scale,
                legend=alt.Legend(title=None, orient="top", direction="vertical"),
            ),
        )
    )


# EUI
def get_order(df):
    order = df[df.Year == 2050]
    order = order[order["Unit"] == "kWh/m²GIA/yr"]
    order = order[order["ConstructionMethod"] == "newbuild"]
    order = order.sort_values("Target", ascending=False)["BuildingType"].to_list()
    a, b, c = [f"{i} - RETROFIT-STEPPED" for i in order], [f"{i} - RETROFIT-IN-ONE-GO" for i in order], [f"{i} - NEWBUILD" for i in order]
    return [j for i in zip(a, b, c) for j in i]


def plot_eui(df: pd.DataFrame = EUI_DATA) -> alt.Chart:
    """Plot energy use intensity data. Defaults to reference data from UKNZCB standard."""
    order = get_order(df)
    data = df[df.Unit == "kWh/m²GIA/yr"]
    data.loc[:, "BuildingType"] = (
        data["BuildingType"] + " - " + data["ConstructionMethod"].str.upper()
    )

    return (
        alt.Chart(data)
        .mark_circle()
        .encode(
            y=alt.Y(
                "BuildingType",
                title=None,
                axis=alt.Axis(titleAlign="left", labelLimit=400, labelAlign="right"),
            ).sort(order),
            x=alt.Y("Target", title="Target (KWHr / m2(GIA) / yr)"),
            color=alt.Color("Year").scale(scheme="redblue"),
        )
        .properties(
            height=900,
            title=alt.Title(
                "UKNZCB Energy Use Intensity (EUI) Targets",
                subtitle=[
                    "EUI Target in KWHr / m2(GIA) / yr (x-axis)",
                    "for retrofit-stepped, retrofit-in-one-go and newbuild buildings categorised by building type (y-axis)",
                    "with targets indicated by year, between now and 2050 (color)",
                ],
            ),
        )
    )


if __name__ == "__main__":
    plot_eui()


def plot_building_targets(
    df_nzc_standard_building_year_targets: EuiTargetDataFrame,
    df_all_building_targets: BuildingTargetDataFrame,
    df_all_project_targets: ProjectTargetDataFrame,
) -> alt.Chart:
    """Plot the building and project targets.

    This will plot the UK NZC standard targets and any custom targets defined by the user.
    """
    df_all_building_targets["Name"] = df_all_building_targets.BuildingName.astype(str)
    df_nzc_standard_building_year_targets["Name"] = (
        df_nzc_standard_building_year_targets.BuildingName.astype(str)
    )

    x = alt.X("Target", title="Target (kWh/m²/yr)")
    y = alt.Y("Name", title="Building Name")
    nzc_target_name = NZC_TARGET_NAME

    domain = df_all_building_targets["TargetName"].unique().tolist()
    domain = [nzc_target_name] + [
        target for target in domain if target != nzc_target_name
    ]
    nzc_standard_color = Prism_10.hex_colors[4]
    color_range = [nzc_standard_color] + [
        color for color in Prism_10.hex_colors if color != nzc_standard_color
    ]
    # Plot the NZC standard year targets for each building within the project
    if df_nzc_standard_building_year_targets.empty:
        nzc_standard_building_year_targets_chart = alt.Chart(
            pd.DataFrame(),
        ).mark_circle(size=60)
    else:
        df_nzc_standard_building_year_targets["Target"] = (
            df_nzc_standard_building_year_targets["Target"].round(1)
        )
        nzc_standard_building_year_targets_chart = (
            alt.Chart(
                df_nzc_standard_building_year_targets,
                title=alt.Title(
                    "Project Area-Weighted Energy Use Intensity Targets",
                ),
            )
            .mark_circle(size=60)
            .encode(
                x=x,
                y=y,
                color=alt.Color("Year", legend=alt.Legend(format=".0f")).scale(
                    scheme="redblue",
                ),
            )
        )
    chart = nzc_standard_building_year_targets_chart
    if not df_all_building_targets.empty:
        # Plot building targets for every project-defined target type
        df_all_building_targets["Target"] = df_all_building_targets["Target"].round(1)
        ticks_targets = (
            alt.Chart(df_all_building_targets)
            .mark_tick(tooltip=True, opacity=1, thickness=2)
            .encode(
                y=y,
                x="Target:Q",
                color=alt.Color(
                    "TargetName:N",
                    title="Target Name",
                    legend=None,
                    scale=alt.Scale(domain=domain, range=color_range),
                ),
            )
        )
        chart += ticks_targets
    if not df_all_project_targets.empty:
        # Plot project targets for every project-defined target type
        df_all_project_targets["ProjectTarget"] = df_all_project_targets[
            "ProjectTarget"
        ].round(1)
        rules_targets = (
            alt.Chart(pd.DataFrame(df_all_project_targets))
            .mark_rule(tooltip=True, opacity=1, strokeWidth=2)
            .encode(
                x="ProjectTarget:Q",
                color=alt.Color(
                    "TargetName:N",
                    title="Target Name",
                    scale=alt.Scale(domain=domain, range=color_range),
                ),
            )
        )
        chart += rules_targets
    return chart
