/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Result } from './Result';
/**
 * Schema for a results artifact
 */
export type ResultsArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    results: Array<Result>;
    created_at?: string;
    pipeline_name?: (string | null);
    parent_name?: (string | null);
};

