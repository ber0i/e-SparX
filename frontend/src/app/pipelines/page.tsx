"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { PipelinesService } from "@/lib/api/services/PipelinesService";
import type { Pipeline } from "@/lib/manual/pipeline";


export default function PipelinesPage() {

  const [Pipelines, setPipelines] = useState<Pipeline[]>([]);
  const router = useRouter();

  useEffect(() => {

    // Fetch all pipelines
    const fetchPipelines = async () => {
      try {
        const response = await PipelinesService.getPipelinesPipelinesGet();
        setPipelines(response);
      } catch (error) {
        console.error("Failed to fetch pipelines", error);
      }
    };

    fetchPipelines();
  }, []);

  // Handler to navigate to the artifact details page
  const handleRowClick = (name: string) => {
    router.push(`/pipelines/${name}`);  // Navigate to /pipelines/[name]
  };

  return (
    <div className="p-5 ">

      <h1>Pipelines Overview</h1>
      
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
                {Pipelines.map((pipeline) => (
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
