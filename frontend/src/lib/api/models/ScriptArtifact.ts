/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
/**
 * Schema for a script artifact
 */
export type ScriptArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    created_at?: string;
    source_url?: (string | null);
    download_url?: (string | null);
    pipeline_name?: (string | null);
    parent_name?: (string | null);
    input_artifact?: (string | null);
    output_artifact?: (string | null);
};

