/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColSpec } from './ColSpec';
/**
 * Schema for a data artifact
 */
export type DataArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    created_at?: string;
    source_url?: (string | null);
    download_url?: (string | null);
    pipeline_name?: (string | null);
    parent_name?: (string | null);
    num_rows?: (number | null);
    num_columns?: (number | null);
    data_schema?: (Array<ColSpec> | null);
    index_name?: (string | null);
    index_dtype?: (string | null);
};

