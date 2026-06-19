import type { Status, Test } from "./types";

/** Maps a raw status to one of the four visual tones. */
export const M: Record<Status, "normal" | "low" | "high" | "info"> = {
  normal: "normal",
  low: "low",
  high: "high",
  info: "info",
  flag: "high",
};

export const tone = (s: Status): "normal" | "low" | "high" | "info" => M[s] ?? "normal";

export const valClass = (s: Status): string => "s-" + tone(s);

export const STATUS_LABEL: Record<string, string> = {
  high: "High",
  low: "Low",
  info: "Note",
  normal: "OK",
};

/** Display value: prefer text, then numeric, else an em dash. */
export const showVal = (t: Test): string => {
  if (t.value_text) return t.value_text;
  if (t.value == null) return "\u2014";
  const n = +t.value;
  return Math.abs(n) >= 100 ? n.toFixed(0) : n.toString();
};

export const fmtVal = showVal;

/** Position of a value along a test's scaled axis, as a percentage. */
export const pct = (x: number, t: Test): number =>
  ((x - t.axis_min) / (t.axis_max - t.axis_min || 1)) * 100;

export const clamp = (p: number): number => Math.max(-2, Math.min(102, p));
