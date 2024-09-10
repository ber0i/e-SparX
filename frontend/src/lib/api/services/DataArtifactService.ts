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
export class DataArtifactService {
    /**
     * Get Artifacts
     * Get all artifacts
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getArtifactsDataArtifactGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifact/',
        });
    }
    /**
     * Register Free Data Artifact
     * Register a free-form data artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerFreeDataArtifactDataArtifactPost(
        requestBody: DataArtifactFree,
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
     * Register a pandas.DataFrame data artifact. Saves the artifact in the document database.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerPandasDataArtifactDataArtifactPandasPost(
        requestBody: DataArtifactPandas,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/data-artifact/pandas',
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
    /**
     * Get Artifacts By Pipeline
     * Get all artifacts in a pipeline
     * @param pipelineName
     * @returns ArtifactResponse Successful Response
     * @throws ApiError
     */
    public static getArtifactsByPipelineDataArtifactPipelinePipelineNameGet(
        pipelineName: string,
    ): CancelablePromise<Array<ArtifactResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/data-artifact/pipeline/{pipeline_name}',
            path: {
                'pipeline_name': pipelineName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
