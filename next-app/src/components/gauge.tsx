"use client";

import { motion } from "framer-motion";
import type { Test } from "@/lib/types";
import { fmtVal, pct, clamp, tone, valClass, STATUS_LABEL } from "@/lib/format";

export function Gauge({ t }: { t: Test }) {
  const v = fmtVal(t);
  const dot = clamp(pct(t.value == null ? 0 : t.value, t));
  const tn = tone(t.status);

  let band: { l: number; w: number } | null = null;
  if (t.band_low != null && t.band_high != null) {
    const l = clamp(pct(t.band_low, t));
    const w = clamp(pct(t.band_high, t)) - l;
    band = { l, w: Math.max(w, 2) };
  }

  const ref = t.ref_text || "\u2014";
  const tag =
    t.status !== "normal" ? (
      <span className={`tag ${tn}`}>{STATUS_LABEL[tn]}</span>
    ) : null;

  return (
    <div className="test">
      <div className="test-head">
        <span className="tname">
          {t.name}
          {tag}
        </span>
        <span className="tmeta">
          <b className={`tval ${valClass(t.status)}`}>
            {v}
            {t.unit ? (
              <>
                {" "}
                <small>{t.unit}</small>
              </>
            ) : null}
          </b>
          <span className="ref">ref {ref}</span>
        </span>
      </div>
      <div className="strip">
        {band && (
          <motion.div
            className="band"
            style={{ left: `${band.l}%`, width: `${band.w}%` }}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.4 }}
          />
        )}
        <motion.div
          className={`marker m-${tn}`}
          initial={{ left: "0%" }}
          animate={{ left: `${dot}%` }}
          transition={{ duration: 0.6, ease: [0.4, 0, 0.2, 1] }}
        />
      </div>
      <div className={`tnote ${t.status !== "normal" ? "warn" : ""}`}>{t.note || ""}</div>
    </div>
  );
}
