"use client";
import React, { useEffect, useState, memo } from "react";
import {
  ReactFlow,
  useNodesState,
  useEdgesState,
  Handle,
  Position,
  Node,
} from "@xyflow/react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faDatabase,
  faFileCode,
  faCircleNodes,
  faSliders,
  faSquarePollVertical,
  faAngleLeft,
  faAngleRight,
} from "@fortawesome/free-solid-svg-icons";
import { useRouter } from "next/navigation";
import Button from "@/components/Button";
import ArtifactNode from "@/components/ArtifactNode";
import { topologicalSort } from "@/lib/manual/topological_sort";
import {
  ArtifactResponse,
  ConnectionResponse,
  getArtifactsForGlobalViewArtifactsGlobalGet,
  getConnectionsConnectionsGet,
  getPipelinesByArtifactPipelinesArtifactArtifactNameGet,
  getPipelinesPipelinesGet,
} from "@/lib/api";

import "@xyflow/react/dist/base.css";
import "../../../tailwind.config";

const nodeTypes = {
  custom: memo(ArtifactNode),
};

// Define the DAG component
const DAGFlow = () => {
  const [artifacts, setArtifacts] = useState<ArtifactResponse[]>([]);
  const [connections, setConnections] = useState<ConnectionResponse[]>([]);
  const [pipelines, setPipelines] = useState<{ [key: string]: number }>({});
  const router = useRouter();
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);

  // Function to handle node click
  const handleNodeClick = (
    event: React.MouseEvent,
    node: any,
  ) => {
    // Ensure click on pipeline badge behaves consistently in different browsers
    if (event.target instanceof HTMLElement && event.target.nodeName !== "DIV") {
      return;
    }

    const nodeId = node.id;
    router.push(`/artifacts/${nodeId}`); // Navigate to the artifact route
  };

  useEffect(() => {
    const fetchArtifacts = async () => {
      // Fetch pipelines
      const { error: fetchPipelineError, data: fetchedPipelines } =
        await getPipelinesPipelinesGet();

      if (fetchPipelineError) {
        console.error("Unable to fetch Pipelines", fetchPipelineError);
        return;
      }

      const pipelineMap = (
        fetchedPipelines as { id: number; name: string }[]
      ).reduce(
        (map, cur, idx) => {
          map[cur.name] = idx;
          return map;
        },
        {} as { [key: string]: number },
      );
      setPipelines(pipelineMap);

      // Fetch all artifacts and connections
      const { error: fetchArtifactsError, data: fetchedArtifacts } =
        await getArtifactsForGlobalViewArtifactsGlobalGet();

      if (fetchArtifactsError) {
        console.error("Failed to fetch Artifacts", fetchArtifactsError);
        return;
      }

      setArtifacts(fetchedArtifacts as ArtifactResponse[]);

      const { error: fetchConnectionsError, data: fetchedConnections } =
        await getConnectionsConnectionsGet();
      if (fetchConnectionsError) {
        console.error("Failed to fetch Connections", fetchConnectionsError);
        return;
      }
      setConnections(fetchedConnections as ConnectionResponse[]);

      // Create a dependency map
      const nodeDependencies = new Map<string, string[]>();

      fetchedArtifacts!.forEach((artifact) => {
        nodeDependencies.set(artifact.name, []);
      });

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
      const updatedNodes = await Promise.all(
        sortedNodes.map(async (nodeName) => {
          const artifact = fetchedArtifacts?.find(
            (artifact) => artifact.name === nodeName,
          );

          let pipeline_idx: { idx: number; name: string }[] = [];
          if (artifact) {
            const {
              error: artifactPipelinesErr,
              data: fetchArtifactPipelines,
            } = await getPipelinesByArtifactPipelinesArtifactArtifactNameGet({
              path: { artifact_name: artifact.name },
            });

            if (!artifactPipelinesErr) {
              pipeline_idx = (
                fetchArtifactPipelines as { id: number; name: string }[]
              ).map((val) => ({
                idx: pipelineMap[val.name],
                name: val.name,
              }));
            }
          }
          const level = nodeLevels.get(nodeName) || 0;

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
            type: "custom",
            data: {
              name: nodeName,
              artifact_type: artifact_type,
              pipelines: pipeline_idx,
            },
            position: {
              x: 100 + maxLevel * 250 - level * 250,
              y: 100 + yPos,
            }, // Horizontal position by level, vertical by node count at the level
          };
        }),
      );

      {
        /* @ts-ignore */
        setNodes(updatedNodes);
      }

      // Set edges based on fetched connections
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
        nodeTypes={nodeTypes}
      />
    </div>
  );
};

const initLegendNodes: Node[] = [
  {
    id: "1",
    type: "custom",
    data: {
      name: "Dataset",
      artifact_type: "dataset",
      color: "bg-brand-tumblue",
    },
    position: { x: 100, y: 0 },
    draggable: false,
    selectable: false,
    connectable: false,
  },
  {
    id: "2",
    type: "custom",
    data: { name: "Code", artifact_type: "code" },
    position: { x: 100 + 1 * 225, y: 0 },
    draggable: false,
    selectable: false,
    connectable: false,
  },
  {
    id: "3",
    type: "custom",
    data: { name: "Model", artifact_type: "model" },
    position: { x: 100 + 2 * 225, y: 0 },
    draggable: false,
    selectable: false,
    connectable: false,
  },
  {
    id: "4",
    type: "custom",
    data: { name: "(Hyper-)Parameters", artifact_type: "parameters" },
    position: { x: 100 + 3 * 225, y: 0 },
    draggable: false,
    selectable: false,
    connectable: false,
  },
  {
    id: "5",
    type: "custom",
    data: { name: "Results", artifact_type: "results" },
    position: { x: 100 + 4 * 225, y: 0 },
    draggable: false,
    selectable: false,
    connectable: false,
  },
];

export default function GlobalPage() {
  const [legendNodes, setLegendNodes, onLegendNodesChange] =
    useNodesState(initLegendNodes);
  const [legendVisible, setLegendVisible] = useState(false);

  const toggleLegend = () => {
    setLegendVisible((prev) => !prev);
  };

  // Making sure that legend button is only displayed once the icon is rendered correctly
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // Wait for the component to mount and styles to be applied
    const timer = setTimeout(() => {
      setIsVisible(true);
    }, 50); // Small delay to ensure icon is rendered correctly

    return () => clearTimeout(timer);
  }, []);

  return (
    <div style={{ width: "100vw", height: "100vh" }}>
      {/* Legend Button */}
      <div
        className="button-container"
        style={{ position: "absolute", top: "125px", left: "24px", zIndex: 10 }}
      >
        <Button variant="secondary" onClick={toggleLegend}>
          {isVisible ? (
            legendVisible ? (
              <>
                Legend <FontAwesomeIcon icon={faAngleLeft} size="lg" />
              </>
            ) : (
              <>
                Legend <FontAwesomeIcon icon={faAngleRight} size="lg" />
              </>
            )
          ) : (
            <span style={{ visibility: "hidden" }}>Legend</span> // Hide before icon is visible
          )}
        </Button>
      </div>

      {/* Legend*/}
      <div
        className={`legend-container ${legendVisible ? "fade-in" : "fade-out"}`}
        style={{
          position: "absolute",
          top: "120px",
          left: "50px", // Adjust to prevent overlap with the button
          height: "100vh",
          overflow: "hidden", // Hide content while fading out
          transition: "width 0.5s ease, opacity 0.5s ease",
          opacity: legendVisible ? "1" : "0",
        }}
      >
        <ReactFlow
          nodes={legendNodes}
          edges={[]}
          style={{ height: "mincontent", width: "mincontent" }}
          zoomOnScroll={false}
          panOnDrag={false}
          zoomOnPinch={false}
          zoomOnDoubleClick={false}
          elementsSelectable={false}
          nodeTypes={nodeTypes}
        />
      </div>

      {/* Horizontal line */}
      <div
        style={{
          position: "absolute",
          top: "183px",
          left: "0",
          width: "100vw",
          height: "2px",
          backgroundColor: "#072140",
        }}
      ></div>

      {/* DAG */}
      <div
        style={{
          position: "absolute",
          top: "180px",
          left: "50px",
          width: "100vw",
          height: "100vh",
        }}
      >
        <DAGFlow />
      </div>
    </div>
  );
}
