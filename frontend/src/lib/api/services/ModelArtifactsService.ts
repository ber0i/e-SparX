/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ModelArtifact } from '../models/ModelArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ModelArtifactsService {
    /**
     * Register Model Artifact
     * Register a model artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerModelArtifactModelArtifactsPost(
        requestBody: ModelArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/model-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
