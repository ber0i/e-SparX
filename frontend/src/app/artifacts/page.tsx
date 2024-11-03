"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/manual/format_date";
import { DatasetArtifact, getArtifactsArtifactsGet } from "@/lib/api";

export default function ArtifactsPage() {
  const [artifacts, setArtifacts] = useState<DatasetArtifact[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [artifactType, setArtifactType] = useState("");
  const router = useRouter();

  useEffect(() => {
    // Fetch all artifacts
    const fetchArtifacts = async () => {
      const { error, data } = await getArtifactsArtifactsGet();

      if (error) {
        console.error("Failed to fetch datasets", error);
        return;
      }

      setArtifacts((data as { entries: DatasetArtifact[] }).entries);
    };

    fetchArtifacts();
  }, []);

  // Handler to navigate to the artifact details page
  const handleRowClick = (name: string) => {
    router.push(`/artifacts/${name}`); // Navigate to /artifacts/[name]
  };

  // Filter artifacts based on search term
  const filteredArtifacts = artifacts.filter(
    (artifact: DatasetArtifact) =>
      (artifact.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        artifact.description
          .toLowerCase()
          .includes(searchTerm.toLowerCase())) &&
      (artifactType === "" || artifact.artifact_type === artifactType),
  );

  return (
    <div className="p-5 ">
      <h1>Artifacts Overview</h1>

      {/* Search bar */}
      <div className="mt-5">
        <input
          type="text"
          placeholder="Search by name or description"
          className="w-full p-2 border border-brand-smoke rounded-md"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Artifact type dropdown filter */}
      <div className="mt-5 flex items-center space-x-2">
        <label className="text-contrast w-32">Artifact Type:</label>{" "}
        {/* Label for dropdown */}
        <select
          className="dropdown w-1/8"
          value={artifactType}
          onChange={(e) => setArtifactType(e.target.value)}
        >
          <option value="">all</option>
          <option value="dataset">dataset</option>
          <option value="code">code</option>
          <option value="hyperparameters">hyperparameters</option>
          <option value="model">model</option>
          <option value="results">results</option>
          <option value="parameters">parameters</option>
        </select>
      </div>

      <section className="mb-8">
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Name
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Description
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Artifact Type
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    File Type
                  </th>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Created/Updated At
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredArtifacts.map((artifact: DatasetArtifact) => (
                  <tr
                    key={artifact.name}
                    className="cursor-pointer"
                    onClick={() => handleRowClick(artifact.name)}
                  >
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {artifact.name}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {artifact.description}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {artifact.artifact_type}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {artifact.file_type}
                      </div>
                    </td>
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {formatDate(artifact.created_at)}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </div>
  );
}
