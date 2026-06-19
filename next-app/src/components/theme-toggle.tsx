"use client";

import { useEffect, useState } from "react";
import { useTheme } from "next-themes";
import { SunIcon, MoonIcon } from "@/lib/icons";

export function ThemeToggle() {
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => setMounted(true), []);

  const dark = mounted && resolvedTheme === "dark";

  return (
    <button
      className="theme-toggle"
      aria-label="Toggle dark mode"
      title="Toggle light / dark"
      onClick={() => setTheme(dark ? "light" : "dark")}
    >
      <span className="knob">
        <SunIcon className="ic-sun" />
        <MoonIcon className="ic-moon" />
      </span>
    </button>
  );
}
