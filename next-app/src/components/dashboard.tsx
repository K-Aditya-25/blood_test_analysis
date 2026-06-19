"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import type { ReportDoc } from "@/lib/types";
import { Header } from "./header";
import { Hero } from "./hero";
import { Priority } from "./priority";
import { SectionNav } from "./section-nav";
import { SectionCard } from "./section-card";
import { Footer } from "./footer";

export function Dashboard({ doc }: { doc: ReportDoc | null }) {
  const [idx, setIdx] = useState(0);

  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "smooth" });
  }, [idx]);

  if (!doc || !doc.patients.length) {
    return (
      <>
        <main>
          <div className="empty-state">
            <h2>No report data yet</h2>
            <p>Generate the dashboard data from your blood-test PDFs by running, from the repo root:</p>
            <p style={{ margin: "12px 0" }}>
              <code>uv run python -m src.export_json</code>
            </p>
            <p style={{ fontSize: 12 }}>
              This reads <code>private_reports/*.pdf</code> via the Python pipeline and writes
              <code> next-app/src/data/report.json</code>.
            </p>
          </div>
        </main>
        <Footer />
      </>
    );
  }

  const p = doc.patients[idx];

  return (
    <>
      <Header patients={doc.patients} idx={idx} onPick={setIdx} />
      <main>
        <AnimatePresence mode="wait">
          <motion.div
            key={idx}
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -8 }}
            transition={{ duration: 0.3, ease: "easeOut" }}
          >
            <Hero p={p} />
            <Priority p={p} sections={doc.sections} />
            <SectionNav sections={doc.sections} p={p} />
            {doc.sections.map((s) => (
              <SectionCard key={s.key} s={s} p={p} />
            ))}
          </motion.div>
        </AnimatePresence>
      </main>
      <Footer />
    </>
  );
}
