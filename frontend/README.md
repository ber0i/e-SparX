# EDL Registry MVP - Frontend

## Getting Started

As first step, create a `.env` file in this directory of the following form:

```bash
NEXT_PUBLIC_API_ENDPOINT="http://127.0.0.1:8080"
```

If you're running the API individually (outside of the container), the endpoint could be different.

Next, run the following line once

```bash
npm install
```

to install all dependencies. To start the frontend in development mode, run

```bash
npm run dev
```

## Automatically Created TypeScript Client Code

When changes are made on backend models, the corresponding TypeScript representations for the frontend can be automatically generated via running the script in `scripts/gen_tsAPIclientcode.py`.
