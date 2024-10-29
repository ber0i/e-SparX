// TODO: This page renders the DAG legend. Should be displayed nicely on the pipeline/[name] page at some point.

import React from "react";
import { ReactFlow } from "@xyflow/react";

import "@xyflow/react/dist/style.css";

const initialNodes = [
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

export default function App() {
  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      {/* @ts-ignore */}
      <ReactFlow nodes={initialNodes} edges={[]} />
    </div>
  );
}
