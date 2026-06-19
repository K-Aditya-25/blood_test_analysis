"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import type { Test } from "@/lib/types";

/* ------------------------------------------------------------------ *
 * WBC differential — elegant donut
 *
 * Why arc-path wedges (not stroke-dasharray circles):
 *   • clean visible gaps between segments
 *   • tiny segments (basophils ~0.4%) get a minimum visible arc
 *   • hover can lift a single wedge radially
 * A dedicated, harmonious palette is used instead of the semantic
 * theme vars (which collided — e.g. lymphocytes were "normal green").
 * ------------------------------------------------------------------ */

const WANT = ["neutrophils", "lymphocytes", "monocytes", "eosinophils", "basophils"] as const;

// Curated palette — distinct, harmonious, readable on light + dark.
const COLORS: Record<string, string> = {
  neutrophils: "#6366f1", // indigo
  lymphocytes: "#0ea5e9", // sky
  monocytes: "#14b8a6", // teal
  eosinophils: "#f59e0b", // amber
  basophils: "#ec4899", // pink
};

const TAU = Math.PI * 2;
const GAP = 0.018; // rad between segments (~1°)
const MIN_ARC = 0.06; // rad minimum (~3.4°) so basophils is visible

function polar(cx: number, cy: number, r: number, rad: number): [number, number] {
  return [cx + r * Math.cos(rad), cy + r * Math.sin(rad)];
}

/** Annular-sector (wedge) path with a rounded outer edge. */
function wedge(
  cx: number,
  cy: number,
  rInner: number,
  rOuter: number,
  start: number,
  end: number,
): string {
  const [x1, y1] = polar(cx, cy, rOuter, start);
  const [x2, y2] = polar(cx, cy, rOuter, end);
  const [x3, y3] = polar(cx, cy, rInner, end);
  const [x4, y4] = polar(cx, cy, rInner, start);
  const large = end - start > Math.PI ? 1 : 0;
  return [
    `M ${x1.toFixed(2)} ${y1.toFixed(2)}`,
    `A ${rOuter} ${rOuter} 0 ${large} 1 ${x2.toFixed(2)} ${y2.toFixed(2)}`,
    `L ${x3.toFixed(2)} ${y3.toFixed(2)}`,
    `A ${rInner} ${rInner} 0 ${large} 0 ${x4.toFixed(2)} ${y4.toFixed(2)}`,
    "Z",
  ].join(" ");
}

interface Seg {
  t: Test;
  c: string;
  start: number;
  end: number;
  mid: number;
}

export function Donut({ tests }: { tests: Test[] }) {
  const [hover, setHover] = useState<number | null>(null);

  const rows = WANT.map((k) => tests.find((x) => x.key === k))
    .filter((t): t is Test => Boolean(t))
    .map((t) => ({ t, c: COLORS[t.key] ?? "#64748b" }));

  const total = rows.reduce((s, r) => s + (r.t.value ?? 0), 0) || 1;

  // Build angular segments: proportional, with a minimum arc and gaps.
  let cursor = -Math.PI / 2; // start at top
  const segs: Seg[] = rows.map((r) => {
    const frac = (r.t.value ?? 0) / total;
    let arc = Math.max(frac * TAU, MIN_ARC);
    if (rows.length > 1) arc -= GAP; // reserve gap
    const start = cursor;
    const end = cursor + arc;
    cursor = end + GAP;
    return { t: r.t, c: r.c, start, end, mid: (start + end) / 2 };
  });

  const cx = 95;
  const cy = 95;
  const rOuter = 80;
  const rInner = 56;

  return (
    <div className="donut-wrap">
      <div className="donut-box" style={{ width: 190, height: 190 }}>
        <svg width="190" height="190" viewBox="0 0 190 190">
          {/* track ring */}
          <circle
            cx={cx}
            cy={cy}
            r={(rOuter + rInner) / 2}
            fill="none"
            stroke="var(--surface-3)"
            strokeWidth={rOuter - rInner}
            opacity={0.5}
          />
          {segs.map((s, i) => {
            const isHover = hover === i;
            const dimmed = hover !== null && !isHover;
            // lift hovered wedge along its bisector
            const lift = 6;
            const dx = isHover ? lift * Math.cos(s.mid) : 0;
            const dy = isHover ? lift * Math.sin(s.mid) : 0;
            return (
              <motion.path
                key={s.t.key}
                d={wedge(cx, cy, rInner, rOuter, s.start, s.end)}
                fill={s.c}
                initial={false}
                animate={{
                  opacity: dimmed ? 0.35 : 1,
                  x: dx,
                  y: dy,
                }}
                transition={{ duration: 0.2, ease: "easeOut" }}
                style={{ cursor: "pointer" }}
                onMouseEnter={() => setHover(i)}
                onMouseLeave={() => setHover(null)}
              />
            );
          })}
        </svg>
        <div className="donut-center">
          <div className="n">
            {hover !== null ? (
              <>
                {segs[hover].t.value}
                <span style={{ fontSize: 13 }}>%</span>
              </>
            ) : (
              <>
                {Math.round(total)}
                <span style={{ fontSize: 13 }}>%</span>
              </>
            )}
          </div>
          <div className="l">
            {hover !== null ? segs[hover].t.name : "WBC diff"}
          </div>
        </div>
      </div>

      <ul className="legend wbc-legend">
        {rows.map((r, i) => (
          <li
            key={r.t.key}
            className="wbc-row"
            data-hover={hover === i}
            data-dim={hover !== null && hover !== i}
            onMouseEnter={() => setHover(i)}
            onMouseLeave={() => setHover(null)}
          >
            <span className="sw" style={{ background: r.c }} />
            <div className="wbc-info">
              <div className="wbc-top">
                <b>{r.t.name}</b>
                <span className="pct-v">{r.t.value}%</span>
              </div>
              <RangeBar t={r.t} color={r.c} />
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

/** Mini reference-range bar mirroring the gauge style. */
function RangeBar({ t, color }: { t: Test; color: string }) {
  const low = t.band_low;
  const high = t.band_high;
  const val = t.value ?? 0;

  if (low == null || high == null) {
    // e.g. basophils "<2.00" — show a threshold bar.
    const high2 = t.band_high ?? 2;
    const span = high2 * 1.5 || 1;
    const w = (high2 / span) * 100;
    const vp = Math.min(100, (val / span) * 100);
    return (
      <div className="rbar">
        <div className="rtrack">
          <div className="rband" style={{ left: 0, width: `${w}%` }} />
          <div className="rdot" style={{ left: `${vp}%`, background: color }} />
        </div>
        <span className="rref">ref {t.ref_text}</span>
      </div>
    );
  }

  const span = high - low || 1;
  const amin = Math.max(0, low - 0.4 * span);
  const amax = high + 0.4 * span;
  const range = amax - amin || 1;
  const bl = ((low - amin) / range) * 100;
  const bw = ((high - low) / range) * 100;
  const vp = Math.max(0, Math.min(100, ((val - amin) / range) * 100));

  return (
    <div className="rbar">
      <div className="rtrack">
        <div className="rband" style={{ left: `${bl}%`, width: `${bw}%` }} />
        <div className="rdot" style={{ left: `${vp}%`, background: color }} />
      </div>
      <span className="rref">ref {t.ref_text}</span>
    </div>
  );
}
