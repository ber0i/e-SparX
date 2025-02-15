"use client";

import { useEffect, useState } from "react";
import {
  getArtifactByNameArtifactsNameNameGet,
  getPipelinesByArtifactPipelinesArtifactArtifactNameGet,
  getNeighborsArtifactsNeighborsNameGet,
} from "@/lib/api";
import { formatDate } from "@/lib/manual/format_date";
import type { Artifact } from "@/lib/manual/artifact";
import type { Pipeline } from "@/lib/manual/pipeline";
import type { Neighbor } from "@/lib/manual/neighbor";

export default function ArtifactDetailPage({
  params,
}: {
  params: { name: string };
}) {
  // Get the artifact name from the URL
  const name = params.name;
  const [artifact, setArtifact] = useState<Artifact | null>(null);
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [neighbors, setNeighbors] = useState<Neighbor[]>([]);

  useEffect(() => {
    // Fetch artifact by name
    const fetchArtifactDetails = async () => {
      if (name) {
        const { error, data } = await getArtifactByNameArtifactsNameNameGet({
          path: { name: name },
        });

        if (error) {
          console.error("Failed to fetch artifact details", error);
          return;
        }

        setArtifact(data as Artifact);
      }
    };

    // Fetch pipelines by artifact name
    const fetchPipelines = async () => {
      if (name) {
        const decodedName = decodeURIComponent(name as string);
        const { error, data } =
          await getPipelinesByArtifactPipelinesArtifactArtifactNameGet({
            path: { artifact_name: decodedName },
          });

        if (error) {
          console.error("Failed to fetch pipelines", error);
          return;
        }
        setPipelines(data as Pipeline[]);
      }
    };

    // Fetch neighbors of artifact by artifact name
    const fetchNeighbors = async () => {
      if (name) {
        const decodedName = decodeURIComponent(name as string);
        const { error, data } = await getNeighborsArtifactsNeighborsNameGet({
          path: { name: decodedName },
        });

        if (error) {
          console.error("Failed to fetch artifact neighbors", error);
          return;
        }
        setNeighbors(data as Neighbor[]);
      }
    };

    fetchArtifactDetails();
    fetchPipelines();
    fetchNeighbors();
  }, [name]);

  if (!artifact) {
    return <div>Loading...</div>;
  }

  return (
    <div className="p-5">
      <p className="text-3xl font-semibold pb-10">Artifact &quot;{artifact.name}&quot;</p>

      {/* Horizontal line */}
      <div className="w-1/2"
        style={{
          position: "absolute",
          top: "205px",
          left: "0",
          
          height: "2px",
          backgroundColor: "#072140",
        }}
      ></div>

      <div className="artifact-info">
        <p className="key text-brand-darkblue text-lg uppercase p-1">Description:</p>
        <p className="value text-brand-darkblue text-lg p-1">{artifact.description}</p>

        <p className="key text-brand-darkblue text-lg uppercase p-1">Artifact Type:</p>
        <p className="value text-brand-darkblue text-lg p-1">{artifact.artifact_type}</p>

        {artifact.artifact_type === "dataset" ? (
          <>
            <p className="key text-brand-darkblue text-lg uppercase p-1">Subtype:</p>
            <p className="value text-brand-darkblue text-lg p-1">{artifact.artifact_subtype}</p>
          </>
        ) : (
          <></>
        )}

        {artifact.artifact_type === "model" ? (
          <>
            <p className="key text-brand-darkblue text-lg uppercase p-1">Model Flavor:</p>
            <p className="value text-brand-darkblue text-lg p-1">{artifact.flavor}</p>
          </>
        ) : (
          <></>
        )}

        {artifact.artifact_type !== "results" ? (
          <>
            <p className="key text-brand-darkblue text-lg uppercase p-1">File Type:</p>
            <p className="value text-brand-darkblue text-lg p-1">{artifact.file_type}</p>
          </>
        ) : (
          <></>
        )}

        <p className="key text-brand-darkblue text-lg uppercase p-1">Created/Updated:</p>
        <p className="value text-brand-darkblue text-lg p-1">{formatDate(artifact.created_at)}</p>

        {artifact.artifact_type === "model" ? (
          <>
            <p className="key text-brand-darkblue text-lg uppercase p-1">Dependencies:</p>
            <div className="value text-brand-darkblue text-lg p-1">
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
            <p className="key text-brand-darkblue text-lg uppercase p-1">URL:</p>
            <p className="value text-brand-darkblue text-lg p-1">
              {artifact.source_url ? (
                <a
                  href={artifact.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="artifact-link"
                >
                  {artifact.source_url}
                </a>
              ) : (
                "not available"
              )}
            </p>

            <p className="key text-brand-darkblue text-lg uppercase p-1">Download URL:</p>
            <p className="value text-brand-darkblue text-lg p-1">
              {artifact.download_url ? (
                <a
                  href={artifact.download_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="artifact-link"
                >
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

        <p className="key text-brand-darkblue text-lg uppercase p-1">Pipelines:</p>
        <div className="value text-brand-darkblue text-lg p-1">
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

        <p className="key text-brand-darkblue text-lg uppercase p-1">Neighbors:</p>
        <div className="value text-brand-darkblue text-lg p-1">
          {neighbors.length > 0 ? (
            <ul className="inline-flex">
              {neighbors.map((neighbor, index) => (
                <li key={index} className="mr-1">
                  <a href={`/artifacts/${neighbor.name}`}>{neighbor.name}</a>
                  {index < neighbors.length - 1 && ", "}
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
                <p className="key text-brand-darkblue text-lg uppercase p-1">Number of Rows:</p>
                <p className="value text-brand-darkblue text-lg p-1">
                  {artifact.num_rows ? artifact.num_rows : "not available"}
                </p>

                <p className="key text-brand-darkblue text-lg uppercase p-1">Number of Columns:</p>
                <p className="value text-brand-darkblue text-lg p-1">
                  {artifact.num_columns
                    ? artifact.num_columns
                    : "not available"}
                </p>

                <p className="key text-brand-darkblue text-lg uppercase p-1">Index:</p>
                <p className="value text-brand-darkblue text-lg p-1">
                  {artifact.index_name} (data type: {artifact.index_dtype})
                </p>
              </div>
              <table className="leading-normal border w-1/2">
                <thead>
                  <tr>
                    <th>
                      Column Name
                    </th>
                    <th>
                      Data Type
                    </th>
                    {/*
                    <th>
                      Required
                    </th>
                    */}
                  </tr>
                </thead>
                <tbody>
                  {artifact.data_schema.map((colSpec, index) => (
                    <tr key={index}>
                      <td>
                        <div className="text-brand-darkblue whitespace-no-wrap">
                          {colSpec.name}
                        </div>
                      </td>
                      <td>
                        <div className="text-brand-darkblue whitespace-no-wrap">
                          {colSpec.type}
                        </div>
                      </td>
                      {/*
                      <td>
                        {colSpec.required ? "Yes" : "No"}
                      </td>
                      */}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <p></p>
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
                      <th>
                        Name
                      </th>
                      <th>
                        Value
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {artifact.hyperparameters.map((hyperparameter, index) => (
                      <tr key={index}>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {hyperparameter.name}
                          </div>
                        </td>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {hyperparameter.value}
                          </div>
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
                      <th>
                        Metric
                      </th>
                      <th>
                        Value
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {artifact.results.map((result, index) => (
                      <tr key={index}>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {result.metric}
                          </div>
                        </td>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {result.value}
                          </div>
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
                      <th>
                        Data Type
                      </th>
                      <th>
                        Shape
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {artifact.input_format.map((format, index) => (
                      <tr key={index}>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {format.tensor_spec.dtype}
                          </div>
                        </td>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {JSON.stringify(format.tensor_spec.shape)}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
              <p className="text-3xl p-1 pt-4 font-semibold mb-4 text-brand-tumdark">Output Format</p>
              <div className="w-1/2">
                <table className="leading-normal border w-full">
                  <thead>
                    <tr>
                      <th>
                        Data Type
                      </th>
                      <th>
                        Shape
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {/* @ts-ignore */}
                    {artifact.output_format.map((format, index) => (
                      <tr key={index}>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {format.tensor_spec.dtype}
                          </div>
                        </td>
                        <td>
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            {JSON.stringify(format.tensor_spec.shape)}
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          ) : (
            <p></p>
          )}
        </>
      )}
    </div>
  );
}
