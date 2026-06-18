from dataclasses import dataclass
from enum import Enum
from pathlib import Path

PATH = Path(__file__).parent
STUDY_YEARS = (2008, 2024)
FIELD_BOUNDARY_SHAPEFILE = PATH / 'data' / 'plot_boundaries.shp'
FIELD_BOUNDING = [-93.75243, -93.74701, 41.91966, 41.9216]
GSSURGO_DATA_PATH = Path('/storage/group/kxa15/default/data/gSSURGO/')

@dataclass
class DatasetDataMixin:
    csv_path: Path
    date_column: str

class Dataset(DatasetDataMixin, Enum):
    PLANTING_ACTIVITIES = PATH / 'data' / 'dataset_planting_activities.csv', 'planting_date'
    CHEMICAL_INPUTS = PATH / 'data' / 'dataset_chemical_inputs.csv', 'application_date'
    HARVEST_ACTIVITIES = PATH / 'data' / 'dataset_harvest_activities.csv', 'activity_date'

@dataclass
class Treatment:
    treatment_filter: callable
    harvest_filter: callable
    description: str
    planting_management: dict[str, dict]
    harvest_management: dict[str, str]

TREATMENTS = {
    'CS': Treatment(
        # Corn-soybean rotation with annual grain removal (designated C2 in corn years, S2 in soybean years),
        # Both C2 and S2 were harvested annually for grain only and thus represent the traditional Midwest row crop
        # systems in the United States
        description='Corn-soybean rotation',
        treatment_filter=lambda x: ((x['treatment'] == 'C2') & ((x['study_year'] - STUDY_YEARS[0]) % 2 == 0)) | ((x['treatment'] == 'S2') & ((x['study_year'] - STUDY_YEARS[0]) % 2 == 1)),
        harvest_filter=lambda x: (x['crop'] == 'corn_grain') | (x['crop'] == 'soybean_grain'),
        planting_management={
            'corn': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 50,
                'residue_removed': 50,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
            'soybean': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 10,
                'residue_removed': 0,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'RETURN',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
        },
        harvest_management={
            'corn': 'Grain_Harvest',
            'soybean': 'Grain_Harvest',
        },
    ),
    'SC': Treatment(
        # Soybean-corn rotation with annual grain removal (designated C2 in corn years, S2 in soybean years),
        # Both C2 and S2 were harvested annually for grain only and thus represent the traditional Midwest row crop
        # systems in the United States
        description='Soybean-corn rotation',
        treatment_filter=lambda x: ((x['treatment'] == 'S2') & ((x['study_year'] - STUDY_YEARS[0]) % 2 == 0)) | ((x['treatment'] == 'C2') & ((x['study_year'] - STUDY_YEARS[0]) % 2 == 1)),
        harvest_filter=lambda x: (x['crop'] == 'corn_grain') | (x['crop'] == 'soybean_grain'),
        planting_management={
            'corn': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 50,
                'residue_removed': 50,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
            'soybean': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 10,
                'residue_removed': 0,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'RETURN',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
        },
        harvest_management={
            'corn': 'Grain_Harvest',
            'soybean': 'Grain_Harvest',
        },
    ),
    'CC': Treatment(
        # Corn with annual grain and stover removal (CC)
        # CC and CCW were harvested annually for grain plus approximately 50% of dry-weight-based stover
        description='Continuous corn with stover removed',
        treatment_filter=lambda x: x['treatment'] == 'CC',
        harvest_filter=lambda x: (x['crop'] == 'corn_grain'),
        planting_management={
            'corn': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 50,
                'residue_removed': 50,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
        },
        harvest_management={
            'corn': 'Grain_Harvest',
        },
    ),
    'CCW': Treatment(
        # Continuous corn with grain and stover removal and rye (Secale cereale L.) used as a winter cover crop (CCW)
        # CC and CCW were harvested annually for grain plus approximately 50% of dry-weight-based stover
        description='Continuous corn with cover crop and stover removed',
        treatment_filter=lambda x: x['treatment'] == 'CCW',
        harvest_filter=lambda x: (x['crop'] == 'corn_grain') | (x['crop'] == 'rye'),
        planting_management={
            'corn': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 50,
                'residue_removed': 50,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
            'rye': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 40,
                'residue_removed': 0,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'RETURN',
                'harvest_timing': -999,
                'kill_after_harvest': 1,
            },
        },
        harvest_management={
            'corn': 'Grain_Harvest',
            'rye': 'Kill_Crop',
        },
    ),
    'P': Treatment(
        # Reconstructed multispecies tallgrass prairie with annual aboveground biomass removal (P)
        # The aboveground biomass of P and PF were harvested annually after a killing frost (~75% biomass removal)
        # The seed mix contained 31 species, including C3 and C4 grasses and leguminous and non-leguminous forbs. All
        # species were perennial and were sourced from within 240 km of Boone County, IA. The composition of the seed
        # mix by weight was 12% C3 grasses, 56% C4 grasses, 8% legumes, and 24% forbs.

        description='Prairie with no fertilizer application',
        treatment_filter=lambda x: x['treatment'] == 'P',
        harvest_filter=lambda x: (x['activity'] == 'mow'),
        planting_management={
            'prairie': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 30,
                'residue_removed': 75,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 0,
            },
        },
        harvest_management={
            'prairie': 'Forage_Harvest',
        },
    ),
    'PF': Treatment(
        # N-fertilized reconstructed multispecies tallgrass prairie with annual aboveground biomass removal (PF)
        # The aboveground biomass of P and PF were harvested annually after a killing frost (~75% biomass removal)
        # The seed mix contained 31 species, including C3 and C4 grasses and leguminous and non-leguminous forbs. All
        # species were perennial and were sourced from within 240 km of Boone County, IA. The composition of the seed
        # mix by weight was 12% C3 grasses, 56% C4 grasses, 8% legumes, and 24% forbs.
        description='Prairie with fertilizer application',
        treatment_filter=lambda x: x['treatment'] == 'PF',
        harvest_filter=lambda x: (x['activity'] == 'mow'),
        planting_management={
            'prairie': {
                'clipping_start': -999,
                'clipping_end': -999,
                'maximum_soil_coverage': 100,
                'standing_residue_at_harvest': 30,
                'residue_removed': 75,
                'clipping_biomass_threshold_lower': 0.5,
                'clipping_biomass_threshold_upper': 999,
                'clipping_biomass_destiny': 'REMOVE',
                'harvest_timing': -999,
                'kill_after_harvest': 0,
            },
        },
        harvest_management={
            'prairie': 'Forage_Harvest',
        },
    ),
}
