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
 
const initialNodes = [
  {
    id: 'Freedom',
    sourcePosition: 'right',
    type: 'input',
    data: { label: 'Freedom' },
    position: { x: 100, y: 100 },
  },
  {
    id: 'Kelmarsh SCADA Data',
    sourcePosition: 'right',
    targetPosition: 'left',
    data: { label: 'Kelmarsh SCADA Data' },
    position: { x: 350, y: 100 },
  },
];
const initialEdges = [{ id: 'e1-2', source: 'Freedom', target: 'Kelmarsh SCADA Data' }];
 
export default function App() {
  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);
 
  const onConnect = useCallback(
    (params: Connection) => setEdges((eds) => addEdge(params, eds)),
    [setEdges],
  );
 
  return (
    <div style={{ width: '100vw', height: '100vh' }}>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        onConnect={onConnect}
      />
    </div>
  );
}
