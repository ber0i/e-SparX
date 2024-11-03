"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import type { Pipeline } from "@/lib/manual/pipeline";
import { getPipelinesPipelinesGet } from "@/lib/api";

export default function PipelinesPage() {
  const [pipelines, setPipelines] = useState<Pipeline[]>([]);
  const [searchTerm, setSearchTerm] = useState("");
  const router = useRouter();

  useEffect(() => {
    // Fetch all pipelines
    const fetchPipelines = async () => {
      const { error, data } = await getPipelinesPipelinesGet();

      if (error) {
        console.error("Failed to fetch pipelines", error);
        return;
      }

      setPipelines(data as Pipeline[]);
    };

    fetchPipelines();
  }, []);

  // Handler to navigate to the artifact details page
  const handleRowClick = (name: string) => {
    router.push(`/pipelines/${name}`); // Navigate to /pipelines/[name]
  };

  // Filter artifacts based on search term
  const filteredPipelines = pipelines.filter((pipeline: Pipeline) =>
    pipeline.name.toLowerCase().includes(searchTerm.toLowerCase()),
  );

  return (
    <div className="p-5 ">
      <h1>Pipelines Overview</h1>

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

      <section className="mb-8">
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                  <th className="px-5 py-3 border-b-2 border-brand-smoke bg-accent text-left text-xs font-semibold text-contrast uppercase tracking-wider ">
                    Name
                  </th>
                </tr>
              </thead>
              <tbody>
                {filteredPipelines.map((pipeline: Pipeline) => (
                  <tr
                    key={pipeline.name}
                    className="cursor-pointer"
                    onClick={() => handleRowClick(pipeline.name)}
                  >
                    <td className="px-5 py-5 border-b border-brand-smoke bg-canvas text-sm dark:bg-accent dark:border-primary">
                      <div className="text-contrast whitespace-no-wrap">
                        {pipeline.name}
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
