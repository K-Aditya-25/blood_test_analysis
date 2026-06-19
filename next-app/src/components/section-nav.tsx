"use client";

import { useEffect, useState } from "react";
import type { Patient, Section } from "@/lib/types";

export function SectionNav({ sections, p }: { sections: Section[]; p: Patient }) {
  const [active, setActive] = useState<string>(sections[0]?.key ?? "");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) setActive((e.target as HTMLElement).id);
        });
      },
      { rootMargin: "-90px 0px -65% 0px", threshold: 0 },
    );
    sections.forEach((s) => {
      const el = document.getElementById(s.key);
      if (el) observer.observe(el);
    });
    return () => observer.disconnect();
  }, [sections, p]);

  return (
    <nav className="secnav">
      {sections.map((s) => {
        const cnt = p.tests.filter((t) => t.section === s.key).length;
        return (
          <a key={s.key} href={`#${s.key}`} className={active === s.key ? "active" : ""}>
            {s.title}
            <span style={{ opacity: 0.6, marginLeft: 5 }}>{cnt}</span>
          </a>
        );
      })}
    </nav>
  );
}
