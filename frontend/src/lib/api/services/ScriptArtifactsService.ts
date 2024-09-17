/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ScriptArtifact } from '../models/ScriptArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ScriptArtifactsService {
    /**
     * Register Script Artifact
     * Register a code script artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerScriptArtifactScriptArtifactsPost(
        requestBody: ScriptArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/script-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
