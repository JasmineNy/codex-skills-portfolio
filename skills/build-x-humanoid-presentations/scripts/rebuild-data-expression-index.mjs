#!/usr/bin/env node

import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import { createReadStream } from "node:fs";
import { mkdir, mkdtemp, readFile, readdir, rm, stat, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillDir = path.dirname(scriptDir);

function parseArgs(argv) {
  const args = {
    pptx: path.join(skillDir, "assets", "data-analysis-reference.pptx"),
    out: path.join(skillDir, "references", "data-expression-index.json"),
  };
  for (let index = 0; index < argv.length; index += 1) {
    const token = argv[index];
    if (token === "--pptx") args.pptx = path.resolve(argv[++index]);
    else if (token === "--out") args.out = path.resolve(argv[++index]);
    else if (token === "--help" || token === "-h") {
      console.log("Usage: node scripts/rebuild-data-expression-index.mjs [--pptx <file>] [--out <file>]");
      process.exit(0);
    } else {
      throw new Error(`Unknown argument: ${token}`);
    }
  }
  return args;
}

function numericSuffix(name) {
  return Number(name.match(/(\d+)(?=\D*$)/)?.[1] || 0);
}

function decodeXml(value) {
  return value
    .replace(/&#x([0-9a-f]+);/gi, (_, hex) => String.fromCodePoint(Number.parseInt(hex, 16)))
    .replace(/&#(\d+);/g, (_, number) => String.fromCodePoint(Number(number)))
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&apos;/g, "'")
    .replace(/&amp;/g, "&");
}

function attribute(tag, name) {
  const match = tag.match(new RegExp(`(?:^|\\s)${name}="([^"]*)"`));
  return match ? decodeXml(match[1]) : undefined;
}

function unique(values) {
  return [...new Set(values.filter(Boolean))];
}

function sha256(filePath) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256");
    const stream = createReadStream(filePath);
    stream.on("data", (chunk) => hash.update(chunk));
    stream.on("end", () => resolve(hash.digest("hex")));
    stream.on("error", reject);
  });
}

function inspectChart(xml, fileName) {
  const types = unique([...xml.matchAll(/<c:([A-Za-z0-9]+Chart)\b/g)].map((match) => match[1]));
  const pointCounts = [...xml.matchAll(/<c:ptCount\b[^>]*\bval="(\d+)"/g)].map((match) => Number(match[1]));
  const grouping = unique([...xml.matchAll(/<c:grouping\b[^>]*\bval="([^"]+)"/g)].map((match) => match[1]));
  const barDirections = unique([...xml.matchAll(/<c:barDir\b[^>]*\bval="([^"]+)"/g)].map((match) => match[1]));
  return {
    file: fileName,
    types: types.length ? types : ["unknown"],
    seriesCount: (xml.match(/<c:ser\b/g) || []).length,
    pointCount: pointCounts.length ? Math.max(...pointCounts) : 0,
    grouping,
    barDirections,
  };
}

function patternForTypes(types) {
  const patterns = [];
  if (types.includes("barChart")) patterns.push("category-comparison");
  if (types.includes("lineChart")) patterns.push("time-series-or-trend");
  if (types.includes("areaChart")) patterns.push("cumulative-trend-or-composition");
  if (types.some((type) => ["pieChart", "doughnutChart", "ofPieChart"].includes(type))) {
    patterns.push("part-to-whole");
  }
  if (types.includes("scatterChart")) patterns.push("correlation-or-distribution");
  if (types.includes("bubbleChart")) patterns.push("portfolio-or-three-variable-comparison");
  if (types.includes("radarChart")) patterns.push("multi-factor-profile");
  if (types.includes("stockChart")) patterns.push("range-or-financial-trend");
  if (types.includes("surfaceChart")) patterns.push("three-dimensional-response-surface");
  if (types.includes("barChart") && types.includes("lineChart")) patterns.push("volume-rate-combination");
  return unique(patterns.length ? patterns : ["layout-or-logic-reference"]);
}

function recommendedVolume(types) {
  if (types.includes("bubbleChart")) return "At least 10 observations and 3 numeric variables";
  if (types.includes("scatterChart")) return "At least 6 comparable observations with numeric x and y values";
  if (types.some((type) => ["pieChart", "doughnutChart", "ofPieChart"].includes(type))) {
    return "3-5 mutually exclusive categories that sum to 100%";
  }
  if (types.includes("lineChart") || types.includes("areaChart")) return "At least 4 ordered time points per series";
  if (types.includes("barChart")) return "2-6 categories per series; split, rank, or aggregate when categories exceed 6";
  return "Match the information volume; remove unused modules instead of fabricating data";
}

function mediaExtension(target) {
  return path.extname(target.split("?")[0]).toLowerCase();
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const sourceStat = await stat(args.pptx);
  if (!sourceStat.isFile()) throw new Error(`Missing PPTX: ${args.pptx}`);

  const zipListing = execFileSync("unzip", ["-Z1", args.pptx], {
    encoding: "utf8",
    maxBuffer: 64 * 1024 * 1024,
  });
  const zipNames = zipListing.split(/\r?\n/).filter(Boolean);
  const slideNames = zipNames.filter((name) => /^ppt\/slides\/slide\d+\.xml$/.test(name));
  const chartNames = zipNames.filter((name) => /^ppt\/charts\/chart\d+\.xml$/.test(name));
  const embeddingNames = zipNames.filter((name) => name.startsWith("ppt/embeddings/") && !name.endsWith("/"));
  const mediaNames = zipNames.filter((name) => name.startsWith("ppt/media/") && !name.endsWith("/"));

  const tempDir = await mkdtemp(path.join(os.tmpdir(), "x-humanoid-ppt-index-"));
  try {
    const extraction = spawnSync(
      "unzip",
      [
        "-qq",
        "-o",
        args.pptx,
        "ppt/slides/slide*.xml",
        "ppt/slides/_rels/slide*.xml.rels",
        "ppt/charts/chart*.xml",
        "-d",
        tempDir,
      ],
      { encoding: "utf8", maxBuffer: 64 * 1024 * 1024 },
    );
    if (extraction.status !== 0) {
      throw new Error(`unzip extraction failed: ${extraction.stderr || extraction.stdout}`);
    }

    const chartDir = path.join(tempDir, "ppt", "charts");
    const chartFiles = (await readdir(chartDir)).filter((name) => /^chart\d+\.xml$/.test(name)).sort((a, b) => numericSuffix(a) - numericSuffix(b));
    const chartByFile = new Map();
    const chartTypeCounts = {};
    for (const fileName of chartFiles) {
      const xml = await readFile(path.join(chartDir, fileName), "utf8");
      const info = inspectChart(xml, fileName);
      chartByFile.set(fileName, info);
      for (const type of info.types) chartTypeCounts[type] = (chartTypeCounts[type] || 0) + 1;
    }

    const slides = [];
    for (const zipSlideName of slideNames.sort((a, b) => numericSuffix(a) - numericSuffix(b))) {
      const slideNumber = numericSuffix(zipSlideName);
      const slideFile = `slide${slideNumber}.xml`;
      const slideXml = await readFile(path.join(tempDir, "ppt", "slides", slideFile), "utf8");
      const relsPath = path.join(tempDir, "ppt", "slides", "_rels", `${slideFile}.rels`);
      let relsXml = "";
      try {
        relsXml = await readFile(relsPath, "utf8");
      } catch {
        relsXml = "";
      }

      const relationships = new Map();
      for (const match of relsXml.matchAll(/<Relationship\b[^>]*\/?\s*>/g)) {
        const tag = match[0];
        const id = attribute(tag, "Id");
        if (!id) continue;
        relationships.set(id, {
          type: attribute(tag, "Type") || "",
          target: attribute(tag, "Target") || "",
        });
      }

      const chartFilesOnSlide = [];
      for (const match of slideXml.matchAll(/<c:chart\b[^>]*\br:id="([^"]+)"/g)) {
        const rel = relationships.get(match[1]);
        if (rel?.target) chartFilesOnSlide.push(path.basename(rel.target));
      }
      const charts = unique(chartFilesOnSlide).map((fileName) => chartByFile.get(fileName)).filter(Boolean);
      const chartTypes = unique(charts.flatMap((chart) => chart.types));

      const textRuns = [...slideXml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)]
        .map((match) => decodeXml(match[1]).replace(/\s+/g, " ").trim())
        .filter(Boolean);
      const title = textRuns[0] || `Slide ${slideNumber}`;
      const textPreview = textRuns.join(" | ").slice(0, 500);

      const compatibilityReasons = [];
      const relatedMedia = [];
      for (const rel of relationships.values()) {
        if (!rel.type.endsWith("/image")) continue;
        relatedMedia.push(rel.target);
        const extension = mediaExtension(rel.target);
        if ([".emf", ".wmf", ".eps"].includes(extension)) {
          compatibilityReasons.push(`unsupported-or-fragile-media:${extension.slice(1)}`);
        }
      }
      if (/<(?:a|c):pattFill\b/.test(slideXml)) compatibilityReasons.push("pattern-fill");
      if ([...relationships.values()].some((rel) => /\/chartEx$/.test(rel.type))) {
        compatibilityReasons.push("extended-chart");
      }

      const compatibilityStatus = compatibilityReasons.length
        ? "logic-reference-only"
        : charts.length
          ? "chart-structure-reusable"
          : "layout-reference-only";

      slides.push({
        slideNumber,
        title,
        textPreview,
        chartCount: charts.length,
        chartTypes,
        charts,
        analysisPatterns: patternForTypes(chartTypes),
        recommendedDataVolume: recommendedVolume(chartTypes),
        relatedMedia: unique(relatedMedia),
        compatibility: {
          status: compatibilityStatus,
          directChartReuseAllowed: compatibilityStatus === "chart-structure-reusable",
          assessment: "static-ooxml",
          reasons: unique(compatibilityReasons),
        },
      });
    }

    const output = {
      schema: "x-humanoid/data-expression-index/v1",
      generatedAt: new Date().toISOString(),
      source: {
        asset: path.relative(skillDir, args.pptx),
        fileName: path.basename(args.pptx),
        byteLength: sourceStat.size,
        modifiedAt: sourceStat.mtime.toISOString(),
        sha256: await sha256(args.pptx),
      },
      summary: {
        slideCount: slideNames.length,
        chartCount: chartNames.length,
        embeddingCount: embeddingNames.length,
        mediaCount: mediaNames.length,
        indexedSlideCount: slides.length,
        slidesWithCharts: slides.filter((slide) => slide.chartCount > 0).length,
        compatibilityCounts: slides.reduce((counts, slide) => {
          const status = slide.compatibility.status;
          counts[status] = (counts[status] || 0) + 1;
          return counts;
        }, {}),
        chartTypeCounts,
      },
      slides,
    };

    await mkdir(path.dirname(args.out), { recursive: true });
    await writeFile(args.out, `${JSON.stringify(output, null, 2)}\n`, "utf8");
    console.log(JSON.stringify(output.summary, null, 2));
    console.log(`Wrote ${args.out}`);
  } finally {
    await rm(tempDir, { recursive: true, force: true });
  }
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
