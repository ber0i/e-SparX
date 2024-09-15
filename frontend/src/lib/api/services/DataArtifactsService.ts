/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ArtifactResponse } from '../models/ArtifactResponse';
import type { DataArtifactFree } from '../models/DataArtifactFree';
import type { DataArtifactPandas } from '../models/DataArtifactPandas';
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
     * Register Free Data Artifact
     * Register a free-form data artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerFreeDataArtifactDataArtifactsPost(
        requestBody: DataArtifactFree,
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
     * Register Pandas Data Artifact
     * Register a pandas.DataFrame data artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerPandasDataArtifactDataArtifactsPandasPost(
        requestBody: DataArtifactPandas,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/data-artifacts/pandas',
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
