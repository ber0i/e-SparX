/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { PyTorchFormat } from './PyTorchFormat';
/**
 * Schema for a model artifact
 */
export type ModelArtifact = {
    name: string;
    description: string;
    artifact_type: string;
    file_type: string;
    flavor: string;
    created_at?: string;
    source_url?: (string | null);
    download_url?: (string | null);
    pipeline_name?: (string | null);
    parent_name?: (string | null);
    dependencies?: (Array<string> | null);
    input_format?: (Array<PyTorchFormat> | null);
    output_format?: (Array<PyTorchFormat> | null);
};

