from dataset.operation import TransformNormalize, Preprocessing
from dataset.transform import Transform, TransformEnum
from dataset.normalize import Normalize, NormalizeEnum
from dataset.valid.row import RowValid, RowValidEnum


def doRun(save_file: str, name_file: str, actions: list[TransformNormalize], remove_rows: list[RowValid]):
    preprocessing = Preprocessing(
        name_file=name_file,
        save_file=save_file,
        actions=actions,
        remove_rows=remove_rows,
    )
    preprocessing.validate_rows()
    preprocessing.transform()
    preprocessing.normalize()
    preprocessing.save(is_index=False, is_save_origin=True)


if __name__ == "__main__":
    remove_rows = [
        RowValid(
            column="GRAIN_YIELD:(t/ha):avg",
            valid=RowValidEnum.VALUE_OR_REMOVE
        ),
        RowValid(
            column="SOWING_DATE:(date)",
            valid=RowValidEnum.VALUE_OR_REMOVE
        ),
        RowValid(
            column="HARVEST_STARTING_DATE:(date)",
            valid=RowValidEnum.VALUE_OR_REMOVE
        ),
        RowValid(
            column="GPS Latitude (N or S):(TEXT)",
            valid=RowValidEnum.VALUE_OR_REMOVE
        ),
        RowValid(
            column="GPS Longitude ( E or W):(TEXT)",
            valid=RowValidEnum.VALUE_OR_REMOVE
        ),
    ]

    # actions = [
    #     TransformNormalize(
    #         column="GRAIN_YIELD:(t/ha):avg",
    #         transform=Transform(transformEnum=TransformEnum.PASS),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE),
    #     ),
    #     TransformNormalize(
    #         column='SOWING_DATE:(date)',
    #         transform=Transform(transformEnum=TransformEnum.FORCE_ONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
    #     ),
    #     TransformNormalize(
    #         column='AREA_HARVESTED_BED_PLOT_M2:(m2)',
    #         transform=Transform(transformEnum=TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE),
    #     ),
    #     TransformNormalize(
    #         column='AREA_SOWN_BED_PLOT_M2:(m2)',
    #         transform=Transform(TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='BIRD_DAMAGE:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='EMERGENCE:(E/N/L)',
    #         transform=Transform(TransformEnum.STR_NORMAL),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='HARVEST_STARTING_DATE:(date)',
    #         transform=Transform(TransformEnum.DATE_FROM,
    #                             column_base="SOWING_DATE:(date)"),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
    #     ),
    #     TransformNormalize(
    #         column='EMERGENCE_DATE:(date)',
    #         transform=Transform(TransformEnum.DATE_FROM,
    #                             column_base="SOWING_DATE:(date)"),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
    #     ),
    #     TransformNormalize(
    #         column='FERTILIZER_%K2O_1:(%)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='FERTILIZER_%N_1:(%)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='FERTILIZER_%P2O5_1:(%)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='FERTILIZER_1:(date)',
    #         transform=Transform(TransformEnum.DATE_FROM,
    #                             column_base="SOWING_DATE:(date)"),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
    #     ),
    #     TransformNormalize(
    #         column='FOLIAR_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='FROST_DAMAGE_SPIKE:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='HAIL_DAMAGE:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='HERBICIDE_DAMAGE:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='HERBICIDE:(Y/N)',
    #         transform=Transform(TransformEnum.STR_NO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='IRRIGATED:(Y/N)',
    #         transform=Transform(TransformEnum.STR_NO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='INSECT_DAMAGE:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='LODGING:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='NO_OF_ROWS_HARVESTED:(integer)',
    #         transform=Transform(TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='NO_OF_ROWS_SOWN:(integer)',
    #         transform=Transform(TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='NUMBER_POST_SOWING_IRRIGATIONS:(integer)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='NUMBER_PRE_SOWING_IRRIGATIONS:(integer)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_MONTH_OF_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_1ST_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_2ND_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_3RD_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_4TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_5TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_6TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_7TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_8TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_9TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_10TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PPN_11TH_MO_BEFORE_HARVESTED:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PRE_SOWING_IRRIGATION:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PRECIPITATION_FROM_SOWING_TO_MATURITY:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='ROOT_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='SOIL_ALUMINIUM_TOXICITY:(Y/N)',
    #         transform=Transform(TransformEnum.STR_NO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SPIKE_DISEASE_DEVELOPMENT:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='TOTAL_PRECIPIT_IN_12_MONTHS:(mm)',
    #         transform=Transform(TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='WEED_PROBLEM:(N/T/S/M/V)',
    #         transform=Transform(TransformEnum.STR_NONE),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='YIELD_FACTOR:(real)',
    #         transform=Transform(TransformEnum.FILL_AVG),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='IRRIGATION_AFTER_SOWING:(mm)',
    #         transform=Transform(TransformEnum.FILL_CERO),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SOIL_ROOT_BARRIER:(Y/N/U)',
    #         transform=Transform(TransformEnum.STR_UNKNOWN),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GPS Altitude:(integer)',
    #         transform=Transform(TransformEnum.PASS),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GPS Latitude (Decimal)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.COORDINATE_DECIMAL,
    #             column_coordinate_degree="GPS Latitude (Degrees):(integer)",
    #             column_coordinate_minute="GPS Latitude (Minutes):(integer)",
    #             column_coordinate_NSEW="GPS Latitude (N or S):(TEXT)"
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GPS Longitude (Decimal)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.COORDINATE_DECIMAL,
    #             column_coordinate_degree="GPS Longitude (Degress):(integer)",
    #             column_coordinate_minute="GPS Longitude (Minutes):(integer)",
    #             column_coordinate_NSEW="GPS Longitude ( E or W):(TEXT)"
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SOIL_PERCENT_ORGANIC_MATTER:(%)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SOIL_DEPTH_OF_ROOT_ZONE:(cm)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='FUNGICIDE:(Y/N)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.STR_NO,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='PESTICIDE:(Y/N)',
    #         transform=Transform(
    #             transformEnum=TransformEnum.STR_NO,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_TO_ONE)
    #     ),
    #     TransformNormalize(
    #         column='1000_GRAIN_WEIGHT:(g):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='ABOVE_GROUND_BIOMASS:(t/ha):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='AGRONOMIC_SCORE:(1-5):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='CANOPY_TEMPERATURE_DEPRESSION:(oC):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='CHLOROPHYLL:(integer):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='Canopy Temperature:(real):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='DAYS_TO_HEADING:(days):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='DAYS_TO_MATURITY:(days):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='EARLY_VIGOR:(1-5):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GERMINATION_%:(%):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GRAINS/SPIKE:(NO_GRAINS/SPIKE):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='GRAIN_PROTEIN:(%):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='PLANT_HEIGHT:(cm):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SEDIMENTATION_INDEX:(%):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SPIKELETS/SPIKE:(integer):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SPIKE_LENGTH:(cm):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='SPIKES_M2:(ears/m2):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='TEST_WEIGHT:(kg/hl):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    #     TransformNormalize(
    #         column='Yellow color index (b-value):(real):avg',
    #         transform=Transform(
    #             transformEnum=TransformEnum.FILL_AVG,
    #         ),
    #         normalize=Normalize(normalizeEnum=NormalizeEnum.ONE_POSITIVE)
    #     ),
    # ]

    actions = [
        TransformNormalize(
            column="GRAIN_YIELD:(t/ha):avg",
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        ),
        TransformNormalize(
            column="country",
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        ),
        TransformNormalize(
            column='SOWING_DATE:(date)',
            transform=Transform(transformEnum=TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS),
        ),
        TransformNormalize(
            column='HARVEST_STARTING_DATE:(date)',
            transform=Transform(TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        ),
        TransformNormalize(
<<<<<<< HEAD
=======
            column='EMERGENCE_DATE:(date)',
            transform=Transform(TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        ),
        TransformNormalize(
>>>>>>> 94b84ca (Adding requirenments)
            column='GPS Altitude:(integer)',
            transform=Transform(TransformEnum.PASS),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        ),
        TransformNormalize(
            column='GPS Latitude (Decimal)',
            transform=Transform(
                transformEnum=TransformEnum.COORDINATE_DECIMAL,
                column_coordinate_degree="GPS Latitude (Degrees):(integer)",
                column_coordinate_minute="GPS Latitude (Minutes):(integer)",
                column_coordinate_NSEW="GPS Latitude (N or S):(TEXT)"
            ),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        ),
        TransformNormalize(
            column='GPS Longitude (Decimal)',
            transform=Transform(
                transformEnum=TransformEnum.COORDINATE_DECIMAL,
                column_coordinate_degree="GPS Longitude (Degress):(integer)",
                column_coordinate_minute="GPS Longitude (Minutes):(integer)",
                column_coordinate_NSEW="GPS Longitude ( E or W):(TEXT)"
            ),
            normalize=Normalize(normalizeEnum=NormalizeEnum.PASS)
        ),
    ]

    doRun(
        save_file='test.csv',
        name_file='./dataset.csv',
        actions=actions,
        remove_rows=remove_rows,
    )
