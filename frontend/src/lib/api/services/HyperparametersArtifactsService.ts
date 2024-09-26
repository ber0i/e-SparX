/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HyperparametersArtifact } from '../models/HyperparametersArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class HyperparametersArtifactsService {
    /**
     * Register Hyperparameters Artifact
     * Register a hyperparameters artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerHyperparametersArtifactHyperparametersArtifactsPost(
        requestBody: HyperparametersArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/hyperparameters-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
