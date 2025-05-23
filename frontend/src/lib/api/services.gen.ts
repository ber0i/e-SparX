// This file is auto-generated by @hey-api/openapi-ts

import { createClient, createConfig, type Options } from '@hey-api/client-fetch';
import type { RegisterCodeArtifactRegisterCodePostData, RegisterCodeArtifactRegisterCodePostError, RegisterCodeArtifactRegisterCodePostResponse, RegisterHyperparametersArtifactRegisterHyperparametersPostData, RegisterHyperparametersArtifactRegisterHyperparametersPostError, RegisterHyperparametersArtifactRegisterHyperparametersPostResponse, RegisterDatasetArtifactRegisterDatasetPostData, RegisterDatasetArtifactRegisterDatasetPostError, RegisterDatasetArtifactRegisterDatasetPostResponse, RegisterModelArtifactRegisterModelPostData, RegisterModelArtifactRegisterModelPostError, RegisterModelArtifactRegisterModelPostResponse, RegisterParametersArtifactRegisterParametersPostData, RegisterParametersArtifactRegisterParametersPostError, RegisterParametersArtifactRegisterParametersPostResponse, RegisterResultsArtifactRegisterResultsPostData, RegisterResultsArtifactRegisterResultsPostError, RegisterResultsArtifactRegisterResultsPostResponse, GetArtifactsArtifactsGetError, GetArtifactsArtifactsGetResponse, GetArtifactsForGlobalViewArtifactsGlobalGetError, GetArtifactsForGlobalViewArtifactsGlobalGetResponse, GetArtifactsByPipelineArtifactsPipelinePipelineNameGetData, GetArtifactsByPipelineArtifactsPipelinePipelineNameGetError, GetArtifactsByPipelineArtifactsPipelinePipelineNameGetResponse, GetNeighborsArtifactsNeighborsNameGetData, GetNeighborsArtifactsNeighborsNameGetError, GetNeighborsArtifactsNeighborsNameGetResponse, GetArtifactByNameArtifactsNameNameGetData, GetArtifactByNameArtifactsNameNameGetError, GetArtifactByNameArtifactsNameNameGetResponse, RemoveArtifactByNameArtifactsNameNameDeleteData, RemoveArtifactByNameArtifactsNameNameDeleteError, RemoveArtifactByNameArtifactsNameNameDeleteResponse, GetPipelinesPipelinesGetError, GetPipelinesPipelinesGetResponse, GetPipelinesByArtifactPipelinesArtifactArtifactNameGetData, GetPipelinesByArtifactPipelinesArtifactArtifactNameGetError, GetPipelinesByArtifactPipelinesArtifactArtifactNameGetResponse, GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetData, GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetError, GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetResponse, GetConnectionsByPipelineConnectionsPipelinePipelineNameGetData, GetConnectionsByPipelineConnectionsPipelinePipelineNameGetError, GetConnectionsByPipelineConnectionsPipelinePipelineNameGetResponse, CreateConnectionConnectionsCreatePostData, CreateConnectionConnectionsCreatePostError, CreateConnectionConnectionsCreatePostResponse, GetConnectionsConnectionsGetError, GetConnectionsConnectionsGetResponse, RootGetError, RootGetResponse } from './types.gen';

export const client = createClient(createConfig());

/**
 * Register Code Artifact
 * Register code artifact
 */
export const registerCodeArtifactRegisterCodePost = <ThrowOnError extends boolean = false>(options: Options<RegisterCodeArtifactRegisterCodePostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterCodeArtifactRegisterCodePostResponse, RegisterCodeArtifactRegisterCodePostError, ThrowOnError>({
    ...options,
    url: '/register/code'
}); };

/**
 * Register Hyperparameters Artifact
 * Register hyperparameters artifact
 */
export const registerHyperparametersArtifactRegisterHyperparametersPost = <ThrowOnError extends boolean = false>(options: Options<RegisterHyperparametersArtifactRegisterHyperparametersPostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterHyperparametersArtifactRegisterHyperparametersPostResponse, RegisterHyperparametersArtifactRegisterHyperparametersPostError, ThrowOnError>({
    ...options,
    url: '/register/hyperparameters'
}); };

/**
 * Register Dataset Artifact
 * Register dataset artifact
 */
export const registerDatasetArtifactRegisterDatasetPost = <ThrowOnError extends boolean = false>(options: Options<RegisterDatasetArtifactRegisterDatasetPostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterDatasetArtifactRegisterDatasetPostResponse, RegisterDatasetArtifactRegisterDatasetPostError, ThrowOnError>({
    ...options,
    url: '/register/dataset'
}); };

/**
 * Register Model Artifact
 * Register model artifact
 */
export const registerModelArtifactRegisterModelPost = <ThrowOnError extends boolean = false>(options: Options<RegisterModelArtifactRegisterModelPostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterModelArtifactRegisterModelPostResponse, RegisterModelArtifactRegisterModelPostError, ThrowOnError>({
    ...options,
    url: '/register/model'
}); };

/**
 * Register Parameters Artifact
 * Register parameters artifact
 */
export const registerParametersArtifactRegisterParametersPost = <ThrowOnError extends boolean = false>(options: Options<RegisterParametersArtifactRegisterParametersPostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterParametersArtifactRegisterParametersPostResponse, RegisterParametersArtifactRegisterParametersPostError, ThrowOnError>({
    ...options,
    url: '/register/parameters'
}); };

/**
 * Register Results Artifact
 * Register results artifact
 */
export const registerResultsArtifactRegisterResultsPost = <ThrowOnError extends boolean = false>(options: Options<RegisterResultsArtifactRegisterResultsPostData, ThrowOnError>) => { return (options?.client ?? client).post<RegisterResultsArtifactRegisterResultsPostResponse, RegisterResultsArtifactRegisterResultsPostError, ThrowOnError>({
    ...options,
    url: '/register/results'
}); };

/**
 * Get Artifacts
 * Get all artifacts from the DocumentDB
 */
export const getArtifactsArtifactsGet = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => { return (options?.client ?? client).get<GetArtifactsArtifactsGetResponse, GetArtifactsArtifactsGetError, ThrowOnError>({
    ...options,
    url: '/artifacts/'
}); };

/**
 * Get Artifacts For Global View
 * Get all artifacts from the DAG DB for global view
 */
export const getArtifactsForGlobalViewArtifactsGlobalGet = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => { return (options?.client ?? client).get<GetArtifactsForGlobalViewArtifactsGlobalGetResponse, GetArtifactsForGlobalViewArtifactsGlobalGetError, ThrowOnError>({
    ...options,
    url: '/artifacts/global'
}); };

/**
 * Get Artifacts By Pipeline
 * Get all artifacts in a pipeline
 */
export const getArtifactsByPipelineArtifactsPipelinePipelineNameGet = <ThrowOnError extends boolean = false>(options: Options<GetArtifactsByPipelineArtifactsPipelinePipelineNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetArtifactsByPipelineArtifactsPipelinePipelineNameGetResponse, GetArtifactsByPipelineArtifactsPipelinePipelineNameGetError, ThrowOnError>({
    ...options,
    url: '/artifacts/pipeline/{pipeline_name}'
}); };

/**
 * Get Neighbors
 * Get all neighbors (in any pipeline) of an artifact by artifact name
 */
export const getNeighborsArtifactsNeighborsNameGet = <ThrowOnError extends boolean = false>(options: Options<GetNeighborsArtifactsNeighborsNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetNeighborsArtifactsNeighborsNameGetResponse, GetNeighborsArtifactsNeighborsNameGetError, ThrowOnError>({
    ...options,
    url: '/artifacts/neighbors/{name}'
}); };

/**
 * Get Artifact By Name
 * Get a single artifact by name
 */
export const getArtifactByNameArtifactsNameNameGet = <ThrowOnError extends boolean = false>(options: Options<GetArtifactByNameArtifactsNameNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetArtifactByNameArtifactsNameNameGetResponse, GetArtifactByNameArtifactsNameNameGetError, ThrowOnError>({
    ...options,
    url: '/artifacts/name/{name}'
}); };

/**
 * Remove Artifact By Name
 * Remove a single artifact by name
 */
export const removeArtifactByNameArtifactsNameNameDelete = <ThrowOnError extends boolean = false>(options: Options<RemoveArtifactByNameArtifactsNameNameDeleteData, ThrowOnError>) => { return (options?.client ?? client).delete<RemoveArtifactByNameArtifactsNameNameDeleteResponse, RemoveArtifactByNameArtifactsNameNameDeleteError, ThrowOnError>({
    ...options,
    url: '/artifacts/name/{name}'
}); };

/**
 * Get Pipelines
 * Get all pipelines in the DAG database.
 */
export const getPipelinesPipelinesGet = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => { return (options?.client ?? client).get<GetPipelinesPipelinesGetResponse, GetPipelinesPipelinesGetError, ThrowOnError>({
    ...options,
    url: '/pipelines/'
}); };

/**
 * Get Pipelines By Artifact
 * Get all pipelines in the DAG database that contain a specific artifact.
 */
export const getPipelinesByArtifactPipelinesArtifactArtifactNameGet = <ThrowOnError extends boolean = false>(options: Options<GetPipelinesByArtifactPipelinesArtifactArtifactNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetPipelinesByArtifactPipelinesArtifactArtifactNameGetResponse, GetPipelinesByArtifactPipelinesArtifactArtifactNameGetError, ThrowOnError>({
    ...options,
    url: '/pipelines/artifact/{artifact_name}'
}); };

/**
 * Get Results Artifacts By Pipeline
 * Get all results artifacts in a pipeline
 */
export const getResultsArtifactsByPipelinePipelinesResultsPipelineNameGet = <ThrowOnError extends boolean = false>(options: Options<GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetResponse, GetResultsArtifactsByPipelinePipelinesResultsPipelineNameGetError, ThrowOnError>({
    ...options,
    url: '/pipelines/results/{pipeline_name}'
}); };

/**
 * Get Connections By Pipeline
 * Get all connections in a pipeline
 */
export const getConnectionsByPipelineConnectionsPipelinePipelineNameGet = <ThrowOnError extends boolean = false>(options: Options<GetConnectionsByPipelineConnectionsPipelinePipelineNameGetData, ThrowOnError>) => { return (options?.client ?? client).get<GetConnectionsByPipelineConnectionsPipelinePipelineNameGetResponse, GetConnectionsByPipelineConnectionsPipelinePipelineNameGetError, ThrowOnError>({
    ...options,
    url: '/connections/pipeline/{pipeline_name}'
}); };

/**
 * Create Connection
 * Create a connection between two artifacts in a pipeline
 */
export const createConnectionConnectionsCreatePost = <ThrowOnError extends boolean = false>(options: Options<CreateConnectionConnectionsCreatePostData, ThrowOnError>) => { return (options?.client ?? client).post<CreateConnectionConnectionsCreatePostResponse, CreateConnectionConnectionsCreatePostError, ThrowOnError>({
    ...options,
    url: '/connections/create'
}); };

/**
 * Get Connections
 * Get all connections
 */
export const getConnectionsConnectionsGet = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => { return (options?.client ?? client).get<GetConnectionsConnectionsGetResponse, GetConnectionsConnectionsGetError, ThrowOnError>({
    ...options,
    url: '/connections/'
}); };

/**
 * Root
 * Base route with welcome message.
 */
export const rootGet = <ThrowOnError extends boolean = false>(options?: Options<unknown, ThrowOnError>) => { return (options?.client ?? client).get<RootGetResponse, RootGetError, ThrowOnError>({
    ...options,
    url: '/'
}); };