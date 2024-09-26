/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Hyperparameter } from './Hyperparameter';
/**
 * Schema for a hyperparameter artifact
 */
export type HyperparameterArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    created_at?: string;
    hyperparameters: Array<Hyperparameter>;
    pipeline_name?: (string | null);
    parent_name?: (string | null);
};

