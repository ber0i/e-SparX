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

    const visit = (node: string) => {
      if (tempMark.has(node)) return; // Ignore temporary marked nodes (prevents cycles)
      if (!visited.has(node)) {
        tempMark.add(node);  // Mark the node temporarily
        const dependencies = nodesMap.get(node) || [];
        dependencies.forEach(visit);
        visited.add(node);  // Mark as permanently visited
        tempMark.delete(node);
        sortedNodes.push(node);  // Add node to sorted result
      }
    };

    nodesMap.forEach((_, node) => {
      if (!visited.has(node)) {
        visit(node);
      }
    });

    return sortedNodes;
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
          const sortedNodeNames = topologicalSort(nodeDependencies);

          const updatedNodes = sortedNodeNames.map((nodeName, index) => ({
            id: nodeName,
            data: { label: nodeName },
            position: { x: 100 + 250 * index, y: 100 },
            sourcePosition: 'right',
            targetPosition: 'left',
          }));
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