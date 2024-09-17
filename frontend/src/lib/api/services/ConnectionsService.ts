/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ConnectionCreation } from '../models/ConnectionCreation';
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
    /**
     * Create Connection
     * Create a connection between two artifacts in a pipeline
     * @param requestBody
     * @returns any Successful Response
     * @throws ApiError
     */
    public static createConnectionConnectionsCreatePost(
        requestBody: ConnectionCreation,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/connections/create',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
