// Akeso Body System Explorer: the 3D view (three.js), bundled into one file
// with esbuild so it runs offline inside the app's built-in browser.
//
// Python drives it through window.akeso (setLayer, focus, setTheme,
// clearSelection) and hears back through the Qt web channel "bridge"
// (ready, partSelected, regionChanged). Models: BodyParts3D,
// (c) The Database Center for Life Science (CC BY 4.0).

import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader.js";
import { MeshoptDecoder } from "three/examples/jsm/libs/meshopt_decoder.module.js";

const BASE = "";      // relative: akeso://anatomy/ in the app, any folder in tests
const LAYERS = ["skin", "muscle", "bone", "organ"];          // outer -> inner
const SYSTEM_COLOURS = {
  nervous: 0xf2b8c6, cardiovascular: 0xc0392b, respiratory: 0xf5a3a3,
  digestive: 0xd9915a, urinary: 0xe0c060, endocrine: 0xa98bd8,
};
const LAYER_COLOURS = { skin: 0xe8b99a, muscle: 0xb04a4a, bone: 0xeee6d2 };

let bridge = null, parts = {}, regions = {};
let theme = { bg: "#0d0d13", dark: true };
let highlight = 0x6c5ce7;               // selection glow: the theme's accent
const meshes = [];                      // every part mesh
const byLayer = { skin: [], muscle: [], bone: [], organ: [] };
let layerValue = 0, region = "body", selected = null, hovered = null;
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
  const moving = controls.update();
  renderer.render(scene, camera);
  if (flying || moving) requestRender();
}
controls.addEventListener("change", requestRender);

// ------------------------------------------------------------- materials
function material(part) {
  const colour = part.layer === "organ" ? (SYSTEM_COLOURS[part.system] || 0xcc8888)
                                        : LAYER_COLOURS[part.layer];
  return new THREE.MeshStandardMaterial({
    color: colour, roughness: part.layer === "bone" ? 0.75 : 0.55,
    metalness: 0.0, transparent: true, opacity: 1, side: THREE.DoubleSide,
  });
}

function applyLayers() {
  const hidden = new Set(), ghosts = new Set();
  for (const e of entries.values()) for (const id of e.ids) (e.kind === "hide" ? hidden : ghosts).add(id);
  LAYERS.forEach((name, i) => {
    // Each layer fades out while the slider moves from i to i + 1; organs stay.
    const layerOpacity = i === 3 ? 1 : Math.max(0, Math.min(1, 1 - (layerValue - i)));
    for (const m of byLayer[name]) {
      let opacity = isolated ? (isolated.ids.has(m.name) ? 1 : 0) : layerOpacity;
      if (hidden.has(m.name)) opacity = 0;
      else if (ghosts.has(m.name)) opacity = Math.min(opacity, 0.16);   // see-through
      m.visible = opacity > 0.02;
      m.material.opacity = opacity;
      m.material.depthWrite = opacity > 0.98;
      m.renderOrder = opacity > 0.98 ? 0 : 10 - i;
    }
  });
  if (hovered && !hovered.visible) {               // its name tag must not linger
    hovered = null;
    const tip = document.getElementById("tip");
    if (tip) tip.style.display = "none";
  }
  requestRender();
}

// ------------------------------------------------- hide / see-through / show only
function idsFor(id, whole) {
  const p = parts[id] || {};
  if (!whole) return [id];
  // the whole organ or bone group ("skull", "heart"), or every piece with the same name
  const key = p.group_fma ? "group_fma" : "fma", value = p[key];
  return Object.keys(parts).filter(k => parts[k][key] === value);
}
function labelFor(id, whole) {
  const p = parts[id] || {};
  const text = whole && p.group ? p.group : (p.name || id);
  return text.charAt(0).toUpperCase() + text.slice(1);
}
function report() {
  if (!bridge) return;
  bridge.visibilityChanged(JSON.stringify({
    entries: [...entries.entries()].map(([key, e]) => ({ key, label: e.label, kind: e.kind, count: e.ids.size })),
    isolated: isolated ? isolated.label : null,
  }));
}
function hidePart(id, whole) {
  if (!parts[id]) return;
  const key = `hide:${whole ? "g:" : ""}${id}`;
  entries.set(key, { label: labelFor(id, whole), kind: "hide", ids: new Set(idsFor(id, whole)) });
  if (selected && entries.get(key).ids.has(selected.name)) clearSelection();
  applyLayers(); report();
}
function ghostPart(id, whole) {
  if (!parts[id]) return;
  const key = `ghost:${whole ? "g:" : ""}${id}`;
  if (entries.has(key)) entries.delete(key);            // pressing again makes it solid
  else entries.set(key, { label: labelFor(id, whole), kind: "ghost", ids: new Set(idsFor(id, whole)) });
  applyLayers(); report();
}
function isolatePart(id, whole) {
  if (!parts[id]) return;
  isolated = { label: labelFor(id, whole), ids: new Set(idsFor(id, whole)) };
  applyLayers(); report();
  const box = new THREE.Box3();
  for (const m of meshes) if (isolated.ids.has(m.name)) box.expandByObject(m);
  if (!box.isEmpty()) flyToBox(box, null);
}
function restore(key) { entries.delete(key); applyLayers(); report(); }
function showAll() { entries.clear(); isolated = null; applyLayers(); report(); }
function clearSelection() { if (selected) setEmissive(selected, false); selected = null; requestRender(); }

window.addEventListener("keydown", e => {
  const k = e.key.toLowerCase();
  if (k === "r") { showAll(); return; }
  if (k === "escape") { clearSelection(); return; }
  if (!selected) return;
  // Shift = the whole group (all of the skull, the whole heart...)
  if (k === "h") hidePart(selected.name, e.shiftKey);
  else if (k === "t") ghostPart(selected.name, e.shiftKey);
  else if (k === "o") isolatePart(selected.name, e.shiftKey);
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
    if (hovered && hovered !== selected) setEmissive(hovered, false);
    hovered = mesh;
    if (hovered && hovered !== selected) setEmissive(hovered, true, 0.25);
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
  if (hovered && hovered !== selected) setEmissive(hovered, false);
  hovered = null; requestRender();
});

function select(mesh) {
  if (selected) setEmissive(selected, false);
  selected = mesh;
  setEmissive(selected, true, 0.7);
  requestRender();
  const p = Object.assign({ id: mesh.name }, parts[mesh.name] || {});
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
        obj.material = material(part);
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
  if (bridge) bridge.ready();
}

// ------------------------------------------------------------ API for Python
window.akeso = {
  setLayer(v) { layerValue = Math.max(0, Math.min(3, Number(v))); applyLayers(); },
  focus(key) { focus(key); },
  clearSelection() { clearSelection(); },
  hide(id, whole) { hidePart(id, !!whole); },
  ghost(id, whole) { ghostPart(id, !!whole); },
  isolate(id, whole) { isolatePart(id, !!whole); },
  restore(key) { restore(key); },
  showAll() { showAll(); },
  setTheme(bg, dark, accent) {
    theme = { bg, dark };
    if (accent) highlight = new THREE.Color(accent).getHex();
    if (selected) setEmissive(selected, true, 0.7);
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
