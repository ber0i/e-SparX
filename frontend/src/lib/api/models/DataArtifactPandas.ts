/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ColSpec } from './ColSpec';
/**
 * Schema for an artifact of type Pandas data
 */
export type DataArtifactPandas = {
    name: string;
    description: string;
    dataset_type: string;
    num_rows: number;
    num_columns: number;
    schema?: Array<ColSpec>;
};

