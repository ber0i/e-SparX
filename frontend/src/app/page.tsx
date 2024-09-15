"use client";

import clsx from "clsx";

import * as api from "@/lib/manual/api";
import { useEffect, useState } from "react";

export default function StatusPage() {
  const [status, setStatus] = useState<{
    version: string | undefined;
    status: "online" | "offline" | "error";
  }>({
    version: undefined,
    status: "offline",
  });

  useEffect(() => {
    api.status().then((data) => setStatus(data));
  }, []);

  return (
    <div className="flex justify-center">
      <div className="flex flex-col items-center">
        <h1 className="text-2xl font-bold mb-4">
          Energy Data Lab API Status:{" "}
          <span
            className={clsx({
              "text-brand-green": status.status === "online",
              "text-brand-orange": status.status === "offline",
              "text-brand-red": status.status === "error",
            })}
          >
            {status.status}
          </span>
        </h1>
        {status.version ? (
          <h2 className="text-lg mb-4">Version: {status.version}</h2>
        ) : null}
      </div>
    </div>
  );
}
