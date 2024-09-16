"use client";

import { useEffect, useState } from "react";
import { DataArtifactsService } from "@/lib/api/services/DataArtifactsService";
import type { DataArtifact } from "@/lib/api/models/DataArtifact";

export default function ArtifactDetailPage({ params }: { params: { name: string } }) {
  // Get the artifact name from the URL
  const name = params.name;
  const [artifact, setArtifact] = useState<DataArtifact | null>(null);

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
    fetchArtifactDetails();
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

        <p className="key">Dataset Type:</p>
        <p className="value">{artifact.dataset_type}</p>

        <p className="key">Created At:</p>
        <p className="value">{formatDate(artifact.created_at)}</p>

        <p className="key">URL to Artifact Source:</p>
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

        <p className="key">Number of Rows:</p>
        <p className="value">{artifact.num_rows ? artifact.num_rows : "not available"}</p>

        <p className="key">Number of Columns:</p>
        <p className="value">{artifact.num_columns ? artifact.num_columns : "not available"}</p>
      </div>
      
      {artifact.data_schema && artifact.data_schema.length > 0 ? (
        <div className="overflow-x-auto">
          <h2>Dataset Schema</h2>
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
    </div>
  );
}
