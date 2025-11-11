import pathlib

import pandas as pd
import pytest
from netzero_metrics.constants import nzdata
from great_tables import GT
from netzero_metrics.calcs import (
    attach_target_year_to_area,
    get_area_and_target_summaries,
)
from netzero_metrics.tables import (
    plot_great_tables_area_summary,
    plot_great_tables_targets,
)

fdir = pathlib.Path(__file__).parent
fdir_data = fdir / "data"
fdir_output = fdir / "outputs"


@pytest.fixture
def test_data():
    _area = pd.read_csv(fdir_data / "areas.csv")
    _bldg = pd.read_csv(fdir_data / "bldgs.csv")
    eui_uknzcb = nzdata.energy_use_intensity
    eui_custom = pd.read_csv(fdir_data / "eui-custom.csv")
    return _area, _bldg, eui_uknzcb, eui_custom


def test_plot_great_tables_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    ) = get_area_and_target_summaries(_bldg, _area, eui_custom, eui_uknzcb)
    ch = plot_great_tables_targets(
        df_all_building_targets,
        df_all_project_targets,
    )
    assert isinstance(ch, GT)


def test_plot_great_tables_area_summary(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    area = attach_target_year_to_area(_area, _bldg)
    ch = plot_great_tables_area_summary(
        area,
    )
    assert isinstance(ch, GT)
