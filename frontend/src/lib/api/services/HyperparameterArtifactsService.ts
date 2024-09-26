/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { HyperparameterArtifact } from '../models/HyperparameterArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class HyperparameterArtifactsService {
    /**
     * Register Hyperparameter Artifact
     * Register a hyperparameter artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerHyperparameterArtifactHyperparameterArtifactsPost(
        requestBody: HyperparameterArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/hyperparameter-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
