"use client";

export * from "./api/index";
import { client } from "./api/services.gen";

/** Configure Client **/
client.setConfig({
  baseUrl: process.env.NEXT_PUBLIC_API_ENDPOINT || "http://localhost:9000",
});
