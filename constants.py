import pathlib

# from aectemplater_client import get_object_by_code
# def get_object_id():
#     return get_object_by_code(code="MxfProjectBuildingArea")["id"]

PTH_EUI_IN = pathlib.Path("data/energy-use-intensity.xlsx")
PTH_EUI = pathlib.Path("data/energy-use-intensity.csv")
PTH_BUILDING_TYPES = pathlib.Path("data/building-types.txt")

OBJECT_ID_BUILDING_AREA = 835 # get_object_id()
TEST_PROJECT_REVISION_ID = 2