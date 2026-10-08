#!/usr/bin/env node
/**
 * amaliyot/<dars>/<loyiha>/ papkalarini yuklab olinadigan zip'ga aylantiradi:
 *   out/amaliyot/<loyiha>.zip
 *
 * Tashqi kutubxonasiz: zip formati qo'lda yoziladi (deflate + CRC32, Node 22+).
 * Sana va tartib qat'iy — bir xil fayllardan har safar bir xil zip chiqadi.
 */
import { readdir, readFile, writeFile, mkdir, stat } from "node:fs/promises";
import { join, relative } from "node:path";
import { deflateRawSync, crc32 } from "node:zlib";

const SRC = "amaliyot";
const OUT = "out/amaliyot";

async function walk(dir) {
  const out = [];
  for (const e of (await readdir(dir, { withFileTypes: true })).sort((a, b) =>
    a.name.localeCompare(b.name),
  )) {
    if (e.name === "__pycache__" || e.name.startsWith(".")) continue;
    const p = join(dir, e.name);
    if (e.isDirectory()) out.push(...(await walk(p)));
    else out.push(p);
  }
  return out;
}

// 2026-01-01 00:00 — DOS sana/vaqt formatida
const DOS_TIME = 0;
const DOS_DATE = ((2026 - 1980) << 9) | (1 << 5) | 1;

function zip(entries) {
  const locals = [];
  const centrals = [];
  let offset = 0;
  for (const { name, data } of entries) {
    const nameBuf = Buffer.from(name, "utf8");
    const packed = deflateRawSync(data, { level: 9 });
    const crc = crc32(data);
    const local = Buffer.alloc(30);
    local.writeUInt32LE(0x04034b50, 0);
    local.writeUInt16LE(20, 4);
    local.writeUInt16LE(0x0800, 6); // UTF-8 nomlar
    local.writeUInt16LE(8, 8); // deflate
    local.writeUInt16LE(DOS_TIME, 10);
    local.writeUInt16LE(DOS_DATE, 12);
    local.writeUInt32LE(crc, 14);
    local.writeUInt32LE(packed.length, 18);
    local.writeUInt32LE(data.length, 22);
    local.writeUInt16LE(nameBuf.length, 26);
    local.writeUInt16LE(0, 28);
    locals.push(local, nameBuf, packed);

    const central = Buffer.alloc(46);
    central.writeUInt32LE(0x02014b50, 0);
    central.writeUInt16LE(20, 4);
    central.writeUInt16LE(20, 6);
    central.writeUInt16LE(0x0800, 8);
    central.writeUInt16LE(8, 10);
    central.writeUInt16LE(DOS_TIME, 12);
    central.writeUInt16LE(DOS_DATE, 14);
    central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(packed.length, 20);
    central.writeUInt32LE(data.length, 24);
    central.writeUInt16LE(nameBuf.length, 28);
    central.writeUInt32LE(offset, 42);
    centrals.push(central, nameBuf);
    offset += local.length + nameBuf.length + packed.length;
  }
  const cd = Buffer.concat(centrals);
  const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50, 0);
  end.writeUInt16LE(entries.length, 8);
  end.writeUInt16LE(entries.length, 10);
  end.writeUInt32LE(cd.length, 12);
  end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, cd, end]);
}

await mkdir(OUT, { recursive: true });
for (const lesson of await readdir(SRC)) {
  if (!(await stat(join(SRC, lesson))).isDirectory()) continue;
  for (const project of await readdir(join(SRC, lesson))) {
    const root = join(SRC, lesson, project);
    if (!(await stat(root)).isDirectory()) continue;
    const files = await walk(root);
    const entries = await Promise.all(
      files.map(async (f) => ({
        name: `${project}/${relative(root, f).split("\\").join("/")}`,
        data: await readFile(f),
      })),
    );
    const buf = zip(entries);
    await writeFile(join(OUT, `${project}.zip`), buf);
    console.log(`${OUT}/${project}.zip — ${files.length} fayl, ${buf.length} bayt`);
  }
}
