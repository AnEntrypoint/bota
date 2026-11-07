import { execFileSync } from "child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, writeFileSync } from "fs";
import { dirname, join, resolve } from "path";
import { fileURLToPath } from "url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const charsDir = resolve(process.env.BOTA_CHARS_DIR ?? join(ROOT, "..", "chars"));
const generatedDir = resolve(process.env.BOTA_GENERATED_DIR ?? join(ROOT, "..", "characters", "memes", "generated"));
const python = process.env.BOTA_PYTHON ?? "python3";
const OUT = join(ROOT, "gallery");

const RESERVE = new Set(["028", "029", "030", "031", "032"]);
const roster = readdirSync(join(ROOT, "characters"))
  .map((f) => f.match(/^(\d{3})-(.+)\.md$/))
  .filter(Boolean)
  .map((m) => ({ id: m[1], slug: m[2] }))
  .filter((r) => !RESERVE.has(r.id))
  .sort((a, b) => a.id.localeCompare(b.id));
const byId = new Map(roster.map((r) => [r.id, r]));

const sources = new Map();
if (existsSync(charsDir)) {
  for (const f of readdirSync(charsDir)) {
    const m = f.match(/^(.+?) \[(\d{3})\]\.(jpe?g|png|webp)$/i);
    if (m && byId.has(m[2])) sources.set(m[2], join(charsDir, f));
  }
}
if (existsSync(generatedDir)) {
  for (const f of readdirSync(generatedDir)) {
    const m = f.match(/^(\d{3})-.+-gemini\.(png|jpe?g)$/i);
    if (m && byId.has(m[1])) sources.set(m[1], join(generatedDir, f));
  }
}
if (!sources.size) {
  console.error(`gallery: no sources in ${charsDir} or ${generatedDir}`);
  process.exit(2);
}

mkdirSync(OUT, { recursive: true });
const entries = [];
for (const { id, slug } of roster) {
  const src = sources.get(id);
  if (!src) continue;
  const dst = join(OUT, `${id}-${slug}.jpg`);
  execFileSync(python, ["-I", join(ROOT, "tools", "resize.py"), src, dst, "1200"]);
  const md = readFileSync(join(ROOT, "characters", `${id}-${slug}.md`), "utf8");
  const title = (md.match(/^#\s+(.+)$/m) || [, `${id} ${slug}`])[1].trim();
  entries.push({ id, slug, title, file: `gallery/${id}-${slug}.jpg` });
}

const cards = entries
  .map(
    (e) =>
      `<figure><a href="${e.file}"><img src="${e.file}" alt="${e.title.replace(/"/g, "&quot;")}" loading="lazy"></a><figcaption>${e.title}</figcaption></figure>`
  )
  .join("\n");

const have = new Set(entries.map((e) => e.id));
const pending = roster.filter((r) => !have.has(r.id));

const md = `# Gallery

**${entries.length} of ${roster.length} characters generated.** Every image below opens full size.

<style>
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(170px,1fr));gap:14px}
.gal figure{margin:0;background:var(--zebra,#f6f4fa);border:1px solid var(--line,#ddd);border-radius:8px;overflow:hidden}
.gal img{display:block;width:100%;height:200px;object-fit:contain;background:#181818}
.gal figcaption{padding:6px 8px;font-size:13px;line-height:1.3}
.gal a{text-decoration:none}
</style>

<div class="gal">
${cards}
</div>

## Pending

Not generated yet: ${pending.length ? pending.map((p) => p.id).join(", ") : "none"}.
`;

writeFileSync(join(ROOT, "GALLERY.md"), md);

const manifestPath = join(ROOT, "manifest.json");
const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
if (!manifest.some((s) => s.files && s.files.includes("GALLERY.md"))) {
  const at = manifest.findIndex((s) => s.title === "Start");
  manifest.splice(at >= 0 ? at + 1 : 0, 0, { title: "Gallery", files: ["GALLERY.md"] });
  writeFileSync(manifestPath, JSON.stringify(manifest, null, 1) + "\n");
}

const readmePath = join(ROOT, "README.md");
const readme = readFileSync(readmePath, "utf8");
if (!readme.includes("GALLERY.md")) {
  writeFileSync(
    readmePath,
    readme.replace(
      /^(# .+\n)/m,
      "$1\n[Open the character gallery](GALLERY.md) — every generated character in one grid.\n"
    )
  );
}

console.log(`gallery: ${entries.length} generated, ${pending.length} pending, ${roster.length} total`);
