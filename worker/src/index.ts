/**
 * Vitals API Proxy — Cloudflare Worker
 *
 * Security model:
 *   - No API keys live in Vercel environment variables.
 *   - All secrets are stored as Cloudflare Worker secrets
 *     (wrangler secret put KEY_NAME) and accessed via `env`.
 *   - The browser only ever sees calls to this Worker's public URL;
 *     keys are never exposed in network traffic or source maps.
 *   - Vercel cannot read the secrets — only the Worker runtime can.
 */

export interface Env {
  ALLOWED_ORIGIN: string;
  // Secrets (set via `wrangler secret put`):
  // TENSORIX_API_KEY: string;
}

function corsHeaders(origin: string): Record<string, string> {
  return {
    "Access-Control-Allow-Origin": origin,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type, Authorization",
    "Access-Control-Max-Age": "86400",
  };
}

function json(body: unknown, init: ResponseInit, origin: string): Response {
  return new Response(JSON.stringify(body), {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...corsHeaders(origin),
      ...init.headers,
    },
  });
}

export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const origin = env.ALLOWED_ORIGIN || "*";

    if (request.method === "OPTIONS") {
      return new Response(null, { headers: corsHeaders(origin) });
    }

    if (url.pathname === "/health") {
      return json(
        { status: "ok", service: "vitals-api-proxy", time: new Date().toISOString() },
        { status: 200 },
        origin,
      );
    }

    // ── Example: proxy an LLM call ──────────────────────────────────
    // The secret key is read from the Worker environment (set via
    // `wrangler secret put TENSORIX_API_KEY`). It is never visible
    // to the browser, Vercel, or source control.
    //
    // if (url.pathname === "/api/llm" && request.method === "POST") {
    //   const apiKey = env.TENSORIX_API_KEY;
    //   if (!apiKey) {
    //     return json({ error: "API key not configured" }, { status: 500 }, origin);
    //   }
    //   const body = await request.json();
    //   const resp = await fetch("https://api.tensorix.ai/v1/chat/completions", {
    //     method: "POST",
    //     headers: {
    //       Authorization: `Bearer ${apiKey}`,
    //       "Content-Type": "application/json",
    //     },
    //     body: JSON.stringify(body),
    //   });
    //   return new Response(resp.body, { headers: corsHeaders(origin) });
    // }

    return json(
      { error: "Not found", path: url.pathname },
      { status: 404 },
      origin,
    );
  },
};
