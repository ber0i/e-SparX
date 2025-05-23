import type { Node, Position } from "@xyflow/react";

export const legendNodes: Node[] = [
    {
      id: "1",
      position: { x: 100, y: 0 },
      data: { label: "Dataset" },
      style: { backgroundColor: "rgb(63, 161, 241)" },
      sourcePosition: 'right' as Position,
      targetPosition: 'left' as Position,
      draggable: false,
      selectable: false,
      connectable: false,
    },
    {
      id: "2",
      position: { x: 100 + 1 * 180, y: 0 },
      data: { label: "Code" },
      style: { backgroundColor: "gray", color: "white" },
      sourcePosition: 'right' as Position,
      targetPosition: 'left' as Position,
      draggable: false,
      selectable: false,
      connectable: false,
    },
    {
      id: "3",
      position: { x: 100 + 2 * 180, y: 0 },
      data: { label: "Model" },
      style: { backgroundColor: "rgb(12, 167, 137)" },
      sourcePosition: 'right' as Position,
      targetPosition: 'left' as Position,
      draggable: false,
      selectable: false,
      connectable: false,
    },
    {
      id: "4",
      position: { x: 100 + 3 * 180, y: 0 },
      data: { label: "(Hyper-)Parameters" },
      style: { backgroundColor: "rgba(12, 167, 137, 0.6)" },
      sourcePosition: 'right' as Position,
      targetPosition: 'left' as Position,
      draggable: false,
      selectable: false,
      connectable: false,
    },
    {
      id: "5",
      position: { x: 100 + 4 * 180, y: 0 },
      data: { label: "Results" },
      style: { backgroundColor: "rgba(8, 102, 84, 0.8)", color: "white" },
      sourcePosition: 'right' as Position,
      targetPosition: 'left' as Position,
      draggable: false,
      selectable: false,
      connectable: false,
    },
  ];