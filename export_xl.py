import pathlib
import xlsxdatagrid as xdg
from constants import OBJECT_ID_BUILDING_AREA, TEST_PROJECT_REVISION_ID
from aectemplater_client import get_instance_specs_object_data_grid, get_type_spec_object_data_grid
from jsonref import replace_refs
base_url = "https://aectemplater.maxfordham.com"
def get_instance(project_revision_id, object_id, is_transposed=False):
    _ = get_instance_specs_object_data_grid(project_revision_id, object_id)
    data, schema = _["data"], _["$schema"]
    schema = replace_refs(schema)
    datamodel_url = base_url + f"object/{object_id}/gridschema"
    schema["datagrid_index_name"] = ["section", "unit", "name"]
    schema["is_transposed"] = is_transposed
    # schema["project_number"] = project_number
    schema["template_id"] = object_id
    schema["datamodel_url"] = datamodel_url
    schema["title"] = "Project Building Areas"
    schema["items"]["properties"] = {k:v for k,v in schema["items"]["properties"].items() if k not in ["Id", "TypeSpecId"]}
    return data, schema

def get_type(project_revision_id, object_id, is_transposed=False):
    _ = get_type_spec_object_data_grid(project_revision_id, object_id)
    data, schema = _["data"], _["$schema"]
    schema = replace_refs(schema)
    datamodel_url = base_url + f"object/{object_id}/gridschema"
    schema["datagrid_index_name"] = ["section", "unit", "name"]
    
    schema["is_transposed"] = is_transposed
    # schema["project_number"] = project_number
    schema["template_id"] = object_id
    schema["datamodel_url"] = datamodel_url
    schema["title"] = "Project Buildings"
    schema["items"]["properties"] = {k:v for k,v in schema["items"]["properties"].items() if k not in ["Id"]}
    return data, schema

def download_excel(project_revision_id, object_id):
    base_url = "https://aectemplater.maxfordham.com"
    
    
    data_i, schema_i = get_instance(project_revision_id, object_id)
    data_t, schema_t = get_type(project_revision_id, object_id)

    # dropids = lambda data, li: [{k:v for k, v in x.items() if k not in li} for x in data]
    # data_i, data_t = dropids(data_i, ["Id", "InstanceSpecId"]), dropids(data_t, ["Id", "TypeSpecId"])
    
    fpth = pathlib.Path(f"{project_revision_id}-{object_id}.xlsx")
    fpth = xdg.from_jsons([data_t, data_i], [schema_t, schema_i], fpth=fpth)
    return fpth

if __name__ == "__main__":
    project_revision_id, object_id =  TEST_PROJECT_REVISION_ID, OBJECT_ID_BUILDING_AREA
    fpth = download_excel(project_revision_id, object_id)
    print(fpth)