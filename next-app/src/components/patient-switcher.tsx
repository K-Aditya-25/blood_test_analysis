"use client";

import type { Patient } from "@/lib/types";

export function PatientSwitcher({
  patients,
  idx,
  onPick,
}: {
  patients: Patient[];
  idx: number;
  onPick: (i: number) => void;
}) {
  return (
    <div className="switcher" role="tablist" aria-label="Switch patient">
      {patients.map((p, i) => (
        <button
          key={p.lab_no || i}
          role="tab"
          aria-selected={i === idx}
          data-i={i}
          data-flag={p.flagged_count ? "1" : "0"}
          className={i === idx ? "active" : ""}
          onClick={() => onPick(i)}
        >
          <span className="dot" />
          <span>{p.first_name}</span>
        </button>
      ))}
    </div>
  );
}
