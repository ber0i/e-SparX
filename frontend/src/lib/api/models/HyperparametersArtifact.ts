/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Hyperparameter } from './Hyperparameter';
/**
 * Schema for a hyperparameters artifact
 */
export type HyperparametersArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    created_at?: string;
    source_url?: (string | null);
    download_url?: (string | null);
    hyperparameters: Array<Hyperparameter>;
    pipeline_name?: (string | null);
    parent_name?: (string | null);
};

