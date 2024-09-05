/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { DataArtifact } from '../models/DataArtifact';
import type { DataArtifactPandas } from '../models/DataArtifactPandas';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DataArtifactService {
    /**
     * View Artifacts
     * Get all artifacts
     * @returns any Successful Response
     * @throws ApiError
     */
    public static viewArtifactsDataArtifactGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifact/',
        });
    }
    /**
     * Register Data Artifact
     * Register a data artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerDataArtifactDataArtifactPost(
        requestBody: DataArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/data-artifact/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Register Pandas Data Artifact
     * Register a Pandas data artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerPandasDataArtifactDataArtifactPandasPost(
        requestBody: DataArtifactPandas,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/data-artifact/pandas/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Artifact By Name
     * Get a single data artifact by name
     * @param name
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtifactByNameDataArtifactNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifact/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
