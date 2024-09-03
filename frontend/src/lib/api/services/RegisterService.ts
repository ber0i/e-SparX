/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DataArtifact } from '../models/DataArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class RegisterService {
    /**
     * View Artifacts
     * Get all artifacts
     * @returns any Successful Response
     * @throws ApiError
     */
    public static viewArtifactsRegisterGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/register/',
        });
    }
    /**
     * Register Artifact
     * Register an artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerArtifactRegisterPost(
        requestBody: DataArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/register/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
