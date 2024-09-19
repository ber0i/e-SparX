/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CodeArtifact } from '../models/CodeArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CodeArtifactsService {
    /**
     * Register Code Artifact
     * Register a code artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerCodeArtifactCodeArtifactsPost(
        requestBody: CodeArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/code-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
