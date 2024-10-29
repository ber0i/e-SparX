"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { formatDate } from "@/lib/manual/format_date";
import { DataArtifact, getArtifactsDataArtifactsGet } from "@/lib/api";

export default function ArtifactsPage() {
  const [Artifacts, setArtifacts] = useState<DataArtifact[]>([]);
  const router = useRouter();

  useEffect(() => {
    // Fetch all artifacts
    const fetchArtifacts = async () => {
      const { error, data } = await getArtifactsDataArtifactsGet();

      if (error) {
        console.error("Failed to fetch datasets", error);
        return;
      }

      setArtifacts((data as { entries: DataArtifact[] }).entries);
    };

    fetchArtifacts();
  }, []);

  // Handler to navigate to the artifact details page
  const handleRowClick = (name: string) => {
    router.push(`/artifacts/${name}`); // Navigate to /artifacts/[name]
  };

  return (
    <div className="p-5 ">
      <h1>Artifacts Overview</h1>

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
                    Created At
                  </th>
                </tr>
              </thead>
              <tbody>
                {Artifacts.map((artifact) => (
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
