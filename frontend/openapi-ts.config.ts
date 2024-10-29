import { defineConfig } from "@hey-api/openapi-ts";

export default defineConfig({
  input: "", // Will be set when calling `openapi-ts`
  output: "", // Will be set when calling `openapi-ts`
  client: "@hey-api/client-fetch",
  types: {
    enums: "typescript",
  },
  schemas: false,
});
