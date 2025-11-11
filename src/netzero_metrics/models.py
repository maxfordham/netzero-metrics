"""pydantic data models for netzero-metrics package."""
import pandera.pandas as pa
from pandera.engines.pandas_engine import PydanticModel
from pydantic import BaseModel, Field


class ProjectBuilding(BaseModel):
    """Definition of a columns required for a dataframe of project buildings."""

    BuildingId: str = Field(..., description="Unique identifier for the building, e.g. 'BLDG1'.")
    BuildingName: str = Field(..., description="Descriptive name for the building, e.g. 'Block A'.")
    TargetYear: int = Field(..., description="Target year for the building, e.g. 2030.")


class Area(BaseModel):
    """Definition of a columns required for a dataframe of building use-type areas and target completion year."""

    # AreaId ?
    BuildingId: str = Field(..., description="Unique identifier for the building, e.g. 'BLDG1'.")
    BuildingName: str = Field(..., description="Descriptive name for the building, e.g. 'Block A'.")
    GrossInternalArea: float = Field(..., description="Unique identifier for the building, e.g. 'Block A'.")
    BuildingType: str  # add enum
    ConstructionMethod: str  # add enum
    TargetYear: int  # add enum


class AreaDataFrame(pa.DataFrameModel):
    class Config:
        dtype = PydanticModel(Area)
        coerce = True  # this is required, otherwise a SchemaInitError is raised


class _Target(BaseModel):
    Target: float
    TargetName: str


class BuildingTarget(_Target):
    Name: str


class ProjectTarget(_Target):
    pass


class BuildingTargetDataFrame(pa.DataFrameModel):
    """definition of a pandas dataframe of UKNZCB energy use intensities. Columns defined by `EuiTargetUknzcb` model."""

    class Config:
        dtype = PydanticModel(BuildingTarget)
        coerce = True  # this is required, otherwise a SchemaInitError is raised


class ProjectTargetDataFrame(pa.DataFrameModel):
    """definition of a pandas dataframe of UKNZCB energy use intensities. Columns defined by `EuiTargetUknzcb` model."""

    class Config:
        dtype = PydanticModel(ProjectTarget)
        coerce = True  # this is required, otherwise a SchemaInitError is raised


class EuiTarget(_Target):
    """data model for custom energy use intensities. For simplicity ignore the year column."""

    BuildingName: str
    ConstructionMethod: str


class EuiTargetUknzcb(EuiTarget):
    """data model for UKNZCB energy use intensities."""

    Year: int


class EuiTargetUknzcbDataFrame(pa.DataFrameModel):
    """definition of a pandas dataframe of UKNZCB energy use intensities. Columns defined by `EuiTargetUknzcb` model."""

    class Config:
        dtype = PydanticModel(EuiTargetUknzcb)
        coerce = True  # this is required, otherwise a SchemaInitError is raised


class EuiTargetDataFrame(pa.DataFrameModel):
    """definition of a pandas dataframe of custom target project energy use intensities. Columns defined by `EuiTarget` model."""

    class Config:
        dtype = PydanticModel(EuiTarget)
        coerce = True  # this is required, otherwise a SchemaInitError is raised
