import pandas as pd
import pytest
from netzero_metrics.constants import nzdata
from constants import fdir_data, fdir_output
from netzero_metrics.calcs import (
    get_area_and_target_summaries,
)
from netzero_metrics.plots import (
    plot_building_targets,
    plot_energy_consumption,
    plot_eui,
)

_energy_consumption = pd.read_csv(fdir_data / "energy-consumption.csv")


@pytest.fixture
def test_data():
    _area = pd.read_csv(fdir_data / "areas.csv")
    _bldg = pd.read_csv(fdir_data / "bldgs.csv")
    eui_uknzcb = nzdata.energy_use_intensity
    eui_custom = pd.read_csv(fdir_data / "eui-custom.csv")
    return _area, _bldg, eui_uknzcb, eui_custom


def test_plot_building_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    ) = get_area_and_target_summaries(_bldg, _area, eui_custom, eui_uknzcb)
    ch = plot_building_targets(
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    )
    fpth_plot = fdir_output / "test_plot_building_targets.png"
    fpth_plot.unlink(missing_ok=True)
    ch.save(fpth_plot)
    assert fpth_plot.is_file()


def test_plot_energy_consumption():
    _energy_consumption = pd.read_csv(fdir_data / "energy-consumption.csv")
    plot = plot_energy_consumption(_energy_consumption)
    fpth_plot = fdir_output / "test_plot_energy_consumption.png"
    fpth_plot.unlink(missing_ok=True)
    plot.save(fpth_plot)
    assert fpth_plot.is_file()


def test_plot_eui():
    eui_uknzcb = nzdata.energy_use_intensity
    ch = plot_eui(eui_uknzcb)
    fpth_plot = fdir_output / "test_plot_eui.png"
    fpth_plot.unlink(missing_ok=True)
    ch.save(fpth_plot)
    assert fpth_plot.is_file()
