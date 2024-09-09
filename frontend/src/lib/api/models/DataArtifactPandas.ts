/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColSpec } from './ColSpec';
/**
 * Schema for a pandas.DataFrame data artifact
 */
export type DataArtifactPandas = {
    name: string;
    description: string;
    dataset_type: string;
    created_at?: string;
    url?: (string | null);
    num_rows: number;
    num_columns: number;
    schema?: Array<ColSpec>;
};

