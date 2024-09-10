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
import { DataArtifactService } from "@/lib/api/services/DataArtifactService";
import type { ArtifactResponse } from '@/lib/api/models/ArtifactResponse';

export default function TestPage() {
  const [artifacts, setArtifacts] = useState<ArtifactResponse[]>([]);
  const router = useRouter();

  useEffect(() => {
    const fetchArtifacts = async () => {
      try {
        const artifacts = await DataArtifactService.getArtifactsByPipelineDataArtifactPipelinePipelineNameGet("p2");
        setArtifacts(artifacts);
      } catch (error) {
        console.error("Failed to fetch datasets", error);
      }
    };

    fetchArtifacts();
  }, []);

  const nodes = artifacts.map((artifact, index) => ({
    id: artifact.name,
    data: { label: artifact.name },
    position: { x: 100 + 250 * index, y: 100 },  // You can adjust the positioning logic
  }));

  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={[]}
      />
    </div>
    );}