'use client'
import React, { useCallback, useEffect, useState } from 'react';
import {
  ReactFlow,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
 
import '@xyflow/react/dist/style.css';

import { useRouter } from "next/navigation";
import { DataArtifactsService } from "@/lib/api/services/DataArtifactsService";
import { ConnectionsService } from '@/lib/api/services/ConnectionsService';
import type { ArtifactResponse } from '@/lib/api/models/ArtifactResponse';
import type { ConnectionResponse } from '@/lib/api/models/ConnectionResponse';

export default function PipelinePage({ params }: { params: { name: string } }) {
  const name = params.name;
  const [artifacts, setArtifacts] = useState<ArtifactResponse[]>([]);
  const [connections, setConnections] = useState<ConnectionResponse[]>([]);
  const router = useRouter();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Function to handle node click
  const handleNodeClick = (event: React.MouseEvent, node: any) => {
    const nodeId = node.id;
    router.push(`/artifacts/${nodeId}`);  // Navigate to the artifact route
  };

  // Helper function to perform topological sort (enabling DAGs)
  const topologicalSort = (nodesMap: Map<string, string[]>) => {
    const sortedNodes: string[] = [];
    const visited: Set<string> = new Set();
    const tempMark: Set<string> = new Set();
    const nodeLevels: Map<string, number> = new Map();

    const visit = (node: string, level: number) => {
      console.log(`Visiting node ${node} at level ${level}`); // Debugging
      const dependencies = nodesMap.get(node) || [];
      dependencies.forEach(dep => visit(dep, level + 1));
      if (!visited.has(node)) {
        visited.add(node);  // Mark as permanently visited
        sortedNodes.push(node);  // Add node to sorted result
      }
      nodeLevels.set(node, Math.max(level, nodeLevels.get(node) || 0));
    };

    nodesMap.forEach((_, node) => {
      if (!visited.has(node)) {
        visit(node, 0);
      }
    });

    return { sortedNodes, nodeLevels };
  };

  useEffect(() => {
    const fetchArtifacts = async () => {
      if (name) {
        try {
          const fetchedArtifacts = await DataArtifactsService.getArtifactsByPipelineDataArtifactsPipelinePipelineNameGet(name as string);
          setArtifacts(fetchedArtifacts);
          const fetchedConnections = await ConnectionsService.getConnectionsByPipelineConnectionsPipelinePipelineNameGet(name as string);
          setConnections(fetchedConnections);

          // Create a dependency map (each node gets assigned a list of source nodes)
          const nodeDependencies = new Map<string, string[]>();
          fetchedArtifacts.forEach(artifact => {
            nodeDependencies.set(artifact.name, []);
          });

          fetchedConnections.forEach(connection => {
            nodeDependencies.get(connection.target.name)?.push(connection.source.name);
          });

          console.log("Node Dependencies:", nodeDependencies); // Debugging

          // Perform topological sorting to get the ordered list of nodes and their levels
          const { sortedNodes, nodeLevels } = topologicalSort(nodeDependencies);

          console.log("Sorted Nodes:", sortedNodes); // Debugging
          console.log("Node Levels:", nodeLevels); // Debugging
          // get maximum level
          const maxLevel = Math.max(...Array.from(nodeLevels.values()));

          const levelHeight = 250; // Distance between levels
          const nodeHeight = 100;  // Distance between nodes at the same level

          const levelNodeCounts: Map<number, number> = new Map();

          const updatedNodes = sortedNodes.map((nodeName) => {
            const level = nodeLevels.get(nodeName) || 0;

            // Count nodes at this level to determine vertical positioning
            const yPos = levelNodeCounts.has(level)
              ? levelNodeCounts.get(level)! * nodeHeight
              : 0;

            // Update the count for this level
            levelNodeCounts.set(level, (levelNodeCounts.get(level) || 0) + 1);

            return {
              id: nodeName,
              data: { label: nodeName },
              position: { x: 100 + maxLevel * levelHeight - level * levelHeight, y: yPos + 100 }, // Correct horizontal spacing
              sourcePosition: 'right',
              targetPosition: 'left',
            };
          });
          setNodes(updatedNodes);

          const updatedEdges = fetchedConnections.map((connection) => ({
            id: connection.source.name + '-' + connection.target.name,
            source: connection.source.name,
            target: connection.target.name,
            markerEnd: {
              type: 'arrow',
              width: 20,  
              height: 20,
            },
          }));
          setEdges(updatedEdges);

        } catch (error) {
          console.error("Failed to fetch artifacts", error);
        }
      }
    };
    fetchArtifacts();
  }, [name, setNodes, setEdges]);

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onNodeClick={handleNodeClick}
      />
    </div>
    );
}
