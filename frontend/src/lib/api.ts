"use client";

import axios from "axios";

/** API Endpoint */
export const api_endpoint: string =
  process.env.NEXT_PUBLIC_EDL_API_ENDPOINT || "http://localhost:9000";

/** Get version of the API */
export async function status(): Promise<{
  version: string | undefined;
  status: "online" | "offline" | "error";
}> {
  try {
    const res = await axios.get(`${api_endpoint}`, { timeout: 1000 });

    if (res.status === 200) {
      return { version: res.data.version, status: "online" };
    }
  } catch {
    return {
      version: undefined,
      status: "offline",
    };
  }

  return { version: undefined, status: "error" };
}
