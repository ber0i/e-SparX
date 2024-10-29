/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import { ColSpec, PyTorchFormat, Hyperparameter, Result } from "@/lib/api";

/**
 * Typescript schema for any artifact
 */
export type Artifact = {
  name: string;
  description: string;
  artifact_type: string;
  file_type: string;
  artifact_subtype?: string | null;
  flavor?: string | null;
  created_at?: string;
  source_url?: string | null;
  download_url?: string | null;
  pipeline_name?: string | null;
  parent_name?: string | null;
  num_rows?: number | null;
  num_columns?: number | null;
  data_schema?: Array<ColSpec> | null;
  index_name?: string | null;
  index_dtype?: string | null;
  dependencies?: Array<string> | null;
  input_format?: Array<PyTorchFormat> | null;
  output_format?: Array<PyTorchFormat> | null;
  hyperparameters?: Array<Hyperparameter> | null;
  results?: Array<Result> | null;
};
