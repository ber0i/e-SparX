import energy_data_lab as edl

edl.register_data_free(
    name="a1",
    description="Artifact 1 in pipeline 1.",
    pipeline_name="p1",
)

edl.register_data_free(
    name="a2",
    description="Artifact 2 in pipeline 1.",
    pipeline_name="p1",
    parent_name="a1",
)

edl.register_data_free(
    name="a1",
    description="Artifact 1 in pipeline 2.",
    pipeline_name="p2",
    parent_name="a2",
)

edl.register_data_free(
    name="a2", description="Artifact 2 in pipeline 2.", pipeline_name="p2"
)

edl.register_data_free(
    name="a3",
    description="Artifact 3 in pipeline 2.",
    pipeline_name="p2",
    parent_name="a1",
)
