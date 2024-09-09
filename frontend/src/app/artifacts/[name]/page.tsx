"use client";

import { useEffect, useState } from "react";
import { DataArtifactService } from "@/lib/api/services/DataArtifactService";
import type { DataArtifactPandas } from "@/lib/api/models/DataArtifactPandas";

export default function ArtifactDetailPage({ params }: { params: { name: string } }) {
  // Get the artifact name from the URL
  const name = params.name;
  const [artifact, setArtifact] = useState<DataArtifactPandas | null>(null);

  useEffect(() => {
    const fetchArtifactDetails = async () => {
      console.log(name)
      if (name) {
        try {
          // Assuming there is an API to fetch a single artifact by name
          const response = await DataArtifactService.getArtifactByNameDataArtifactNameGet(name as string);
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

  console.log(name)

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
      <p>Description: {artifact.description}</p>
      <p>Dataset Type: {artifact.dataset_type}</p>
      <p>Created At: {formatDate(artifact.created_at)}</p>
      {artifact.num_rows ? (
        <p>Number of Rows: {artifact.num_rows}</p>
      ) : (
        <p>Number of Rows: not available</p>
      )}
      {artifact.num_columns ? (
        <p>Number of Columns: {artifact.num_columns}</p>
      ) : (
        <p>Number of Columns: not available</p>
      )}

      {/* Schema Table */}
      <h2>Dataset Schema</h2>
      {artifact.schema && artifact.schema.length > 0 ? (
        <div className="overflow-x-auto">
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
              {artifact.schema.map((colSpec, index) => (
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
