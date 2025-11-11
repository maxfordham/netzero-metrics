import pandas as pd
from netzero_metrics_reference_data import load_datapackage

NZC_TARGET_NAME = "UK NZC Standard"


class DataLoader:
    def __init__(self, pkg=None):
        if pkg is None:
            pkg = load_datapackage()
        self.pkg = pkg

    @property
    def building_types(self) -> list:
        return self.pkg.get_resource("building-types").read_text().split("\n")

    @property
    def energy_use_intensity(self) -> pd.DataFrame:
        return self.pkg.get_resource("energy-use-intensity").to_pandas()

    @property
    def energy_use_intensity_metadata(self) -> dict:
        return self.pkg.get_resource("energy-use-intensity").to_dict()

    @property
    def life_cycle_module(self) -> pd.DataFrame:
        return self.pkg.get_resource("life-cycle-modules").to_pandas()

    @property
    def rics_building_element_category(self) -> pd.DataFrame:
        return self.pkg.get_resource("rics-building-element-category").to_pandas()

    @property
    def color_energy_end_use(self) -> list:
        return self.pkg.get_resource("color-energy-end-use").read_rows()


nzdata = DataLoader()
EUI_DATA = nzdata.energy_use_intensity
