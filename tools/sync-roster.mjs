import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const CHECK = process.argv.includes("--check");
const read = rel => readFileSync(join(ROOT, rel), "utf8");
const cells = line => line.split("|").slice(1, -1).map(s => s.trim());
const sections = text => {
  const out = {};
  let key = null;
  let buf = [];
  for (const line of text.split("\n")) {
    const m = line.match(/^## (.+)$/);
    if (m) {
      if (key) out[key] = buf;
      key = m[1].trim();
      buf = [];
    } else if (key) buf.push(line);
  }
  if (key) out[key] = buf;
  return out;
};
const body = lines => (lines ?? []).join("\n").trim();

const errors = [];
const warnings = [];

const style = sections(read("characters/STYLE.md"));
const LEAD = body(style.Lead);
const TAIL = body(style.Tail);
if (!LEAD || !TAIL) errors.push("characters/STYLE.md needs ## Lead and ## Tail");

const p15 = read("plan/15-roster-and-archetypes.md").split("\n");
const roleOf = Object.fromEntries(p15.filter(l => /^\| \d{2} \|/.test(l)).map(l => {
  const c = cells(l);
  return [c[1], c[2]];
}));
const p15BySlot = Object.fromEntries(p15.filter(l => /^\| \d{3} \|/.test(l)).map(l => {
  const c = cells(l);
  return [c[0], {name: c[1], family: c[2], attr: c[3], range: c[4]}];
}));
const p22BySlot = Object.fromEntries(read("plan/22-art-direction.md").split("\n").filter(l => /^\| \d{3} \|/.test(l)).map(l => {
  const c = cells(l);
  return [c[0], {hero: c[1].replace(/\s*\(P\d+\)$/, ""), prop: c[3], values: c[5]}];
}));

const dir = join(ROOT, "characters");
const heroes = readdirSync(dir).filter(n => /^\d{3}-.+\.md$/.test(n)).sort().map(file => {
  const text = readFileSync(join(dir, file), "utf8");
  const slot = file.slice(0, 3);
  const title = text.split("\n")[0].match(/^# (\d{3}) (.+)$/);
  const reserve = /^- Status: reserve\./m.test(text);
  const s = sections(text);
  const hero = {
    file,
    slot,
    name: title ? title[2].trim() : "",
    reserve,
    lead: body(s.Lead) || LEAD,
    subject: body(s.Subject),
    hook: body(s.Hook),
    refs: (s["Aesthetic refs"] ?? []).map(l => l.trim()).filter(l => l.startsWith("- ")).map(l => l.slice(2).trim()),
    row: p15BySlot[slot],
    p22: p22BySlot[slot],
  };

  if (!title || title[1] !== slot) errors.push(`${file}: title must read "# ${slot} Name"`);
  if (!reserve) {
    if (!hero.row) errors.push(`${file}: no plan/15 roster row for ${slot}`);
    else if (hero.row.name !== hero.name) errors.push(`${file}: name "${hero.name}" differs from plan/15 "${hero.row.name}"`);
    if (!hero.p22) errors.push(`${file}: no plan/22 row for ${slot}`);
    else if (hero.p22.hero !== hero.name) errors.push(`${file}: name "${hero.name}" differs from plan/22 "${hero.p22.hero}"`);
    if (hero.row && !roleOf[hero.row.family]) errors.push(`${file}: role family "${hero.row.family}" has no role in plan/15`);
  }
  if (!hero.subject) errors.push(`${file}: empty ## Subject`);
  if (/neutral background|stylized 3d/i.test(hero.subject)) errors.push(`${file}: subject repeats the shared lead or tail`);
  if (!hero.hook || hero.hook === "TBD") errors.push(`${file}: ## Hook is still TBD`);
  if (hero.hook.includes("\n") || hero.hook.includes("|")) errors.push(`${file}: hook must be one line with no pipe`);
  if (hero.hook.length > 200) warnings.push(`${file}: hook is over 200 characters`);
  for (const r of hero.refs) if (!/^https?:\/\//.test(r)) warnings.push(`${file}: aesthetic ref is not a URL: ${r}`);
  return hero;
});

const openings = new Map();
for (const h of heroes) {
  if (!h.hook || h.hook === "TBD") continue;
  const key = h.hook.split(/\s+/).slice(0, 3).join(" ").toLowerCase();
  openings.set(key, [...(openings.get(key) ?? []), h.name]);
}
for (const [key, names] of openings) {
  if (names.length >= 3) warnings.push(`hook opening "${key}" is used by ${names.join(", ")}`);
}

const card = h => {
  if (h.reserve) return ["- Status: reserve. No role family, attribute or prop until promoted (plan/15)."];
  return [
    `- Role family: ${h.row?.family}`,
    `- Role: ${roleOf[h.row?.family]}`,
    `- Attribute: ${h.row?.attr}`,
    `- Range: ${h.row?.range}`,
    `- Distinct prop: ${h.p22?.prop}`,
    `- Value groups (body / head / prop): ${h.p22?.values}`,
  ];
};

const renderHero = h => [
  `# ${h.slot} ${h.name}`,
  "",
  "## Card",
  "",
  ...card(h),
  "",
  ...(h.lead !== LEAD ? ["## Lead", "", h.lead, ""] : []),
  "## Subject",
  "",
  h.subject,
  "",
  "## Hook",
  "",
  h.hook,
  "",
  ...(h.refs.length ? ["## Aesthetic refs", "", ...h.refs.map(r => `- ${r}`), ""] : []),
].join("\n");

const q = JSON.stringify;
const rosterYaml = ["roster:", ...heroes.flatMap((h, i) => [
  ...(i ? [""] : []),
  `  - name: ${q(h.name)}`,
  ...(h.reserve ? ["    reserve: true"] : []),
  `    prompt: ${q(`${h.lead}, ${h.subject}, ${TAIL}`)}`,
  ...(h.refs.length ? ["    aesthetic_refs:", ...h.refs.map(r => `      - ${q(r)}`)] : ["    aesthetic_refs: []"]),
])].join("\n") + "\n";

const index = ["index\tname\thero_slot\tfile", ...heroes.map(h =>
  [h.slot, h.name, h.reserve ? "reserve" : h.slot, `characters/${h.file}`].join("\t"))].join("\n") + "\n";

const hookBySlot = Object.fromEntries(heroes.filter(h => !h.reserve).map(h => [h.slot, h.hook]));
const p15Next = read("plan/15-roster-and-archetypes.md").split("\n").map(line => {
  const m = line.match(/^\| (\d{3}) \|/);
  if (!m || !(m[1] in hookBySlot)) return line;
  const parts = line.split("|");
  parts[6] = ` ${hookBySlot[m[1]]} `;
  return parts.join("|");
}).join("\n");

for (const e of errors) console.error(`error: ${e}`);
for (const w of warnings) console.error(`warning: ${w}`);
if (errors.length) process.exit(1);

const active = heroes.filter(h => !h.reserve);
const rosterMd = [`# Roster: ${active.length} heroes from the character set`, "", `Slot ${active[0]?.slot}-${active.at(-1)?.slot} = the character files in order, with gaps where a slot was retired. Reserve slots follow.`, "", "| Slot | Character | Prompt file |", "| --- | --- | --- |", ...heroes.filter(h => !h.reserve).map(h => `| ${h.slot} | ${h.name} | characters/${h.file} |`), "", "## Reserve", "", ...heroes.filter(h => h.reserve).map(h => `- ${h.name} (characters/${h.file})`)].join("\n") + "\n";
const outputs = [
  ["roster.yaml", rosterYaml],
  ["ROSTER.md", rosterMd],
  ["characters/INDEX.tsv", index],
  ["plan/15-roster-and-archetypes.md", p15Next],
  ...heroes.map(h => [`characters/${h.file}`, renderHero(h)]),
];
const stale = [];
for (const [rel, text] of outputs) {
  let current = null;
  try { current = read(rel); } catch {}
  if (current === text) continue;
  stale.push(rel);
  if (!CHECK) writeFileSync(join(ROOT, rel), text);
}

if (CHECK && stale.length) {
  console.error(`stale: ${stale.join(", ")}`);
  process.exit(1);
}
console.log(CHECK ? "up to date" : `wrote ${stale.length} file(s)`);
