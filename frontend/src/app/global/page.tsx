"use client";
import React, { useEffect, useState } from "react";
import Image from "next/image";
import { useRouter } from "next/navigation";
import { ReactFlow, useNodesState, useEdgesState } from "@xyflow/react";
import DagLegend from "../daglegend.svg";

import "@xyflow/react/dist/style.css";

import { topologicalSort } from "@/lib/manual/topological_sort";
import { getNodeStyle } from "@/lib/manual/get_node_style";
import {
  ArtifactResponse,
  ConnectionResponse,
  getArtifactsForGlobalViewDataArtifactsGlobalGet,
  getConnectionsConnectionsGet,
} from "@/lib/api";

// Define the DAG component
const DAGFlow = () => {
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
      // Fetch all artifacts and connections
      const { error: fetchArtifactsError, data: fetchedArtifacts } =
        await getArtifactsForGlobalViewDataArtifactsGlobalGet();

      if (fetchArtifactsError) {
        console.error("Failed to fetch Artifacts", fetchArtifactsError);
        return;
      }

      console.log(fetchedArtifacts);
      setArtifacts(fetchedArtifacts as ArtifactResponse[]);

      const { error: fetchConnectionsError, data: fetchedConnections } =
        await getConnectionsConnectionsGet();
      if (fetchConnectionsError) {
        console.error("Failed to fetch Connections", fetchConnectionsError);
      }
      setConnections(fetchedConnections as ConnectionResponse[]);

      // Create a dependency map
      const nodeDependencies = new Map<string, string[]>();

      // ! is needed as ts thinks the variable can be undefined due to inconsistent generation of the OpenAPI schema
      fetchedArtifacts!.forEach((artifact) => {
        nodeDependencies.set(artifact.name, []);
      });

      // ! is needed as ts thinks the variable can be undefined due to inconsistent generation of the OpenAPI schema
      fetchedConnections!.forEach((connection) => {
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

        // ! is needed as ts thinks the variable can be undefined due to inconsistent generation of the OpenAPI schema
        const artifact_type =
          fetchedArtifacts!.find((artifact) => artifact.name === nodeName)
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
          position: { x: 100 + maxLevel * 250 - level * 250, y: 100 + yPos }, // Horizontal position by level, vertical by node count at the level
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
      // ! is needed as ts thinks the variable can be undefined due to inconsistent generation of the OpenAPI schema
      const updatedEdges = fetchedConnections!.map((connection) => ({
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
    };

    fetchArtifacts();
  }, [setNodes, setEdges]);

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

export default function GlobalPage() {
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      <div style={{ marginLeft: "100px" }}>
        <Image
          src={DagLegend}
          alt="DAG Legend"
          width={229 * 2.5}
          height={30 * 2.5}
          layout="fixed"
        />
      </div>
      <DAGFlow />
    </div>
  );
}
