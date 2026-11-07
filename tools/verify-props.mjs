import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import os from "node:os";
import { fileURLToPath, pathToFileURL } from "node:url";

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const ARRAY_KEYS = ["props", "rows", "characters", "models", "items", "entries"];
const SLUG_KEYS = ["slug", "character", "name", "prop", "id"];
const GLB_KEYS = ["outputGlb", "glbPath", "glb", "modelPath", "path", "file"];
const BYTES_KEYS = ["bytes", "byteCount", "size"];
const SHA_KEYS = ["sha256", "sha", "hash"];
const JOB_KEYS = ["jobId", "job", "job_id"];
const RESPONSE_KEYS = ["responseJson", "response", "responsePath"];

const pick = (row, keys) => {
  for (const key of keys) {
    const value = row[key];
    if (value !== undefined && value !== null && value !== "") return value;
  }
  return null;
};

const findRows = (doc) => {
  for (const key of ARRAY_KEYS) if (Array.isArray(doc[key])) return doc[key];
  for (const key of Object.keys(doc)) {
    const value = doc[key];
    if (Array.isArray(value) && value.length && typeof value[0] === "object") return value;
  }
  return [];
};

export const toPath = (value) => {
  if (typeof value !== "string") return null;
  const raw = value.startsWith("file:") ? fileURLToPath(value) : value;
  return path.isAbsolute(raw) ? raw : path.resolve(ROOT, raw);
};

export function verifyDoc(doc) {
  const rows = findRows(doc);
  const failures = [];
  const seen = new Set();
  let totalBytes = 0;
  if (!rows.length) failures.push("no rows");
  for (const row of rows) {
    const slug = String(pick(row, SLUG_KEYS) ?? "?");
    if (seen.has(slug)) failures.push(slug + ": duplicate slug");
    seen.add(slug);
    const glbValue = pick(row, GLB_KEYS);
    const glb = toPath(glbValue);
    if (!glb || !glb.endsWith(".glb")) {
      failures.push(slug + ": no glb path");
      continue;
    }
    if (!String(glbValue).includes("bota_prop_" + slug)) failures.push(slug + ": glb path outside its slug dir");
    let buf;
    try { buf = fs.readFileSync(glb); } catch { failures.push(slug + ": glb missing"); continue; }
    if (buf.length < 12 || buf.toString("ascii", 0, 4) !== "glTF" || buf.readUInt32LE(4) !== 2 || buf.readUInt32LE(8) !== buf.length) {
      failures.push(slug + ": bad glTF header");
      continue;
    }
    totalBytes += buf.length;
    const sha = crypto.createHash("sha256").update(buf).digest("hex");
    if (Number(pick(row, BYTES_KEYS)) !== buf.length) failures.push(slug + ": byte count mismatch");
    if (String(pick(row, SHA_KEYS)) !== sha) failures.push(slug + ": sha256 mismatch");
    if (!pick(row, JOB_KEYS)) failures.push(slug + ": no jobId");
    const response = toPath(pick(row, RESPONSE_KEYS));
    if (!response || !fs.existsSync(response)) failures.push(slug + ": responseJson missing");
  }
  return { checked: rows.length, failures, totalBytes };
}

const readDoc = (value) => JSON.parse(fs.readFileSync(toPath(value), "utf8"));

function selfTest() {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "bota-verify-"));
  const glb = path.join(dir, "bota_prop_probe", "bota_prop_probe.glb");
  fs.mkdirSync(path.dirname(glb), { recursive: true });
  const buf = Buffer.alloc(64);
  buf.write("glTF", 0, "ascii");
  buf.writeUInt32LE(2, 4);
  buf.writeUInt32LE(64, 8);
  fs.writeFileSync(glb, buf);
  const response = path.join(dir, "bota_prop_probe", "response.json");
  fs.writeFileSync(response, JSON.stringify({ Status: "DONE" }) + "\n");
  const sha = crypto.createHash("sha256").update(buf).digest("hex");
  const row = { slug: "probe", outputGlb: pathToFileURL(glb).href, bytes: 64, sha256: sha, jobId: "job-1", responseJson: pathToFileURL(response).href };
  const good = verifyDoc({ props: [row] });
  if (good.failures.length || good.checked !== 1) throw new Error("good manifest failed: " + JSON.stringify(good));
  const badSha = verifyDoc({ props: [{ ...row, sha256: "0".repeat(64) }] });
  if (!badSha.failures.some((f) => f.includes("sha256"))) throw new Error("bad sha not detected");
  const short = path.join(dir, "bota_prop_short", "bota_prop_short.glb");
  fs.mkdirSync(path.dirname(short), { recursive: true });
  fs.writeFileSync(short, buf.subarray(0, 32));
  const badHeader = verifyDoc({ props: [{ ...row, slug: "short", outputGlb: pathToFileURL(short).href }] });
  if (!badHeader.failures.some((f) => f.includes("glTF"))) throw new Error("truncated glb not detected");
  const missing = verifyDoc({ props: [{ ...row, slug: "absent", outputGlb: pathToFileURL(path.join(dir, "absent.glb")).href }] });
  if (!missing.failures.some((f) => f.includes("missing") || f.includes("glb path"))) throw new Error("missing glb not detected");
  fs.rmSync(dir, { recursive: true, force: true });
  console.log("SELF TEST: PASS file:// witnesses good/bad-sha/truncated/missing");
}

const args = process.argv.slice(2);
const manifestFlag = args.indexOf("--manifests");
const usage = "usage: verify-props.mjs [--self-test | --manifests <path>...]";
if (args[0] === "--self-test" && args.length === 1) {
  selfTest();
} else if (manifestFlag >= 0) {
  const docs = args.slice(manifestFlag + 1);
  if (!docs.length) {
    console.error(usage);
    process.exitCode = 2;
  } else {
    let failed = 0;
    for (const value of docs) {
      try {
        const result = verifyDoc(readDoc(value));
        console.log(value + " rows=" + result.checked + " bytes=" + result.totalBytes + " failures=" + result.failures.length);
        for (const failure of result.failures) console.error("  " + failure);
        if (result.failures.length) failed++;
      } catch (err) {
        failed++;
        console.error(value + ": " + String(err.message).slice(0, 160));
      }
    }
    if (failed) process.exitCode = 1;
    else console.log("RESULT: PASS " + docs.length + " manifest(s) verified offline");
  }
} else if (args.length) {
  console.error(usage);
  process.exitCode = 2;
} else {
  selfTest();
  console.log("SKIPPED real-manifest verification: pass --manifests <path>... to check docs/bota-props-*.json against host GLBs");
}
