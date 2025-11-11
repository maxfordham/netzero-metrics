
"""render reference data tables for netzero-metrics package."""

from __future__ import annotations

import base64
import pathlib
from io import BytesIO
from typing import TYPE_CHECKING

import ipywidgets as w
import pandas as pd
import polars as pl
from bqplot import ColorScale
from great_tables import GT
from ipyautoui.custom.filedownload import FileDownload
from ipydatagrid import BarRenderer, DataGrid

from netzero_metrics.calcs import get_eui_uknzcb_targets_pivot
from netzero_metrics.constants import EUI_DATA

if TYPE_CHECKING:
    from netzero_metrics.models import (
        EuiTargetDataFrame,
        EuiTargetUknzcbDataFrame,
    )


def plot_great_tables_targets(
    df_all_building_targets: pd.DataFrame,
    df_all_project_targets: pd.DataFrame,
) -> GT:
    """Plot great table of project building targets and the project target."""
    if not df_all_building_targets.empty:
        df_all_project_targets = df_all_project_targets.rename(
            {"ProjectTarget": "Target"},
            axis=1,
        )
        df_all_building_targets = df_all_building_targets.rename(
            {"BuildingName": "Name"},
            axis=1,
        )
        df_all_project_targets["Name"] = "Project"
        df_targets = pd.concat([df_all_building_targets, df_all_project_targets])
        df_targets["Target"] = df_targets["Target"].round(1)
        # Create a custom sort order column to ensure "UK NZC Standard" comes first and then by TargetName
        df_targets["sort_order"] = df_targets["TargetName"].apply(
            lambda x: 0 if x == "UK NZC Standard" else 1
        )
        df_targets = df_targets.sort_values(by=["sort_order", "TargetName"]).drop(
            columns=["sort_order"]
        )
        pl_df_targets = pl.from_pandas(df_targets)
        pivot = pl_df_targets.pivot(
            values="Target",
            index=["TargetName"],
            on="Name",
        ).with_columns(pl.col("*").fill_null(0))
        target_sum = max(df_targets["Target"])
        return (
            GT(pivot)
            .tab_header(
                title="Project Building Targets",
                subtitle="Summary of Project Building Targets",
            )
            .data_color(
                domain=[0, target_sum], palette=["white", "lightblue"], na_color="white"
            )
            .tab_spanner(
                label="Target (kWh/m²/yr) ", columns=[*sorted(set(df_targets["Name"]))]
            )
            .cols_label(
                TargetName="Target Name",
            )
        )
    return GT(pd.DataFrame())


def plot_great_tables_area_summary(df_area: pd.DataFrame) -> GT:
    """Plot great table of project building area summary."""
    if not df_area.empty:
        # Check for empty cells in BuildingName and replace them with BuildingId
        df_area["BuildingName"] = df_area.apply(
            lambda row: (
                row["BuildingId"]
                if pd.isnull(row["BuildingName"])
                else row["BuildingName"]
            ),
            axis=1,
        )
        pl_df_area = pl.from_pandas(df_area)
        pivot = (
            pl_df_area.pivot(
                values="GrossInternalArea",
                index=["BuildingType", "ConstructionMethod"],
                on="BuildingName",
                aggregate_function="sum",
            )
            .with_columns(
                pl.col("*").fill_null(0)
            )  # Replace null values with an empty string
            .sort("BuildingType")  # Sort by BuildingType
        )
        # Calculate row totals
        row_totals = (
            pivot.select(pl.exclude(["BuildingType", "ConstructionMethod"]))
            .sum_horizontal()
            .alias("Total")
        )
        pivot = pivot.with_columns(row_totals)

        # Calculate column totals
        column_totals = pivot.sum()
        column_totals = column_totals.with_columns(
            pl.lit("Total").alias("BuildingType"),
            pl.lit("").alias("ConstructionMethod"),
        )
        pivot = pivot.vstack(column_totals)
        area_sum = sum(df_area["GrossInternalArea"])
        return (
            GT(pivot)
            .tab_header(
                title="Project Building Areas",
                subtitle="Summary of Project Buildings Building Use Type and Construction Method",
            )
            .data_color(
                domain=[0, area_sum], palette=["white", "lightblue"], na_color="white"
            )
            .tab_spanner(
                label="GIA (m²) ",
                columns=[*sorted(set(df_area["BuildingName"])), "Total"],
            )
            .tab_spanner(
                label="Categorisation",
                columns=["BuildingType", "ConstructionMethod"],
            )
            .cols_move_to_start(
                columns=[
                    "BuildingType",
                    "ConstructionMethod",
                ]
            )
            .cols_label(
                BuildingType="Building Type",
                ConstructionMethod="Construction Method",
            )
        )
    return GT(pd.DataFrame())


def render_eui_construction_delivery_type_pivot(
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame,
) -> DataGrid:
    """Return DataGrid for the EUI data."""
    renderers = {
        x: BarRenderer(
            background_color=ColorScale(
                min=0,
                max=eui.iloc[:, 0].max(),
                scale_type="linear",
                scheme="GnYlRd",
                reverse=True,
            ),
        )
        for x in eui.columns
    }
    return DataGrid(
        eui,
        renderers=renderers,
        layout=w.Layout(height="750px"),
        column_widths={"BuildingType": 300},
    )


def render_eui_uknzcb_targets_pivot(
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame | None=None,
) -> w.Tab:
    """Return tabs of grids showing EUI data for each construction method."""
    if eui is None:
        eui = EUI_DATA
    titles = list(eui.ConstructionMethod.unique())
    grids = [
        render_eui_construction_delivery_type_pivot(df)
        for df in get_eui_uknzcb_targets_pivot(eui)
    ]
    return w.Tab(grids, titles=titles)


def dump_tab_datagrids_to_excel(tab: w.Tab) -> BytesIO:
    """Dump the tab DataGrids to an Excel file in memory."""
    # Create a BytesIO buffer to save the Excel file in memory
    excel_buffer = BytesIO()

    # Use pd.ExcelWriter to write to the in-memory buffer
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        for child in tab.children:
            if not isinstance(child, DataGrid):
                msg = f"Expected child to be DataGrid, got {type(child)}"
                raise TypeError(msg)
            sheet_name = tab.titles[tab.children.index(child)]
            child.data.to_excel(writer, sheet_name=sheet_name, index=True)

    # Seek to the beginning of the BytesIO buffer to prepare for download
    excel_buffer.seek(0)
    return base64.b64encode(excel_buffer.read()).decode("utf-8")


def render_eui_uknzcb_targets_pivot_with_file_download(
    eui: EuiTargetUknzcbDataFrame | EuiTargetDataFrame | None= None,
) -> w.VBox:
    """Return tabs of grids showing EUI data for each construction method with a file download button."""
    if eui is None:
        eui = EUI_DATA
    tab_eui = render_eui_uknzcb_targets_pivot(eui)
    file_download = FileDownload(
        content_b64=dump_tab_datagrids_to_excel(tab_eui),
        value=pathlib.Path("eui-data.xlsx"),
    )
    file_download.bn_download.disabled = False  # TODO: Remove once https://github.com/maxfordham/ipyautoui/issues/365 resolved
    file_download.bn_download.description = "Download EUI Data"
    file_download.bn_download.layout.width = "155px"
    return w.VBox(
        [
            file_download,
            tab_eui,
        ],
    )
