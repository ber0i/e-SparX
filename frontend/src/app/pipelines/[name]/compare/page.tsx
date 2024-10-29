"use client";
import { Bar } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { useEffect, useState } from "react";
import { getResultsArtifactsByPipelineResultsArtifactsPipelinePipelineNameGet } from "@/lib/api";

// Register chart.js components
ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
);

export default function ArtifactDetailPage({
  params,
}: {
  params: { name: string };
}) {
  // Get the pipeline name from the URL
  const name = params.name;

  const [resultsartifactsnames, setResultsartifactsnames] = useState<string[]>(
    [],
  );
  const [metrics, setMetrics] = useState<string[]>([]);
  const [valuelists, setValuelists] = useState<number[][]>([]);

  // define color list for the chart
  const colorList = [
    "rgb(63, 161, 241, 0.6)",
    "rgb(12, 167, 137, 0.6)",
    "rgba(255, 159, 64, 0.6)",
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
    "rgba(255, 206, 86, 0.6)",
    "rgba(75, 192, 192, 0.6)",
    "rgba(153, 102, 255, 0.6)",
    "rgba(255, 159, 64, 0.6)",
    "rgba(255, 99, 132, 0.6)",
    "rgba(54, 162, 235, 0.6)",
    "rgba(255, 206, 86, 0.6)",
  ];

  useEffect(() => {
    // Fetch results artifacts by pipeline
    const fetchResults = async () => {
      if (name) {
        const { error, data } =
          await getResultsArtifactsByPipelineResultsArtifactsPipelinePipelineNameGet(
            { path: { pipeline_name: name } },
          );

        if (error) {
          console.error("Failed to fetch artifact details", error);
          return;
        }

        setResultsartifactsnames(
          (data as { results_artifacts_names: string[] })
            .results_artifacts_names,
        );
        setMetrics((data as { results_metrics: string[] }).results_metrics);
        setValuelists((data as { results_values: number[][] }).results_values);
      }
    };

    fetchResults();
  }, [name]);

  if (!resultsartifactsnames) {
    return <div>Loading...</div>;
  }

  const data = {
    labels: resultsartifactsnames,
    datasets: metrics.map((metric, index) => ({
      label: metric,
      data: valuelists[index],
      backgroundColor: colorList[index],
      borderColor: colorList[index],
      borderWidth: 1,
    })),
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: "top",
      },
    },
    scales: {
      x: {
        type: "category",
      },
      y: {
        beginAtZero: true,
        ticks: {
          stepSize: 0.01,
        },
      },
    },
  };

  return (
    <div style={{ width: "100%", height: "500px", padding: "0 80px" }}>
      <h1>Model Error Metrics</h1>
      {/* @ts-ignore */}
      <Bar data={data} options={options} />
    </div>
  );
}
