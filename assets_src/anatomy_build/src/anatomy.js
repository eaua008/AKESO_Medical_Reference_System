// Akeso Body System Explorer: the 3D view (three.js), bundled into one file
// with esbuild so it runs offline inside the app's built-in browser.
//
// Python drives it through window.akeso (setLayer, focus, setTheme, isolateSystem,
// clearSelection, setExtra, setColor, findParts...) and hears back through the Qt web
// channel "bridge" (ready, partSelected, regionChanged, extraLoaded, extraFailed,
// coloursChanged). Models: BodyParts3D,
// (c) The Database Center for Life Science (CC BY 4.0).

import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/examples/jsm/libs/meshopt_decoder.module.js";

const BASE = "";      // relative: akeso://anatomy/ in the app, any folder in tests
const LAYERS = ["skin", "muscle", "bone", "organ"];          // outer -> inner
const SYSTEM_COLOURS = {
  nervous: 0xf2b8c6, cardiovascular: 0xc0392b, respiratory: 0xf5a3a3,
  digestive: 0xd9915a, urinary: 0xe0c060, endocrine: 0xa98bd8, reproductive: 0xd98fb0,
};
const LAYER_COLOURS = { skin: 0xe8b99a, muscle: 0xb04a4a, bone: 0xeee6d2 };
// Blood vessels and nerves: switched on separately (not part of the peel
// slider), loaded the first time they are switched on, and colour coded.
const EXTRAS = ["vessel", "nerve"];
// Textbook colours: oxygen-rich blood red, oxygen-poor blue. The lung
// arteries carry oxygen-poor blood (blue) and the lung veins oxygen-rich (red).
const KIND_DEFAULTS = {
  artery: "#d63031", vein: "#2e6bd9", pulmonary_artery: "#2e6bd9",
  pulmonary_vein: "#d63031", portal_vein: "#8e44ad", nerve: "#f1c40f",
};
let kindColours = { ...KIND_DEFAULTS };  // the user can change a whole kind...
let custom = {};                         // ...or single vessels: part id -> "#rrggbb"
const extraOn = { vessel: false, nerve: false };
const extraLoading = {};                 // name -> Promise while loading
let started = false;                     // the four main layers are in

let bridge = null, parts = {}, regions = {};
let theme = { bg: "#0d0d13", dark: true };
let highlight = 0x6c5ce7;               // selection glow: the theme's accent
const meshes = [];                      // every part mesh
const byLayer = { skin: [], muscle: [], bone: [], organ: [], vessel: [], nerve: [] };
let layerValue = 0, region = "body", selected = null, hovered = null;
// Parts lit up by a search (a whole group such as "heart" can be several
// meshes). They pulse for a moment so the eye finds them, then stay lit
// like a selection until something else is selected.
let glowing = [], pulse = null;
const PULSE_MS = 2600;
function lit(mesh) { return mesh === selected || glowing.includes(mesh); }
// Parts the user hid or made see-through: key -> {label, kind, ids}
const entries = new Map();
let isolated = null;                    // {label, ids} while "Show only" is on

// ------------------------------------------------------------- scene
const canvas = document.getElementById("view");
let renderer;
try {
  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: false });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
} catch (err) {
  // No WebGL (no graphics acceleration, or it is switched off).
  window.__noWebGL = true;
  document.getElementById("status").textContent =
    "This computer can't show the 3D body (graphics acceleration / WebGL is unavailable). " +
    "You can still browse by body system on the right.";
  renderer = { setPixelRatio() {}, setSize() {}, render() {} };
}
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(35, 1, 5, 20000);
const controls = new OrbitControls(camera, canvas);
controls.enableDamping = true;
controls.dampingFactor = 0.12;
controls.minDistance = 120;
controls.maxDistance = 6000;
scene.add(new THREE.HemisphereLight(0xffffff, 0x445066, 1.6));
const key = new THREE.DirectionalLight(0xffffff, 1.6);
key.position.set(600, 900, 1400);
scene.add(key);
const rim = new THREE.DirectionalLight(0xbfd4ff, 0.7);
rim.position.set(-900, 400, -1200);
scene.add(rim);

// BodyParts3D is in millimetres with Z up and the face towards -Y.
// Turn it so Y is up and the face looks at the camera (+Z), centred.
const body = new THREE.Group();
body.rotation.x = -Math.PI / 2;
scene.add(body);
let centre = new THREE.Vector3(0, -100, 780);
function toWorld(x, y, z) {               // model coords -> world coords
  return new THREE.Vector3(x - centre.x, z - centre.z, -(y - centre.y));
}

function resize() {
  const w = canvas.clientWidth, h = canvas.clientHeight;
  renderer.setSize(w, h, false);
  camera.aspect = w / Math.max(h, 1);
  camera.updateProjectionMatrix();
  requestRender();
}
window.addEventListener("resize", resize);

// ------------------------------------------------------ render on demand
let pending = false, flying = null;
function requestRender() {
  if (!pending) { pending = true; requestAnimationFrame(frame); }
}
function frame(t) {
  pending = false;
  if (flying) {
    const k = Math.min(1, (t - flying.start) / flying.ms);
    const e = k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2;
    camera.position.lerpVectors(flying.fromPos, flying.toPos, e);
    controls.target.lerpVectors(flying.fromTarget, flying.toTarget, e);
    if (k >= 1) flying = null;
  }
  if (pulse) {
    const k = (t - pulse.start) / PULSE_MS;
    const strength = k >= 1 ? 0.7 : 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(k * Math.PI * 7));
    for (const m of glowing) setEmissive(m, true, strength);
    if (k >= 1) pulse = null;
  }
  const moving = controls.update();
  renderer.render(scene, camera);
  if (flying || moving || pulse) requestRender();
}
controls.addEventListener("change", requestRender);

// ------------------------------------------------------------- materials
function kindOf(part) {
  if (part.layer === "nerve") return "nerve";
  return part.layer === "vessel" ? (part.vtype || "artery") : null;
}
function colourFor(id) {                     // "#rrggbb" for vessels and nerves
  const part = parts[id] || {};
  const kind = kindOf(part);
  if (!kind) return null;
  return custom[id] || kindColours[kind] || KIND_DEFAULTS[kind];
}
function material(part, id) {
  const coded = colourFor(id);
  const colour = coded ? new THREE.Color(coded)
               : part.layer === "organ" ? (SYSTEM_COLOURS[part.system] || 0xcc8888)
                                        : LAYER_COLOURS[part.layer];
  return new THREE.MeshStandardMaterial({
    color: colour, roughness: part.layer === "bone" ? 0.75 : coded ? 0.45 : 0.55,
    metalness: 0.0, transparent: true, opacity: 1, side: THREE.DoubleSide,
  });
}

let hairOn = false;
function applyLayers() {
  const hidden = new Set(), ghosts = new Set();
  for (const e of entries.values()) for (const id of e.ids) (e.kind === "hide" ? hidden : ghosts).add(id);
  LAYERS.forEach((name, i) => {
    // Each layer fades out while the slider moves from i to i + 1; organs stay.
    const layerOpacity = i === 3 ? 1 : Math.max(0, Math.min(1, 1 - (layerValue - i)));
    for (const m of byLayer[name]) {
      let opacity = isolated ? (isolated.ids.has(m.name) ? 1 : 0) : layerOpacity;
      if (parts[m.name] && parts[m.name].hair && !hairOn) opacity = 0;   // hair stays off until asked for
      if (hidden.has(m.name)) opacity = 0;
      else if (ghosts.has(m.name)) opacity = Math.min(opacity, 0.16);   // see-through
      m.visible = opacity > 0.02;
      m.material.opacity = opacity;
      m.material.depthWrite = opacity > 0.98;
      m.renderOrder = opacity > 0.98 ? 0 : 10 - i;
      if (glowing.includes(m)) m.renderOrder = 999;       // a searched part stays on top
    }
  });
  for (const name of EXTRAS) {
    for (const m of byLayer[name]) {
      let opacity = isolated ? (isolated.ids.has(m.name) ? 1 : 0) : (extraOn[name] ? 1 : 0);
      if (hidden.has(m.name)) opacity = 0;
      else if (ghosts.has(m.name)) opacity = Math.min(opacity, 0.16);
      m.visible = opacity > 0.02;
      m.material.opacity = opacity;
      m.material.depthWrite = opacity > 0.98;
      m.renderOrder = opacity > 0.98 ? 0 : 6;
      if (glowing.includes(m)) m.renderOrder = 999;       // a searched part stays on top
    }
  }
  if (hovered && !hovered.visible) {               // its name tag must not linger
    hovered = null;
    const tip = document.getElementById("tip");
    if (tip) tip.style.display = "none";
  }
  requestRender();
}

// ------------------------------------------------- hide / see-through / show only
// Groups: every part carries a CHAIN of groups, smallest to largest (parts.json
// "groups"), plus alternative groupings ("alt", e.g. teeth by type). Hide /
// See-through / Only this act on one part, or on the group level that is picked.
const groupCache = new Map();
function idsInGroup(gid) {
  if (!groupCache.has(gid)) {
    groupCache.set(gid, Object.keys(parts).filter(k =>
      (parts[k].groups || []).some(g => g.id === gid) || (parts[k].alt || []).some(g => g.id === gid)));
  }
  return groupCache.get(gid);
}
function groupLabelOf(id, gid) {
  const p = parts[id] || {};
  const g = [...(p.groups || []), ...(p.alt || [])].find(x => x.id === gid);
  return g ? g.label : "";
}
let level = null;                  // the picked group level for the selected part (null = smallest)
function defaultGroup(id) {
  const chain = (parts[id] || {}).groups || [];
  return chain.length ? chain[0].id : null;
}
function groupFor(id, gid) {
  const p = parts[id] || {};
  const known = g => g && [...(p.groups || []), ...(p.alt || [])].some(x => x.id === g);
  if (known(gid)) return gid;
  if (known(level)) return level;
  return defaultGroup(id);
}
function idsFor(id, whole, gid) {
  if (!whole) return [id];
  const g = groupFor(id, gid);
  if (g) return idsInGroup(g);
  const p = parts[id] || {};
  // no chain: the old single group, or every piece with the same name
  const key = p.group_fma ? "group_fma" : "fma", value = p[key];
  return Object.keys(parts).filter(k => parts[k][key] === value);
}
function labelFor(id, whole, gid) {
  const p = parts[id] || {};
  const g = whole ? groupFor(id, gid) : null;
  const text = whole ? ((g && groupLabelOf(id, g)) || p.group || p.name || id) : (p.name || id);
  return text.charAt(0).toUpperCase() + text.slice(1);
}
function keyFor(kind, id, whole, gid) {
  return `${kind}:${whole ? "g:" + (groupFor(id, gid) || id) : id}`;
}
function report() {
  if (!bridge) return;
  bridge.visibilityChanged(JSON.stringify({
    entries: [...entries.entries()].map(([key, e]) => ({ key, label: e.label, kind: e.kind, count: e.ids.size, whole: !!e.whole })),
    isolated: isolated ? isolated.label : null,
  }));
}
function hidePart(id, whole, gid) {
  if (!parts[id]) return;
  const key = keyFor("hide", id, whole, gid);
  entries.set(key, { label: labelFor(id, whole, gid), kind: "hide", whole: !!whole, ids: new Set(idsFor(id, whole, gid)) });
  if (selected && entries.get(key).ids.has(selected.name)) clearSelection();
  applyLayers(); report();
}
function ghostPart(id, whole, gid) {
  if (!parts[id]) return;
  const key = keyFor("ghost", id, whole, gid);
  if (entries.has(key)) entries.delete(key);            // pressing again makes it solid
  else entries.set(key, { label: labelFor(id, whole, gid), kind: "ghost", whole: !!whole, ids: new Set(idsFor(id, whole, gid)) });
  applyLayers(); report();
}
function isolateIds(label, ids) {
  isolated = { label, ids: new Set(ids) };
  applyLayers(); report();
  const box = new THREE.Box3();
  for (const m of meshes) if (isolated.ids.has(m.name)) box.expandByObject(m);
  if (!box.isEmpty()) flyToBox(box, null);
}
function isolatePart(id, whole, gid) {
  if (!parts[id]) return;
  isolateIds(labelFor(id, whole, gid), idsFor(id, whole, gid));
}
// a whole group by its id (from the search box)
function groupAction(kind, gid, label) {
  const ids = idsInGroup(gid);
  if (!ids.length) return;
  const text = label || groupLabelOf(ids[0], gid) || gid;
  if (kind === "isolate") { isolateIds(text, ids); return; }
  entries.set(`${kind}:g:${gid}`, { label: text, kind, whole: true, ids: new Set(ids) });
  applyLayers(); report();
}
// Tint every part of a group, so the student sees what a level will affect.
let previewMeshes = [], previewTimer = null;
function clearPreview() {
  if (previewTimer) { clearTimeout(previewTimer); previewTimer = null; }
  for (const m of previewMeshes) if (m !== selected && !glowing.includes(m)) setEmissive(m, false);
  previewMeshes = [];
  requestRender();
}
function previewGroup(gid, ms) {
  clearPreview();
  if (!gid) return;
  const ids = new Set(idsInGroup(gid));
  previewMeshes = meshes.filter(m => ids.has(m.name) && m.visible && m !== selected);
  for (const m of previewMeshes) setEmissive(m, true, 0.4);
  requestRender();
  if (ms) previewTimer = setTimeout(clearPreview, ms);
}
function setLevel(gid, quiet) {
  level = gid || null;
  if (!quiet && bridge && bridge.levelChanged) bridge.levelChanged(level || "");
  previewGroup(level, 1600);
}
function moveLevel(step) {              // ] broader, [ narrower
  if (!selected) return;
  const chain = (parts[selected.name] || {}).groups || [];
  if (!chain.length) return;
  let i = chain.findIndex(g => g.id === (level || chain[0].id));
  if (i < 0) i = 0;
  setLevel(chain[Math.max(0, Math.min(chain.length - 1, i + step))].id);
}
// "Focus on system": only the parts of one body system (Python turns on the
// vessels / nerves layer first when the system needs it).
function isolateSystem(system, label) {
  const ids = Object.keys(parts).filter(k => parts[k].system === system);
  if (!ids.length) return;
  isolated = { label, ids: new Set(ids) };
  if (selected && !isolated.ids.has(selected.name)) clearSelection();
  applyLayers(); report();
  const box = new THREE.Box3();
  for (const m of meshes) if (isolated.ids.has(m.name) && m.visible) box.expandByObject(m);
  if (!box.isEmpty()) flyToBox(box, null);
}
function restore(key) { entries.delete(key); applyLayers(); report(); }
function showAll() { entries.clear(); isolated = null; applyLayers(); report(); }
// A searched part can sit behind others (the abdominal aorta behind the
// intestines), so it is drawn on top of everything, x-ray style, while lit.
function xray(mesh, on) {
  mesh.material.depthTest = !on;
  mesh.renderOrder = on ? 999 : (mesh.material.opacity > 0.98 ? 0 : 6);
  mesh.material.needsUpdate = true;
}
function clearGlow() {
  for (const m of glowing) {
    xray(m, false);
    if (m !== selected) setEmissive(m, false);
  }
  glowing = []; pulse = null;
}
function clearSelection() {
  level = null; clearPreview();
  clearGlow();
  if (selected) setEmissive(selected, false);
  selected = null; requestRender();
}

// Search: bring the parts into view, fly to them and make them glow.
// Python has already peeled the slider to their layer; this switches on the
// vessels / nerves layer if needed (waiting for it to load), and un-hides
// the parts if the user hid them or is showing only something else.
async function findParts(ids) {
  ids = ids.filter(id => parts[id]);
  if (!ids.length) return;
  const want = new Set(ids);
  for (const name of EXTRAS) {
    if (!ids.some(id => parts[id].layer === name)) continue;
    if (!extraOn[name]) setExtra(name, true);
    if (extraLoading[name]) {
      try { await extraLoading[name]; } catch (err) { return; }
    }
  }
  for (const [k, e] of [...entries]) if ([...e.ids].some(id => want.has(id))) entries.delete(k);
  if (isolated && !ids.every(id => isolated.ids.has(id))) isolated = null;
  applyLayers(); report();
  body.updateMatrixWorld(true);           // a layer loaded just now has no position yet
  const size = m => new THREE.Box3().setFromObject(m).getSize(new THREE.Vector3()).length();
  // Biggest first, so a whole organ ("heart") shows the heart itself in the
  // Selected card rather than one small valve cusp.
  const found = meshes.filter(m => want.has(m.name)).sort((a, b) => size(b) - size(a));
  if (!found.length) return;
  select(found[0]);                       // fills the Selected card in Akeso
  glowing = found;
  for (const m of found) xray(m, true);
  pulse = { start: performance.now() };
  const box = new THREE.Box3();
  for (const m of found) box.expandByObject(m);
  flyToBox(box, null);
  window.__akesoFound = found.length;     // read by the tests
}

window.addEventListener("keydown", e => {
  const k = e.key.toLowerCase();
  if (k === "r") { showAll(); return; }
  if (k === "escape") { clearSelection(); return; }
  if (!selected) return;
  // Shift = the whole group (all of the skull, the whole heart...)
  if (k === "h") hidePart(selected.name, e.shiftKey, level);
  else if (k === "t") ghostPart(selected.name, e.shiftKey, level);
  else if (k === "o") isolatePart(selected.name, e.shiftKey, level);
  else if (k === "]" || (k === "arrowup" && e.shiftKey)) { moveLevel(1); e.preventDefault(); }
  else if (k === "[" || (k === "arrowdown" && e.shiftKey)) { moveLevel(-1); e.preventDefault(); }
});

// ------------------------------------------------------------ camera
function boxFor(key) {
  const b = regions[key].box;
  const a = toWorld(b[0][0], b[0][1], b[0][2]), c = toWorld(b[1][0], b[1][1], b[1][2]);
  return new THREE.Box3().setFromPoints([a, c]);
}
function focus(key, ms = 750) {
  if (!regions[key]) return;
  region = key;
  flyToBox(boxFor(key), key, ms);
  window.__akesoRegion = key;
  if (bridge) bridge.regionChanged(key);
}
function flyToBox(box, key, ms = 750) {
  if (!key) region = "part";                       // zoomed on one part: clicks select
  
  const size = box.getSize(new THREE.Vector3());
  const target = box.getCenter(new THREE.Vector3());
  const fit = Math.max(size.y, size.x / camera.aspect) / (2 * Math.tan(THREE.MathUtils.degToRad(camera.fov / 2)));
  const dir = camera.position.clone().sub(controls.target).normalize();
  if (dir.lengthSq() < 0.5 || key === "body") dir.set(0, 0.08, 1).normalize();
  const toPos = target.clone().add(dir.multiplyScalar(fit * 1.25 + size.z));
  flying = { start: performance.now(), ms, fromPos: camera.position.clone(), toPos,
             fromTarget: controls.target.clone(), toTarget: target };
  requestRender();
}

function regionAt(world) {
  // back to model coordinates, then match the region boxes
  const x = world.x + centre.x, z = world.y + centre.z;
  if (z >= regions.head.box[0][2] - 10) return "head";
  if (Math.abs(x) > 150 && z > 650) return "arms";
  if (z < 740) return "legs";
  if (z >= 1180) return "chest";
  return "abdomen";
}

// ------------------------------------------------------------ picking
const ray = new THREE.Raycaster(), mouse = new THREE.Vector2();
function pick(event) {
  const r = canvas.getBoundingClientRect();
  mouse.set(((event.clientX - r.left) / r.width) * 2 - 1, -((event.clientY - r.top) / r.height) * 2 + 1);
  ray.setFromCamera(mouse, camera);
  const visible = meshes.filter(m => m.visible && m.material.opacity > 0.35);
  const hit = ray.intersectObjects(visible, false)[0];
  return hit || null;
}
function setEmissive(mesh, on, strength) {
  if (!mesh) return;
  mesh.material.emissive.setHex(on ? highlight : 0x000000);
  mesh.material.emissiveIntensity = on ? strength : 0;
}
let down = null;
canvas.addEventListener("pointerdown", e => { down = [e.clientX, e.clientY]; canvas.focus(); });
canvas.addEventListener("pointerup", e => {
  if (!down || Math.hypot(e.clientX - down[0], e.clientY - down[1]) > 5) return;
  const hit = pick(e);
  if (!hit) return;
  if (region === "body") { focus(regionAt(hit.point)); return; }   // first click: fly in
  select(hit.object);
});
canvas.addEventListener("pointermove", e => {
  if (e.buttons) return;
  const hit = pick(e);
  const mesh = hit ? hit.object : null;
  if (mesh !== hovered) {
    if (hovered && !lit(hovered)) setEmissive(hovered, false);
    hovered = mesh;
    if (hovered && !lit(hovered)) setEmissive(hovered, true, 0.25);
    const tip = document.getElementById("tip");
    if (mesh) {
      const p = parts[mesh.name] || {};
      tip.textContent = region === "body" ? `Zoom in: ${regionAt(hit.point)}` : (p.name || "");
      tip.style.display = "block";
    } else tip.style.display = "none";
    requestRender();
  }
  const tip = document.getElementById("tip");
  tip.style.left = e.clientX + 14 + "px";
  tip.style.top = e.clientY + 12 + "px";
});
canvas.addEventListener("pointerleave", () => {
  document.getElementById("tip").style.display = "none";
  if (hovered && !lit(hovered)) setEmissive(hovered, false);
  hovered = null; requestRender();
});

function select(mesh) {
  level = null; clearPreview();
  clearGlow();
  if (selected) setEmissive(selected, false);
  selected = mesh;
  setEmissive(selected, true, 0.7);
  requestRender();
  const p = Object.assign({ id: mesh.name }, parts[mesh.name] || {});
  const colour = colourFor(mesh.name);
  if (colour) { p.colour = colour; p.kind = kindOf(p); p.custom = !!custom[mesh.name]; }
  window.__akesoLast = p;                     // read by the tests
  if (bridge) bridge.partSelected(JSON.stringify(p));
}

// ------------------------------------------------------------ loading
async function loadJSON(name) { return (await fetch(BASE + name)).json(); }
const loader = new GLTFLoader();
loader.setMeshoptDecoder(MeshoptDecoder);
function loadLayer(name) {
  return new Promise((resolve, reject) => {
    loader.load(BASE + name + ".glb", gltf => {
      gltf.scene.traverse(obj => {
        if (!obj.isMesh) return;
        // gltfpack names the node; meshes under it inherit the part id
        let id = obj.name, n = obj;
        while (n && !parts[id]) { n = n.parent; id = n ? n.name : ""; }
        obj.name = id;
        const part = parts[id] || { layer: name };
        obj.material = material(part, id);
        meshes.push(obj);
        byLayer[name].push(obj);
      });
      body.add(gltf.scene);
      applyLayers();
      resolve();
    }, undefined, reject);
  });
}

async function start() {
  parts = await loadJSON("parts.json");
  regions = await loadJSON("regions.json");
  const b = regions.body.box;
  centre = new THREE.Vector3((b[0][0] + b[1][0]) / 2, (b[0][1] + b[1][1]) / 2, (b[0][2] + b[1][2]) / 2);
  body.position.set(-centre.x, -centre.z, centre.y);   // so toWorld() matches the meshes
  resize();
  focus("body", 1);
  const status = document.getElementById("status");
  for (const name of ["skin", "bone", "organ", "muscle"]) {
    status.textContent = `Loading ${name === "organ" ? "organs" : name}…`;
    await loadLayer(name);
  }
  status.style.display = "none";
  started = true;
  for (const name of EXTRAS) if (extraOn[name]) setExtra(name, true);
  if (bridge) bridge.ready();
}

// ------------------------------------------------------- vessels and nerves
function setExtra(name, on) {
  if (!EXTRAS.includes(name)) return;
  extraOn[name] = !!on;
  if (!started) return;                  // start() loads it after the main layers
  if (on && !byLayer[name].length && !extraLoading[name]) {
    const status = document.getElementById("status");
    status.textContent = name === "vessel" ? "Loading blood vessels…" : "Loading nerves…";
    status.style.display = "block";
    extraLoading[name] = loadLayer(name).then(() => {
      status.style.display = "none";
      window.__akesoExtras = (window.__akesoExtras || 0) + 1;       // read by the tests
      if (bridge) bridge.extraLoaded(name);
    }, err => {
      console.error(`Couldn't load ${name}.glb: ${err && err.message ? err.message : err}`);
      status.textContent = "Couldn't load this layer. Repair Akeso in Settings \u2192 Updates.";
      extraLoading[name] = null;
      if (bridge && bridge.extraFailed) bridge.extraFailed(name);   // Akeso offers Repair
    });
  }
  applyLayers();
}
function recolour() {
  for (const name of EXTRAS) for (const m of byLayer[name]) {
    const c = colourFor(m.name);
    if (c) m.material.color.set(c);
  }
  requestRender();
}
function reportColours() {
  if (bridge) bridge.coloursChanged(JSON.stringify({ kinds: kindColours, custom }));
}
const HEX = /^#[0-9a-fA-F]{6}$/;
function setColour(id, whole, hex) {
  if (!parts[id] || !kindOf(parts[id]) || !HEX.test(hex)) return;
  for (const k of idsFor(id, whole)) custom[k] = hex.toLowerCase();
  recolour(); reportColours();
}
function resetColour(id, whole) {
  if (!parts[id]) return;
  for (const k of idsFor(id, whole)) delete custom[k];
  recolour(); reportColours();
}
function setKindColour(kind, hex) {
  if (!(kind in KIND_DEFAULTS) || !HEX.test(hex)) return;
  kindColours[kind] = hex.toLowerCase();
  recolour(); reportColours();
}
function resetAllColours() {
  kindColours = { ...KIND_DEFAULTS }; custom = {};
  recolour(); reportColours();
}
function setColours(saved) {                 // restore what Python saved last time
  saved = saved || {};
  kindColours = { ...KIND_DEFAULTS };
  for (const [k, v] of Object.entries(saved.kinds || {}))
    if (k in KIND_DEFAULTS && HEX.test(v)) kindColours[k] = v.toLowerCase();
  custom = {};
  for (const [k, v] of Object.entries(saved.custom || {}))
    if (parts[k] && kindOf(parts[k]) && HEX.test(v)) custom[k] = v.toLowerCase();
  recolour();
}

// ------------------------------------------------------------ API for Python
window.akeso = {
  setLayer(v) { layerValue = Math.max(0, Math.min(3, Number(v))); applyLayers(); },
  focus(key) { focus(key); },
  clearSelection() { clearSelection(); },
  findParts(ids) { findParts((ids || []).map(String)); },
  hide(id, whole, gid) { hidePart(id, !!whole, gid || null); },
  ghost(id, whole, gid) { ghostPart(id, !!whole, gid || null); },
  isolate(id, whole, gid) { isolatePart(id, !!whole, gid || null); },
  hideGroup(gid, label) { groupAction("hide", String(gid), label); },
  ghostGroup(gid, label) { groupAction("ghost", String(gid), label); },
  isolateGroup(gid, label) { groupAction("isolate", String(gid), label); },
  setLevel(gid) { setLevel(String(gid || ""), true); },
  previewGroup(gid) { if (gid) previewGroup(String(gid), 0); else clearPreview(); },
  isolateSystem(system, label) { isolateSystem(String(system), String(label || system)); },
  restore(key) { restore(key); },
  showAll() { showAll(); },
  setExtra(name, on) { setExtra(name, on); },
  setHair(on) { hairOn = !!on; applyLayers(); },
  setColor(id, whole, hex) { setColour(id, !!whole, hex); },
  resetColor(id, whole) { resetColour(id, !!whole); },
  setKindColor(kind, hex) { setKindColour(kind, hex); },
  resetAllColors() { resetAllColours(); },
  setColors(saved) { setColours(saved); },
  colours() { return { kinds: kindColours, custom }; },
  setTheme(bg, dark, accent) {
    theme = { bg, dark };
    if (accent) highlight = new THREE.Color(accent).getHex();
    if (selected) setEmissive(selected, true, 0.7);
    for (const m of glowing) setEmissive(m, true, 0.7);
    scene.background = new THREE.Color(bg);
    document.body.style.background = bg;
    document.getElementById("tip").className = dark ? "dark" : "light";
    requestRender();
  },
};
window.akeso.setTheme(theme.bg, theme.dark);

function connect() {
  if (window.qt && window.QWebChannel) {
    new QWebChannel(qt.webChannelTransport, ch => {
      bridge = ch.objects.bridge;
      if (window.__noWebGL) { bridge.webglFailed(); return; }
      start();
    });
  } else if (!window.__noWebGL) {
    start();                                // opened outside the app (tests)
  }
}
connect();
