/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PipelinesService {
    /**
     * Get Pipelines
     * Get all pipelines in the DAG database.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getPipelinesPipelinesGet(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/pipelines/',
        });
    }
}
