"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/manual/format_date";
import { DatasetArtifact, getArtifactsArtifactsGet } from "@/lib/api";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faDatabase, faFileCode, faCircleNodes, faSliders, faSquarePollVertical } from '@fortawesome/free-solid-svg-icons';

export default function ArtifactsPage() {
  const [artifacts, setArtifacts] = useState<DatasetArtifact[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [artifactType, setArtifactType] = useState("");
  const router = useRouter();

  const artifactTypeMap: Record<string, { icon: any; label: string }> = {
    dataset: { icon: faDatabase, label: "Dataset" },
    code: { icon: faFileCode, label: "Code" },
    model: { icon: faCircleNodes, label: "Model" },
    hyperparameters: { icon: faSliders, label: "Hyperparameters" },
    parameters: { icon: faSliders, label: "Parameters" },
    results: { icon: faSquarePollVertical, label: "Results" },
  };

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
    <div className="p-5">
      <h1>Artifacts Overview</h1>

      {/* Search bar */}
      <div className="mt-5">
        <input
          type="text"
          placeholder="Search by name or description"
          className="w-full text-brand-darkblue bg-brand-linkhover p-2 border border-brand-linkhover rounded-md placeholder:text-brand-gray focus:outline-none focus:ring-brand-darkblue"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      {/* Artifact type dropdown filter */}
      <div className="mt-5 flex items-center space-x-2">
        <label className="text-brand-darkblue font-semibold p-2">Artifact Type:</label>{" "}
        {/* Label for dropdown */}
        <select
          className="dropdown w-1/8 text-brand-darkblue bg-brand-linkhover focus:outline-brand-darkblue"
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

      {/* Artifact table */}
      <section className="mb-8">
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th>
                    Name
                  </th>
                  <th>
                    Description
                  </th>
                  <th>
                    Artifact Type
                  </th>
                  <th>
                    File Type
                  </th>
                  <th>
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
                    <td>
                      <div className="text-brand-darkblue whitespace-no-wrap">
                        {artifact.name}
                      </div>
                    </td>
                    <td>
                      <div className="text-brand-darkblue whitespace-no-wrap">
                        {artifact.description}
                      </div>
                    </td>
                    <td>
                      {artifact.artifact_type && artifactTypeMap[artifact.artifact_type] && (
                        <div className="flex w-full items-center">
                          <div className="text-brand-darkblue whitespace-no-wrap">
                            <FontAwesomeIcon icon={artifactTypeMap[artifact.artifact_type].icon} className="text-brand-darkblue" size="2x" />
                          </div>
                          <div className="text-ms text-brand-darkblue pl-2">
                            {artifactTypeMap[artifact.artifact_type].label}
                          </div>
                        </div>
                      )}
                    </td>
                    <td>
                      <div className="text-brand-darkblue whitespace-no-wrap">
                      {artifact.file_type}
                      </div>
                    </td>
                    <td>
                      <div className="text-brand-darkblue whitespace-no-wrap">
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
