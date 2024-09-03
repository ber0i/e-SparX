"use client";

import { useEffect, useState } from "react";
import { RegisterService } from "@/lib/api/services/RegisterService";
import type { DataArtifact } from "@/lib/api/models/DataArtifact";

export default function ArtifactsPage() {
  const [Artifacts, setArtifacts] = useState<DataArtifact[]>([]);

  useEffect(() => {
    const fetchArtifacts = async () => {
      try {
        const response = await RegisterService.viewArtifactsRegisterGet();
        setArtifacts(response.entries);
      } catch (error) {
        console.error("Failed to fetch datasets", error);
      }
    };

    fetchArtifacts();
  }, []);

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
                </tr>
              </thead>
              <tbody>
                {Artifacts.map((artifact) => (
                  <tr key={artifact.name}>
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
