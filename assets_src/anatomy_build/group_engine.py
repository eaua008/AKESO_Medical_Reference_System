"""Builds each part's group CHAIN from group_rules.py plus the FMA part-of tree.

    parts[fj]["groups"] = [{"id", "label"}, ...]   smallest -> largest, same layer only,
                                                    ends with the whole layer ("All bones")
    parts[fj]["alt"]    = [{"id", "label"}, ...]   alternative groupings (teeth by type...)

Old fields (group_fma, group) are left exactly as they were.
"""

import collections
import csv
import re
import sys

from group_rules import LAYER_LABELS, RULES, SYSTEM_LABELS

MAX_LEVELS = 8
NEAR = 1.15            # a bigger group that adds < 15% more parts is not worth a level
SKIP_AUTO = re.compile(r"^(human body|body|body proper|vasculature of body|trunk|thorax|vascular tree|"
                       r"cardiovascular system|respiratory system|alimentary system|nervous system|"
                       r"musculoskeletal system|skeletal system|skeleton|.*system$|.*tract$|"
                       r"anatomical|set of|segment of|body compartment|compartment of|.*content$|content of|.*segment of trunk|head$|neck$|face$)", re.I)


def side_of(name):
    if re.search(r"\bleft\b", name):
        return "left"
    if re.search(r"\bright\b", name):
        return "right"
    return None


def lower_first(text):
    return text[:1].lower() + text[1:]


def build_groups(parts, el, names, bodyparts_dir):
    groups = {}                       # id -> dict(label, layer, alt, ids, auto)

    def add(gid, label, layer, ids, alt=False, auto=False):
        ids = set(ids)
        if ids:
            groups[gid] = {"label": label, "layer": layer, "alt": alt, "ids": ids, "auto": auto}

    by_layer = collections.defaultdict(set)
    for fj, p in parts.items():
        by_layer[p["layer"]].add(fj)
    nm = {fj: p["name"].lower() for fj, p in parts.items()}
    side = {fj: side_of(nm[fj]) for fj in parts}

    # --- curated: regex rules first, then unions (which may refer to later rules)
    pending = []
    for r in RULES:
        if r.pattern is not None:
            rx = re.compile(r.pattern, re.I)
            ids = {fj for fj in by_layer[r.layer] if rx.search(nm[fj])}
            both = r.both or r.label
            add(r.id, both, r.layer, ids, r.alt)
            if r.sided:
                for s in ("left", "right"):
                    add(f"{r.id}_{s[0]}", f"{s.capitalize()} {lower_first(r.label)}", r.layer,
                        {fj for fj in ids if side[fj] == s}, r.alt)
        else:
            pending.append(r)
    while pending:
        waiting = {r.id for r in pending}
        ready = [r for r in pending if not (set(r.members) & waiting)]
        if not ready:                                   # a loop in the table: give up on the rest
            print("group_rules: unions that could not be resolved:", [r.id for r in pending])
            break
        for r in ready:
            both = r.both or r.label
            ids = set().union(*(groups[m]["ids"] for m in r.members if m in groups))
            add(r.id, both, r.layer, ids, r.alt)
            if r.sided:
                for s in ("left", "right"):
                    got = set()
                    for m in r.members:
                        if f"{m}_{s[0]}" in groups:
                            got |= groups[f"{m}_{s[0]}"]["ids"]
                        elif m in groups:
                            got |= {fj for fj in groups[m]["ids"] if side[fj] == s}
                    add(f"{r.id}_{s[0]}", f"{s.capitalize()} {lower_first(r.label)}", r.layer, got, r.alt)
        pending = [r for r in pending if r not in ready]

    # --- the body system of an organ, the kind of vessel, the whole layer
    for sysname, label in SYSTEM_LABELS.items():
        add(f"sys_{sysname}", label, "organ",
            {fj for fj in by_layer["organ"] if parts[fj]["system"] == sysname})
    vk = lambda *k: {fj for fj in by_layer["vessel"] if parts[fj].get("vtype") in k}
    add("arteries", "All arteries", "vessel", vk("artery", "pulmonary_artery"))
    add("veins", "All veins", "vessel", vk("vein", "pulmonary_vein", "portal_vein"))
    add("pulm_vessels", "Pulmonary vessels", "vessel", vk("pulmonary_artery", "pulmonary_vein"))
    add("portal_vessels", "Portal vein system", "vessel", vk("portal_vein"))
    for layer, label in LAYER_LABELS.items():
        add(f"all_{layer}", label, layer, by_layer[layer])

    # --- automatic: the FMA part-of tree (branches of an artery, parts of the heart...)
    kids = collections.defaultdict(set)
    cname = {}
    path = bodyparts_dir + "partof_inclusion_relation_list.txt.txt"
    for r in list(csv.reader(open(path, encoding="utf-8", errors="replace"), delimiter="\t"))[1:]:
        kids[r[0]].add(r[2]); cname[r[0]] = r[1]; cname[r[2]] = r[3]
    sys.setrecursionlimit(10000)
    memo = {}

    def members(c):
        if c not in memo:
            memo[c] = set(el.get(c, ()))
            for k in kids.get(c, ()):
                memo[c] |= members(k)
        return memo[c]

    for c in list(kids):
        label = cname.get(c, "")
        if not label or SKIP_AUTO.search(label):
            continue
        sub = members(c) & set(parts)
        for layer in ("vessel", "organ", "nerve"):
            ids = {fj for fj in sub if parts[fj]["layer"] == layer}
            if 3 <= len(ids) <= 0.5 * len(by_layer[layer]):
                add(f"fma_{c}_{layer[0]}", label[:1].upper() + label[1:], layer, ids, auto=True)

    # --- the groups the first build already had (heart, lungs, brain, skull...)
    old = collections.defaultdict(set)
    oldname = {}
    for fj, p in parts.items():
        if p.get("group_fma"):
            old[p["group_fma"]].add(fj); oldname[p["group_fma"]] = p.get("group") or p["group_fma"]
    for fma, ids in old.items():
        layers = {parts[fj]["layer"] for fj in ids}
        if len(layers) == 1:
            add(f"old_{fma}", oldname[fma][:1].upper() + oldname[fma][1:], layers.pop(), ids, auto=True)

    # --- chains
    stats = {"no_chain": [], "mixed": []}
    members_of = collections.defaultdict(list)
    for gid, g in groups.items():
        if len(g["ids"]) < 2:
            continue
        mixed = {parts[fj]["layer"] for fj in g["ids"]}
        if mixed != {g["layer"]}:
            stats["mixed"].append(gid)
            continue
        for fj in g["ids"]:
            members_of[fj].append(gid)

    def pick(fj, alt):
        out = [(len(groups[g]["ids"]), groups[g]["auto"], g) for g in members_of[fj]
               if groups[g]["alt"] == alt and not g.startswith(("all_", "sys_"))
               and g not in ("arteries", "veins")]
        out.sort()
        kept = []
        for size, auto, gid in out:
            if kept:
                psize, pauto, pid = kept[-1]
                if groups[gid]["ids"] == groups[pid]["ids"]:
                    if pauto and not auto:
                        kept[-1] = (size, auto, gid)
                    continue
                if not alt and size <= psize * NEAR + 0.5:
                    if pauto and not auto:
                        kept[-1] = (size, auto, gid)
                    continue
            kept.append((size, auto, gid))
        return kept

    for fj, p in parts.items():
        chain = pick(fj, False)
        tail = []
        if p["layer"] == "organ":
            tail.append(f"sys_{p['system']}")
        if p["layer"] == "vessel":
            kind = p.get("vtype")
            if kind in ("pulmonary_artery", "pulmonary_vein"):
                tail.append("pulm_vessels")
            if kind == "portal_vein":
                tail.append("portal_vessels")
            tail.append("arteries" if kind in ("artery", "pulmonary_artery") else "veins")
        tail.append(f"all_{p['layer']}")
        ids = [g for _, _, g in chain]
        # cap the length: drop automatic levels first, then the smallest steps
        while len(ids) + len(tail) > MAX_LEVELS and ids:
            autos = [g for g in ids if groups[g]["auto"]]
            ids.remove(autos[0] if autos else ids[0]) if autos else ids.pop(0)
        for g in tail:
            if g in groups and (not ids or groups[g]["ids"] != groups[ids[-1]]["ids"]) \
                    and (fj in groups[g]["ids"]) and g not in ids:
                ids.append(g)
        # a level that is the same size as the next one up adds nothing
        p["groups"] = [{"id": g, "label": groups[g]["label"]} for g in ids]
        p["alt"] = [{"id": g, "label": groups[g]["label"]} for _, _, g in pick(fj, True)]
        if len(p["groups"]) <= 1:
            stats["no_chain"].append(fj)

    # --- report
    used = {x["id"] for p in parts.values() for x in p["groups"] + p["alt"]}
    per_layer = collections.Counter(groups[g]["layer"] for g in used)
    print("groups used per layer:", dict(per_layer), "total", len(used))
    print("groups that would mix layers:", stats["mixed"] or "none")
    print("parts with no group beyond their layer:", len(stats["no_chain"]))
    by = collections.Counter(parts[f]["layer"] for f in stats["no_chain"])
    print("  by layer:", dict(by))
    for layer in by:
        print("  e.g.", layer, sorted({parts[f]["name"] for f in stats["no_chain"] if parts[f]["layer"] == layer})[:12])
    big = sorted(used, key=lambda g: -len(groups[g]["ids"]))[:30]
    print("30 biggest groups:", [(groups[g]["label"], len(groups[g]["ids"])) for g in big])
    return groups
