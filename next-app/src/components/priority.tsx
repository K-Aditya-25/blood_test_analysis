import type { Patient, Section } from "@/lib/types";
import { fmtVal, tone, STATUS_LABEL } from "@/lib/format";

export function Priority({ p, sections }: { p: Patient; sections: Section[] }) {
  const flagged = p.tests.filter((t) => t.status !== "normal" && t.section !== "urine");
  if (!flagged.length) return null;

  return (
    <div className="priority">
      <h3>
        Needs attention <span className="badge">{flagged.length}</span>
      </h3>
      <p className="hint">
        These results fell outside their healthy range. Tap one to jump to its section.
      </p>
      <div className="prio-list">
        {flagged.map((t) => {
          const sec = sections.find((s) => s.key === t.section);
          const tn = tone(t.status);
          return (
            <a key={t.key} className="prio-item" href={`#${t.section}`}>
              <span className={`chip ${tn}`}>{STATUS_LABEL[tn][0]}</span>
              <span>
                <div className="pi-n">{t.name}</div>
                <div className="pi-d">
                  {fmtVal(t)}
                  {t.unit ? " " + t.unit : ""} · <b>{sec ? sec.title : t.section}</b>
                </div>
              </span>
            </a>
          );
        })}
      </div>
    </div>
  );
}
