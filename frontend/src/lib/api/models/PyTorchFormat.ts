/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { TensorSpec } from './TensorSpec';
/**
 * Schema for an input/output format used in PyTorch model artifacts.
 */
export type PyTorchFormat = {
    type: string;
    tensor_spec: TensorSpec;
};

