CSS = """
:root{
  --bg:#f1f5f9;--card:#ffffff;--ink:#0f172a;--muted:#64748b;--line:#e2e8f0;
  --normal:#16a34a;--low:#d97706;--high:#dc2626;--info:#2563eb;
  --band:#dcfce7;--band-edge:#86efac;
  --grad1:#0ea5e9;--grad2:#6366f1;
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;
  background:var(--bg);color:var(--ink);line-height:1.5}
header.top{position:sticky;top:0;z-index:10;background:linear-gradient(120deg,var(--grad1),var(--grad2));
  color:#fff;padding:18px 28px;display:flex;align-items:center;justify-content:space-between;
  box-shadow:0 2px 12px rgba(2,6,23,.12)}
.brand{font-weight:700;font-size:18px;letter-spacing:.3px}
.brand small{display:block;font-weight:400;opacity:.85;font-size:12px}
#toggle{background:#fff;color:var(--grad2);border:none;border-radius:999px;padding:10px 18px;
  font-weight:600;cursor:pointer;font-size:14px;box-shadow:0 4px 14px rgba(0,0,0,.15);transition:.2s}
#toggle:hover{transform:translateY(-1px);box-shadow:0 6px 18px rgba(0,0,0,.22)}
main{max-width:1040px;margin:0 auto;padding:24px 20px 60px}
.hero{background:var(--card);border-radius:18px;padding:24px 26px;box-shadow:0 6px 24px rgba(2,6,23,.06);
  margin-bottom:22px;border:1px solid var(--line)}
.hero h1{margin:0 0 4px;font-size:26px}
.hero .meta{color:var(--muted);font-size:14px;margin-bottom:14px}
.hero .headline{font-size:16px;padding:12px 16px;border-radius:12px;background:#eff6ff;border-left:4px solid var(--info)}
.pill{display:inline-block;padding:4px 12px;border-radius:999px;font-size:13px;font-weight:600;margin-right:8px}
.pill.flag{background:#fef2f2;color:var(--high)}
.pill.ok{background:#f0fdf4;color:var(--normal)}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;
  margin-bottom:18px;box-shadow:0 4px 16px rgba(2,6,23,.05)}
.card h2{margin:0 0 4px;font-size:19px;display:flex;align-items:center;gap:8px}
.card .story{color:var(--muted);font-size:14px;margin:0 0 14px}
.secsum{font-size:14px;line-height:1.55;padding:12px 16px;margin-bottom:16px;border-radius:11px;
  background:#f8fafc;border:1px solid var(--line);border-left:4px solid var(--info)}
.test{padding:10px 0;border-bottom:1px dashed var(--line)}
.test:last-child{border-bottom:none}
.test-head{display:flex;justify-content:space-between;align-items:baseline;gap:12px}
.tname{font-weight:600;font-size:14px}
.tmeta{text-align:right}
.tval{font-weight:700;font-size:15px;white-space:nowrap}
.tval small{font-weight:400;color:var(--muted);font-size:11px}
.ref{display:block;font-size:11px;color:var(--muted);margin-top:1px}
.s-normal{color:var(--normal)}.s-low{color:var(--low)}.s-high{color:var(--high)}.s-info{color:var(--info)}
.strip{position:relative;height:22px;margin:7px 0 4px;background:#f8fafc;border-radius:7px;border:1px solid var(--line)}
.band{position:absolute;top:2px;bottom:2px;background:var(--band);border:1px solid var(--band-edge);border-radius:5px}
.marker{position:absolute;top:-3px;bottom:-3px;width:3px;border-radius:3px}
.marker::after{content:'';position:absolute;top:-2px;left:-5px;width:13px;height:13px;border-radius:50%;
  background:inherit;box-shadow:0 1px 4px rgba(0,0,0,.3)}
.m-normal{background:var(--normal)}.m-low{background:var(--low)}.m-high{background:var(--high)}.m-info{background:var(--info)}
.tnote{font-size:12.5px;color:#475569;margin-top:6px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px}
.tile{border-radius:12px;padding:12px 14px;border:1px solid var(--line);background:#f8fafc}
.tile .tn{font-size:12px;color:var(--muted)}.tile .tv{font-weight:700;margin-top:2px}
.tile.ok{background:#f0fdf4;border-color:#bbf7d0}.tile.ok .tv{color:var(--normal)}
.donut-wrap{display:flex;gap:20px;align-items:center;flex-wrap:wrap;margin-top:6px}
.legend{font-size:13px}.legend li{margin:3px 0}
footer{text-align:center;color:var(--muted);font-size:12px;padding:24px}
"""
