import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { Dashboard } from "@/components/dashboard";
import type { ReportDoc } from "@/lib/types";

async function getData(): Promise<ReportDoc | null> {
  try {
    const raw = await readFile(
      join(process.cwd(), "src", "data", "report.json"),
      "utf-8",
    );
    return JSON.parse(raw) as ReportDoc;
  } catch {
    return null;
  }
}

export default async function Page() {
  const doc = await getData();
  return <Dashboard doc={doc} />;
}
