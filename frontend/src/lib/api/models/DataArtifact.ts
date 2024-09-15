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
    dataset_type: string;
    created_at?: string;
    url?: (string | null);
    pipeline_name?: (string | null);
    parent_name?: (string | null);
    num_rows?: (number | null);
    num_columns?: (number | null);
    data_schema?: (Array<ColSpec> | null);
};

