import type { Test } from "@/lib/types";
import { showVal } from "@/lib/format";
import { CheckIcon } from "@/lib/icons";

export function UrineTiles({ tests }: { tests: Test[] }) {
  return (
    <div className="grid">
      {tests.map((t) => {
        const val = showVal(t);
        const base = t.value_text || "";
        const nice = base.charAt(0).toUpperCase() + base.slice(1).toLowerCase();
        const label = t.value_text ? nice : val;
        return (
          <div className="tile" key={t.key}>
            <div className="ck">
              <CheckIcon />
            </div>
            <div>
              <div className="tn">{t.name}</div>
              <div className="tv">{label}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
