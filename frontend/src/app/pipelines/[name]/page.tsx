"use client";

import React from "react";
import { ReactFlow, useNodesState, useEdgesState } from "@xyflow/react";
import { useRouter, usePathname } from "next/navigation";
import Image from "next/image";
import DagLegend from "../../daglegend.svg";

import "@xyflow/react/dist/style.css";

import { useEffect, useState } from "react";
import { topologicalSort } from "@/lib/manual/topological_sort";
import { getNodeStyle } from "@/lib/manual/get_node_style";
import {
  ArtifactResponse,
  ConnectionResponse,
  getArtifactsByPipelineArtifactsPipelinePipelineNameGet,
  getConnectionsByPipelineConnectionsPipelinePipelineNameGet,
} from "@/lib/api";

// Define the DAG component
const DAGFlow = ({ name }: { name: string }) => {
  const [artifacts, setArtifacts] = useState<ArtifactResponse[]>([]);
  const [connections, setConnections] = useState<ConnectionResponse[]>([]);
  const router = useRouter();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Function to handle node click
  const handleNodeClick = (event: React.MouseEvent, node: any) => {
    const nodeId = node.id;
    router.push(`/artifacts/${nodeId}`); // Navigate to the artifact route
  };

  useEffect(() => {
    const fetchArtifacts = async () => {
      if (name) {
        try {
          // Fetch artifacts and connections by pipeline name
          const { error: fetchArtifactsError, data: fetchedArtifacts } =
            await getArtifactsByPipelineArtifactsPipelinePipelineNameGet({
              path: { pipeline_name: name },
            });

          if (fetchArtifactsError) {
            console.error("Unable to fetch Artifacts", fetchArtifactsError);
            return;
          }

          console.log(fetchedArtifacts);
          setArtifacts(fetchedArtifacts as ArtifactResponse[]);

          const { error: fetchConnectionsError, data: fetchedConnections } =
            await getConnectionsByPipelineConnectionsPipelinePipelineNameGet({
              path: { pipeline_name: name },
            });

          if (fetchConnectionsError) {
            console.error("Unable to fetch Connections", fetchConnectionsError);
            return;
          }

          setConnections(fetchedConnections);

          // Create a dependency map
          const nodeDependencies = new Map<string, string[]>();
          fetchedArtifacts.forEach((artifact) => {
            nodeDependencies.set(artifact.name, []);
          });

          fetchedConnections.forEach((connection) => {
            nodeDependencies
              .get(connection.target.name)
              ?.push(connection.source.name);
          });

          // Perform topological sorting to get the ordered list of nodes
          const { sortedNodes, nodeLevels } = topologicalSort(nodeDependencies);

          // Get maximum node level (for positioning)
          const maxLevel = Math.max(...Array.from(nodeLevels.values()));

          const levelNodeCounts: Map<number, number> = new Map(); // Initialize the map to track node counts at each level

          // Set node positions based on the topological sort
          const updatedNodes = sortedNodes.map((nodeName) => {
            const level = nodeLevels.get(nodeName) || 0;
            const artifact_type =
              fetchedArtifacts.find((artifact) => artifact.name === nodeName)
                ?.artifact_type || "unknown";

            // Initialize the node count for this level if it doesn't exist
            if (!levelNodeCounts.has(level)) {
              levelNodeCounts.set(level, 0);
            }

            // Calculate the vertical position based on how many nodes are already placed at this level
            const yPos = levelNodeCounts.get(level)! * 100; // Vertical distance between nodes at the same level

            // Increment the count for this level
            levelNodeCounts.set(level, levelNodeCounts.get(level)! + 1);

            return {
              id: nodeName,
              data: { label: nodeName },
              position: {
                x: 100 + maxLevel * 250 - level * 250,
                y: 100 + yPos,
              }, // Horizontal position by level, vertical by node count at the level
              sourcePosition: "right",
              targetPosition: "left",
              style: getNodeStyle(artifact_type),
            };
          });
          {
            /* @ts-ignore */
            setNodes(updatedNodes);
          }

          // Set edges based on fetched connections
          const updatedEdges = fetchedConnections.map((connection) => ({
            id: connection.source.name + "-" + connection.target.name,
            source: connection.source.name,
            target: connection.target.name,
            markerEnd: {
              type: "arrow",
              width: 20,
              height: 20,
            },
          }));
          {
            /* @ts-ignore */
            setEdges(updatedEdges);
          }
        } catch (error) {
          console.error("Failed to fetch artifacts", error);
        }
      }
    };

    fetchArtifacts();
  }, [name, setNodes, setEdges]);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
      />
    </div>
  );
};

export default function PipelinePage({ params }: { params: { name: string } }) {
  const router = useRouter();
  const pathname = usePathname();

  // Function to handle button click
  const handleCompareClick = () => {
    router.push(`${pathname}/compare`); // Navigate to the compare page
  };

  const name = params.name;

  const legendNodes = [
    {
      id: "1",
      position: { x: 100, y: 0 },
      data: { label: "Dataset" },
      style: { backgroundColor: "rgb(63, 161, 241)" },
      sourcePosition: "right",
      targetPosition: "left",
    },
    {
      id: "2",
      position: { x: 100 + 1 * 180, y: 0 },
      data: { label: "Code" },
      style: { backgroundColor: "gray", color: "white" },
      sourcePosition: "right",
      targetPosition: "left",
    },
    {
      id: "3",
      position: { x: 100 + 2 * 180, y: 0 },
      data: { label: "Model" },
      style: { backgroundColor: "rgb(12, 167, 137)" },
      sourcePosition: "right",
      targetPosition: "left",
    },
    {
      id: "4",
      position: { x: 100 + 3 * 180, y: 0 },
      data: { label: "(Hyper-)Parameters" },
      style: { backgroundColor: "rgba(12, 167, 137, 0.6)" },
      sourcePosition: "right",
      targetPosition: "left",
    },
    {
      id: "5",
      position: { x: 100 + 4 * 180, y: 0 },
      data: { label: "Results" },
      style: { backgroundColor: "rgba(8, 102, 84, 0.8)", color: "white" },
      sourcePosition: "right",
      targetPosition: "left",
    },
  ];

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      {/* TODO: Remove image once you have a better solution */}
      <div style={{ marginLeft: "100px" }}>
        <Image
          src={DagLegend}
          alt="DAG Legend"
          width={229 * 2.5}
          height={30 * 2.5}
          layout="fixed"
        />
      </div>
      <div style={{ position: "absolute", top: "110px", right: "200px" }}>
        <button
          onClick={handleCompareClick}
          style={{
            padding: "10px 20px",
            fontSize: "16px",
            cursor: "pointer",
            backgroundColor: "rgba(8, 102, 84, 0.8)", // Dark green background
            color: "#ffffff", // White text
            border: "none",
            borderRadius: "5px", // Optional: rounded corners
            transition: "background-color 0.3s", // Optional: smooth transition for hover effect
          }}
          onMouseEnter={(e) =>
            (e.currentTarget.style.backgroundColor = "#007f00")
          } // Lighter green on hover
          onMouseLeave={(e) =>
            (e.currentTarget.style.backgroundColor = "#005f00")
          } // Revert to dark green
        >
          Compare Results
        </button>
      </div>
      {/* TODO: The legend is not displaying nicely, there is a huge space underneath */}
      {/* <ReactFlow nodes={legendNodes} edges={[]} style={{ height: 'mincontent' }} /> */}
      <DAGFlow name={name} />
    </div>
  );
}
