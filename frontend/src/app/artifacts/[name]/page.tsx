"use client";

import { useEffect, useState } from "react";
import { DataArtifactsService } from "@/lib/api/services/DataArtifactsService";
import { PipelinesService } from "@/lib/api/services/PipelinesService";
import type { Artifact } from "@/lib/manual/artifact";
import type { Pipeline } from "@/lib/manual/pipeline"

export default function ArtifactDetailPage({ params }: { params: { name: string } }) {
  // Get the artifact name from the URL
  const name = params.name;
  const [artifact, setArtifact] = useState<Artifact | null>(null);
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);

  useEffect(() => {
    const fetchArtifactDetails = async () => {
      if (name) {
        try {
          // Fetch artifact by name
          const response = await DataArtifactsService.getArtifactByNameDataArtifactsNameGet(name as string);
          setArtifact(response);
        } catch (error) {
          console.error("Failed to fetch artifact details", error);
        }
      }
    };
    const fetchPipelines = async () => {
      if (name) {
        try {
          const decodedName = decodeURIComponent(name as string);
          const fetchedPipelines = await PipelinesService.getPipelinesByArtifactPipelinesArtifactNameGet(decodedName as string);
          setPipelines(fetchedPipelines);
        } catch (error) {
          console.error("Failed to fetch pipelines", error);
        }
      }
    };
    fetchArtifactDetails();
    fetchPipelines();
  }, [name]);

  

  if (!artifact) {
    return <div>Loading...</div>;
  }

  const formatDate = (dateString: string | undefined) => {
    if (!dateString) {
      return "N/A";  // Return fallback if dateString is undefined
    }
    const date = new Date(dateString);
    return date.toLocaleString("en-US", {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      timeZone: "Europe/Berlin",  // Use Germany's time zone
    });
  };

  return (
    <div className="p-5">
      <h1>Artifact Details: {artifact.name}</h1>
      <div className="artifact-info">
        <p className="key">Description:</p>
        <p className="value">{artifact.description}</p>

        <p className="key">Artifact Type:</p>
        <p className="value">{artifact.artifact_type}</p>

        {artifact.artifact_type === "dataset" ? (
          <>
            <p className="key">Subtype:</p>
            <p className="value">{artifact.artifact_subtype}</p>
          </>
        ) : (
          <></>
        )}

        {artifact.artifact_type === "model" ? (
          <>
            <p className="key">Model Flavor:</p>
            <p className="value">{artifact.flavor}</p>
          </>
        ) : (
          <></>
        )}

        {artifact.artifact_type !== "results" ? (
          <>
            <p className="key">File Type:</p>
            <p className="value">{artifact.file_type}</p>
          </>
        ) : (
          <></>
        )}

        <p className="key">Created At:</p>
        <p className="value">{formatDate(artifact.created_at)}</p>

        {artifact.artifact_type === "model" ? (
          <>
            <p className="key">Dependencies:</p>
            <div className="value">
              <ul className="inline-flex">
              {artifact.dependencies && artifact.dependencies.length > 0 ? (
                artifact.dependencies.map((dependency, index) => (
                  <li key={index} className="mr-1">
                    {dependency}
                    {/* @ts-ignore */}
                    {index < artifact.dependencies.length - 1 && ", "} 
                  </li>
                ))
              ) : (
                <li>Not available.</li>
              )}
              </ul>
            </div>
          </>
        ) : (
          <></>
        )}

        {artifact.artifact_type !== "results" ? (
          <>
            <p className="key">URL:</p>
            <p className="value">
              {artifact.source_url ? (
                <a href={artifact.source_url} target="_blank" rel="noopener noreferrer" className="artifact-link">
                  {artifact.source_url}
                </a>
              ) : (
                "not available"
              )}
            </p>

            <p className="key">Download URL:</p>
            <p className="value">
              {artifact.download_url ? (
                <a href={artifact.download_url} target="_blank" rel="noopener noreferrer" className="artifact-link">
                  {artifact.download_url}
                </a>
              ) : (
                "not available"
              )}
            </p>
          </>
        ) : (
          <></>
        )}

        <p className="key">Pipelines:</p>
        <div className="value">
          {pipelines.length > 0 ? (
            <ul className="inline-flex">
              {pipelines.map((pipeline, index) => (
                <li key={index} className="mr-1">
                  <a href={`/pipelines/${pipeline.name}`}>{pipeline.name}</a>
                {index < pipelines.length - 1 && ", "}
              </li>
              ))}
            </ul>
          ) : (
            "not available"
          )}
        </div>
      </div>

      {artifact.artifact_type === "dataset" && (
        <>
        {artifact.data_schema && artifact.data_schema.length > 0 ? (
          <div className="overflow-x-auto">
            <h2>Dataset Schema</h2>
            <div className="artifact-info">

              <p className="key">Number of Rows:</p>
              <p className="value">{artifact.num_rows ? artifact.num_rows : "not available"}</p>

              <p className="key">Number of Columns:</p>
              <p className="value">{artifact.num_columns ? artifact.num_columns : "not available"}</p>

              <p className="key">Index:</p>
              <p className="value">{artifact.index_name} (data type: {artifact.index_dtype})</p>

            </div>
            <table className="min-w-full leading-normal border">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Column Name
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Data Type
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Required
                  </th>
                </tr>
              </thead>
              <tbody>
                {artifact.data_schema.map((colSpec, index) => (
                  <tr key={index}>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {colSpec.name}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      {colSpec.type}
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      {colSpec.required ? "Yes" : "No"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>No schema available for this artifact.</p>
        )}
        </>
      )}

      {artifact.artifact_type === "hyperparameters" && (
        <>
        {artifact.hyperparameters && artifact.hyperparameters.length > 0 ? (
          <div className="overflow-x-auto">
            <h2>Hyperparameters</h2>
            <div className="w-1/2">
            <table className="leading-normal border w-full">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Name
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Value
                  </th>
                </tr>
              </thead>
              <tbody>
                {artifact.hyperparameters.map((hyperparameter, index) => (
                  <tr key={index}>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {hyperparameter.name}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      {hyperparameter.value}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          </div>
        ) : (
          <></>
        )}
        </>
      )}

      {artifact.artifact_type === "results" && (
        <>
        {artifact.results && artifact.results.length > 0 ? (
          <div className="overflow-x-auto">
            <h2>Results</h2>
            <div className="w-1/2">
            <table className="leading-normal border w-full">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Metric
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Value
                  </th>
                </tr>
              </thead>
              <tbody>
                {artifact.results.map((result, index) => (
                  <tr key={index}>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {result.metric}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      {result.value}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            </div>
          </div>
        ) : (
          <></>
        )}
        </>
      )}  

      {artifact.artifact_type === "model" && (
        <>
        {artifact.input_format && artifact.input_format.length > 0 ? (
          <div className="overflow-x-auto">
            <h2>Input Format</h2>
            <div className="w-1/2">
              <table className="leading-normal border w-full">
                <thead>
                  <tr>
                    <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                      Data Type
                    </th>
                    <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                      Shape
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {artifact.input_format.map((format, index) => (
                    <tr key={index}>
                      <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                        <div className="text-contrast whitespace-no-wrap">
                          {format.tensor_spec.dtype}
                        </div>
                      </td>
                      <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                        {JSON.stringify(format.tensor_spec.shape)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <h2 className="mt-4">Output Format</h2>
            <div className="w-1/2">
              <table className="leading-normal border w-full">
                <thead>
                  <tr>
                    <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                      Data Type
                    </th>
                    <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                      Shape
                    </th>
                  </tr>
                </thead>
                <tbody>
                {/* @ts-ignore */}
                {artifact.output_format.map((format, index) => (
                  <tr key={index}>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {format.tensor_spec.dtype}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      {JSON.stringify(format.tensor_spec.shape)}
                    </td>
                  </tr>
                ))}
                </tbody>
              </table>
            </div>
        </div>
        ) : (
          <p>No input and output formats available for this artifact.</p>
        )}
        </>
      )}
    </div>
  );
}
