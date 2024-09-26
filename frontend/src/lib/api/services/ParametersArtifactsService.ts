/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ParametersArtifact } from '../models/ParametersArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ParametersArtifactsService {
    /**
     * Register Parameters Artifact
     * Register a parameters artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerParametersArtifactParametersArtifactsPost(
        requestBody: ParametersArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/parameters-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
