import energy_data_lab as edl

edl.register_data_free(
    name="Kelmarsh SCADA 2022 Raw",
    description="Raw Kelmarsh SCADA data from 2022, downloaded from Zenodo as ZIP file.",
    source_url="https://zenodo.org/records/8252025",
    download_url="https://zenodo.org/records/8252025/files/Kelmarsh_SCADA_2022_4457.zip?download=1",
    pipeline_name="Wind Power Forecasting",
)


edl.register_data_free(
    name="Kelmarsh Static Turbine Data",
    description="Static Kelmarsh turbine data, downloaded from Zenodo as CSV file.",
    source_url="https://zenodo.org/records/8252025",
    download_url="https://zenodo.org/records/8252025/files/Kelmarsh_WT_static.csv?download=1",
    pipeline_name="Wind Power Forecasting",
)
