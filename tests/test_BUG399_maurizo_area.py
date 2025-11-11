import pandas as pd
from netzero_metrics.constants import nzdata
from constants import fdir_data_7763
from netzero_metrics.calcs import (
    get_area_and_target_summaries,
)


def test_7763():
    _area = pd.read_csv((fdir_data_7763 / "areas.csv"))
    _bldg = pd.read_csv((fdir_data_7763 / "bldgs.csv"))
    eui_custom = pd.DataFrame()
    eui_uknzcb = nzdata.energy_use_intensity

    (
        df_area_summary,
        di_area_weights,
        di_project_area_weights,
        df_nzc_standard_building_year_targets,
        df_all_building_targets,
        df_all_project_targets,
    ) = get_area_and_target_summaries(_bldg, _area, eui_custom, eui_uknzcb)

    assert df_all_project_targets is not None
    assert int(df_all_project_targets.set_index("TargetName").loc["UK NZC Standard","ProjectTarget" ]) == 292
