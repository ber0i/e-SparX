import {
  faCircleNodes,
  faDatabase,
  faFileCode,
  faSliders,
  faSquarePollVertical,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { Handle, Position } from "@xyflow/react";

import "@xyflow/react/dist/base.css";

const artifactStyles = {
  dataset: {
    bgColor: "bg-brand-tumbluelight",
    borderColor: "border-brand-darkblue",
    icon: faDatabase,
    iconColor: "text-brand-white",
    textColor: "text-brand-white",
  },
  code: {
    bgColor: "bg-brand-darkblue",
    borderColor: "border-brand-darkblue",
    icon: faFileCode,
    iconColor: "text-brand-white",
    textColor: "text-brand-white",
  },
  model: {
    bgColor: "bg-brand-green",
    borderColor: "border-brand-darkblue",
    icon: faCircleNodes,
    iconColor: "text-brand-darkblue",
    textColor: "text-brand-darkblue",
  },
  hyperparameters: {
    bgColor: "bg-brand-green",
    borderColor: "border-brand-darkblue",
    icon: faSliders,
    iconColor: "text-brand-darkblue",
    textColor: "text-brand-darkblue",
  },
  parameters: {
    bgColor: "bg-brand-green",
    borderColor: "border-brand-darkblue",
    icon: faSliders,
    iconColor: "text-brand-darkblue",
    textColor: "text-brand-darkblue",
  },
  results: {
    bgColor: "bg-brand-orange",
    borderColor: "border-brand-darkblue",
    icon: faSquarePollVertical,
    iconColor: "text-brand-darkblue",
    textColor: "text-brand-darkblue",
  },
};

// Define the expected data structure
interface NodeData {
  artifact_type:
    | "dataset"
    | "code"
    | "model"
    | "hyperparameters"
    | "parameters"
    | "results";
  name: string;
  pipelines?: { idx: number; name: string }[];
}

export default function ArtifactNode({ data }: { data: NodeData }) {
  const style = artifactStyles[data.artifact_type] || {};

  return (
    <div
      className={`flex items-center pl-1 pr-9 rounded-md ${style.bgColor} border-2 ${style.borderColor}`}
      style={{ width: "210px" }}
    >
      {data.pipelines ? (
        <div className={`absolute flex -top-3 right-2 space-x-1`}>
          {data.pipelines.map((val) => (
            <a
              href={`/pipelines/${encodeURI(val.name)}`}
              title={`Pipeline: ${val.name}`}
              className={`w-6 h-6 rounded-[12px] bg-white text-center border-2 ${style.borderColor} leading-[1.2em]`}
              key={val.idx}
            >
              {val.idx}
            </a>
          ))}
        </div>
      ) : (
        ""
      )}
      <div className="flex w-full items-center py-1">
        <div
          className={`flex-shrink-0 rounded-full w-12 h-12 flex justify-center items-center bg-opacity-100`}
        >
          <FontAwesomeIcon
            icon={style.icon}
            className={style.iconColor}
            size="2x"
          />
        </div>
        <div className="flex-grow text-center">
          <div className={`text-ms ${style.textColor}`}>{data.name}</div>
        </div>
      </div>
      <Handle type="target" position={Position.Left} className="invisible" />
      <Handle type="source" position={Position.Right} className="invisible" />
    </div>
  );
}
