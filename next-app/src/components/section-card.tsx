import type { Patient, Section } from "@/lib/types";
import { ICON } from "@/lib/icons";
import { Gauge } from "./gauge";
import { Donut } from "./donut";
import { UrineTiles } from "./urine-tiles";

const DIFF = ["neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils"];

export function SectionCard({ s, p }: { s: Section; p: Patient }) {
  const tests = p.tests.filter((t) => t.section === s.key);
  if (!tests.length) return null;

  let body: React.ReactNode;
  if (s.key === "urine") {
    body = <UrineTiles tests={tests} />;
  } else if (s.key === "blood_cells") {
    body = (
      <>
        <Donut tests={tests} />
        {tests
          .filter((t) => !DIFF.includes(t.key))
          .map((t) => (
            <Gauge key={t.key} t={t} />
          ))}
      </>
    );
  } else {
    body = tests.map((t) => <Gauge key={t.key} t={t} />);
  }

  const summ = p.section_summary[s.key] || "";

  return (
    <section className="card" id={s.key}>
      <div className="card-h">
        <div className="card-ic">{ICON[s.icon] || "\u{1F4CA}"}</div>
        <div>
          <h2>{s.title}</h2>
          <div className="area">{s.area || ""}</div>
        </div>
      </div>
      <p className="story">{s.story}</p>
      {summ ? <div className="secsum">{summ}</div> : null}
      {body}
    </section>
  );
}
