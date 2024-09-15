/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ConnectionResponse } from '../models/ConnectionResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ConnectionsService {
    /**
     * Get Connections By Pipeline
     * Get all connections in a pipeline
     * @param pipelineName
     * @returns ConnectionResponse Successful Response
     * @throws ApiError
     */
    public static getConnectionsByPipelineConnectionsPipelinePipelineNameGet(
        pipelineName: string,
    ): CancelablePromise<Array<ConnectionResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/connections/pipeline/{pipeline_name}',
            path: {
                'pipeline_name': pipelineName,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
