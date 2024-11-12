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
    <div className="p-5">
      <h1>Pipelines Overview</h1>

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

      <section className="mb-8">
        <div className="-mx-4 sm:-mx-8 px-4 sm:px-8 py-4 overflow-x-auto">
          <div className="inline-block min-w-full shadow rounded-lg overflow-hidden">
            <table className="min-w-full leading-normal">
              <thead>
                <tr>
                <th>
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
                    <td>
                      <div className="text-brand-darkblue whitespace-no-wrap">
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
