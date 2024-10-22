/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ResultsArtifact } from '../models/ResultsArtifact';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ResultsArtifactsService {
    /**
     * Register Results Artifact
     * Register a hyperparameters artifact.
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static registerResultsArtifactResultsArtifactsPost(
        requestBody: ResultsArtifact,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/results-artifacts/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Results Artifacts By Pipeline
     * Get all results artifacts in a pipeline
     * @param pipelineName
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getResultsArtifactsByPipelineResultsArtifactsPipelinePipelineNameGet(
        pipelineName: string,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/results-artifacts/pipeline/{pipeline_name}',
            path: {
                'pipeline_name': pipelineName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
