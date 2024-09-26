'use client'
import React, { useCallback } from 'react';
import {
  ReactFlow,
  addEdge,
  Connection,
  useNodesState,
  useEdgesState,
} from '@xyflow/react';
 
import '@xyflow/react/dist/style.css';

import { useEffect, useState } from "react";
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

    const visit = (node: string, level: number, inLoop: boolean) => {
      if (tempMark.has(node)) return; // Ignore temporary marked nodes (prevents cycles)
      if (!visited.has(node) || inLoop) {
        tempMark.add(node);  // Mark the node temporarily
        const dependencies = nodesMap.get(node) || [];
        dependencies.forEach(dep => visit(dep, level + 1, true));
        if (!visited.has(node)) {
            visited.add(node);  // Mark as permanently visited
            sortedNodes.push(node);  // Add node to sorted result
        }
        tempMark.delete(node);
        nodeLevels.set(node, Math.max(level, nodeLevels.get(node) || 0));
      }
    };

    nodesMap.forEach((_, node) => {
      if (!visited.has(node)) {
        visit(node, 0, false);
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

          // Create a dependency map
          const nodeDependencies = new Map<string, string[]>();
          fetchedArtifacts.forEach(artifact => {
            nodeDependencies.set(artifact.name, []);
          });

          fetchedConnections.forEach(connection => {
            nodeDependencies.get(connection.target.name)?.push(connection.source.name);
          });

          // Perform topological sorting to get the ordered list of nodes
          const { sortedNodes, nodeLevels } = topologicalSort(nodeDependencies);

          // get maximum level
          const maxLevel = Math.max(...Array.from(nodeLevels.values()));

          const getNodeStyle = (artifact_type: string) => {
            if (artifact_type === 'dataset') {
              return { backgroundColor: 'rgb(63, 161, 241)' };  // Blue background, black text
            }
            if (artifact_type === 'code') {
              return { backgroundColor: 'gray', color: 'white' };  // Gray background, white text
            }
            if (artifact_type === 'model') {
              return { backgroundColor: 'rgb(12, 167, 137)', color: 'black' };  // Green background, white text
            }
            if (artifact_type === 'hyperparameters') {
              return { backgroundColor: 'rgba(12, 167, 137, 0.6)' };  // White background, black text
            }
            if (artifact_type === 'parameters') {
              return { backgroundColor: 'rgba(12, 167, 137, 0.6)' };  // White background, black text
            }
            return { backgroundColor: 'white' };  // White background, black text
          };

          const levelNodeCounts: Map<number, number> = new Map(); // Initialize the map to track node counts at each level

          const updatedNodes = sortedNodes.map((nodeName) => {
            const level = nodeLevels.get(nodeName) || 0;
            const artifact_type = fetchedArtifacts.find(artifact => artifact.name === nodeName)?.artifact_type || 'unknown';

            // Initialize the node count for this level if it doesn't exist
            if (!levelNodeCounts.has(level)) {
            levelNodeCounts.set(level, 0);
            }

            // Calculate the vertical position based on how many nodes are already placed at this level
            const yPos = levelNodeCounts.get(level)! * 100;  // Vertical distance between nodes at the same level

            // Increment the count for this level
            levelNodeCounts.set(level, levelNodeCounts.get(level)! + 1);

            return {
              id: nodeName,
              data: { label: nodeName },
              position: { x: 100 + maxLevel * 250 - level * 250, y: 100 + yPos },  // Horizontal position by level, vertical by node count at the level
              sourcePosition: 'right',
              targetPosition: 'left',
              style: getNodeStyle(artifact_type),
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
    );}