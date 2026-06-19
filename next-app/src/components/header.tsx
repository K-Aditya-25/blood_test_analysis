"use client";

import type { Patient } from "@/lib/types";
import { MarkIcon } from "@/lib/icons";
import { PatientSwitcher } from "./patient-switcher";
import { ThemeToggle } from "./theme-toggle";

export function Header({
  patients,
  idx,
  onPick,
}: {
  patients: Patient[];
  idx: number;
  onPick: (i: number) => void;
}) {
  return (
    <header className="top">
      <div className="brand">
        <div className="mark">
          <MarkIcon />
        </div>
        <div>
          <div className="t1">Vitals</div>
          <div className="t2">your blood report, visualized</div>
        </div>
      </div>
      <div className="head-right">
        <PatientSwitcher patients={patients} idx={idx} onPick={onPick} />
        <ThemeToggle />
      </div>
    </header>
  );
}
