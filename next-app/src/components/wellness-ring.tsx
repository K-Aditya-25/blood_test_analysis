"use client";

import { motion } from "framer-motion";

export function WellnessRing({ pct: value }: { pct: number }) {
  const r = 54;
  const c = 2 * Math.PI * r;
  const v = Math.max(0, Math.min(100, value));
  const off = c * (1 - v / 100);

  return (
    <div className="ring-wrap">
      <svg className="ring" width="130" height="130" viewBox="0 0 130 130">
        <defs>
          <linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" style={{ stopColor: "var(--accent-1)" }} />
            <stop offset="100%" style={{ stopColor: "var(--accent-2)" }} />
          </linearGradient>
        </defs>
        <circle className="track" cx="65" cy="65" r={r} strokeWidth={12} />
        <motion.circle
          className="fill"
          cx="65"
          cy="65"
          r={r}
          strokeWidth={12}
          strokeDasharray={c}
          initial={{ strokeDashoffset: c }}
          animate={{ strokeDashoffset: off }}
          transition={{ duration: 1, ease: [0.4, 0, 0.2, 1] }}
        />
      </svg>
      <div className="ring-center">
        <div className="pct">
          {Math.round(v)}
          <span style={{ fontSize: 18 }}>%</span>
        </div>
        <div className="lab">in range</div>
      </div>
    </div>
  );
}
