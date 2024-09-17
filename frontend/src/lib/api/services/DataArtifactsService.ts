/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ArtifactResponse } from '../models/ArtifactResponse';
import type { DataArtifact } from '../models/DataArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class DataArtifactsService {
    /**
     * Get Artifacts
     * Get all artifacts
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtifactsDataArtifactsGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifacts/',
        });
    }
    /**
     * Register Data Artifact
     * Register a data artifact. Currently supported: Free-form and pd.DataFrame data artifacts.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerDataArtifactDataArtifactsPost(
        requestBody: DataArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/data-artifacts/',
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
    public static getArtifactByNameDataArtifactsNameGet(
        name: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifacts/{name}',
            path: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Artifacts By Pipeline
     * Get all artifacts in a pipeline
     * @param pipelineName
     * @returns ArtifactResponse Successful Response
     * @throws ApiError
     */
    public static getArtifactsByPipelineDataArtifactsPipelinePipelineNameGet(
        pipelineName: string,
    ): CancelablePromise<Array<ArtifactResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifacts/pipeline/{pipeline_name}',
            path: {
                'pipeline_name': pipelineName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
