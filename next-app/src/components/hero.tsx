import type { Patient } from "@/lib/types";
import { WellnessRing } from "./wellness-ring";

export function Hero({ p }: { p: Patient }) {
  const inRange = p.total_count - p.flagged_count;
  const wpct = p.total_count ? (inRange / p.total_count) * 100 : 0;

  return (
    <div className="hero">
      <div className="hero-l">
        <h1>{p.name}</h1>
        <div className="meta">
          <span>{p.age} yrs</span>
          <span>·</span>
          <span>{p.gender}</span>
          <span>·</span>
          <span>
            Lab <b>{p.lab_no}</b>
          </span>
          <span>·</span>
          <span>
            Collected <b>{p.collected}</b>
          </span>
        </div>
        <div className="headline">{p.headline}</div>
        <div className="hero-pills">
          <span className="pill ok">
            <span className="pd" />
            {inRange} in range
          </span>
          <span className="pill flag">
            <span className="pd" />
            {p.flagged_count} to review
          </span>
          <span
            className="pill ok"
            style={{
              background: "var(--info-soft)",
              color: "var(--info)",
              borderColor: "color-mix(in srgb,var(--info) 24%,transparent)",
            }}
          >
            <span className="pd" style={{ background: "var(--info)" }} />
            {p.total_count} tests
          </span>
        </div>
      </div>
      <WellnessRing pct={wpct} />
    </div>
  );
}
