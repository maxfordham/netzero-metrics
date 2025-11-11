import pandas as pd
import pytest
from netzero_metrics.constants import nzdata
from constants import fdir_data
from netzero_metrics.calcs import (
    attach_target_year_to_area,
    get_all_buildings_yearly_eui_uknzcb_targets,
    get_area_and_target_summaries,
    get_df_targets,
    get_project_eui_targets,
    get_project_targets,
)
from pytest_examples import CodeExample, EvalExample, find_examples


@pytest.mark.parametrize('example', find_examples('src/netzero_metrics/calcs.py'), ids=str)
def test_examples(example: CodeExample, eval_example: EvalExample):
    eval_example.set_config(line_length=50)
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(example)
    else:
        # eval_example.lint(example)
        eval_example.run_print_check(example)

@pytest.fixture
def test_data():
    _area = pd.read_csv(fdir_data / "areas.csv")
    _bldg = pd.read_csv(fdir_data / "bldgs.csv")
    eui_uknzcb = nzdata.energy_use_intensity
    eui_custom = pd.read_csv(fdir_data / "eui-custom.csv")
    return _area, _bldg, eui_uknzcb, eui_custom


def test_attach_target_year_to_area(test_data: tuple):
    _area, _bldg, _, _ = test_data
    area = attach_target_year_to_area(_area, _bldg)
    assert isinstance(area, pd.DataFrame)
    assert len(area) > 1
    assert "TargetYear" in area.columns



def test_get_project_eui_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    area = attach_target_year_to_area(_area, _bldg)
    targets = get_project_eui_targets(area, eui_uknzcb)


    li = targets.set_index(["Year", "BuildingType", "ConstructionMethod", "BuildingName"]).index.to_list()
    li = ["|".join([str(_) for _ in list(x)]) for x in li]
    assert len(li) == len(set(li)), "Duplicate entries found in targets DataFrame"


def test_get_project_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    area = attach_target_year_to_area(_area, _bldg)
    targets = get_project_targets(area, eui_uknzcb, eui_custom)

    assert isinstance(targets, dict)
    assert targets["UK NZC Standard"]
    assert targets["ambitious!"]["Block A"].round(1) == 70.0
    assert targets["ambitious!"]["Block B"].round(1) == 70.0
    assert targets["ambitious!"]["Project"].round(1) == 70.0


def test_get_df_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    area = attach_target_year_to_area(_area, _bldg)
    targets = get_project_targets(area, eui_uknzcb, eui_custom)
    df_targets = get_df_targets(targets)
    assert isinstance(df_targets, pd.DataFrame)


def test_get_yearly_eui_targets(test_data: tuple):
    _area, _bldg, eui_uknzcb, _ = test_data
    area = attach_target_year_to_area(_area, _bldg)
    yrly_targets = get_all_buildings_yearly_eui_uknzcb_targets(area, eui_uknzcb)
    assert "Block A" in yrly_targets.BuildingName.unique()
    assert "Block B" in yrly_targets.BuildingName.unique()
    assert len(yrly_targets) == len(yrly_targets.BuildingName.unique()) * len(
        yrly_targets.Year.unique()
    )
    # Check that Target is in descending order as Year increases for each BuildingName
    for building in yrly_targets.BuildingName.unique():
        building_data = yrly_targets[yrly_targets.BuildingName == building]
        assert all(
            building_data.sort_values("Year")["Target"].diff().dropna() <= 0,
        ), f"Targets are not in descending order for {building}"


def test_get_area_and_target_summaries(test_data: tuple):
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    ) = get_area_and_target_summaries(_bldg, _area, eui_custom, eui_uknzcb)
    assert isinstance(df_area_summary, pd.DataFrame)


def test_get_area_and_target_summaries_no_eui_custom(test_data: tuple):
    """Test getting area and target summaries without eui_custom."""
    _area, _bldg, eui_uknzcb, eui_custom = test_data
    eui_custom = pd.DataFrame()
    (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    ) = get_area_and_target_summaries(_bldg, _area, eui_custom, eui_uknzcb)
    assert isinstance(df_area_summary, pd.DataFrame)
