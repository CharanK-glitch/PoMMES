#!/usr/bin/env python3
"""Generate plots (e.g. control flow graph) from PoMMES CFG dump files."""
import os
import re
import sys

import matplotlib
matplotlib.use("Agg")  # headless backend
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.path import Path as MPath
from matplotlib.patches import Arc


def read_cfg(path):
    nodes = {}
    edges = []
    with open(path, "r") as f:
        for line in f:
            parts = line.split()
            if not parts:
                continue
            if parts[0] == "n":
                node_id = int(parts[1])
                bb = int(parts[2])
                nodes[node_id] = bb
            elif parts[0] == "e":
                edges.append((int(parts[1]), int(parts[2])))
    return nodes, edges


def compute_layout(node_ids, edges):
    """Simple layered (depth) layout; falls back to index order on cycles."""
    node_ids = sorted(node_ids)
    succ = {n: [] for n in node_ids}
    indeg = {n: 0 for n in node_ids}
    for (a, b) in edges:
        if a in succ and b in indeg:
            succ[a].append(b)
            indeg[b] += 1
    depth = {n: 0 for n in node_ids}
    queue = [n for n in node_ids if indeg[n] == 0]
    visited = set()
    while queue:
        n = queue.pop(0)
        visited.add(n)
        for m in succ[n]:
            depth[m] = max(depth.get(m, 0), depth[n] + 1)
            indeg[m] -= 1
            if indeg[m] == 0:
                queue.append(m)
    for n in node_ids:
        depth.setdefault(n, 0)
    layers = {}
    for n in node_ids:
        layers.setdefault(depth[n], []).append(n)
    pos = {}
    for d, ns in sorted(layers.items()):
        for i, n in enumerate(ns):
            pos[n] = (d * 3.0, i * 1.6)
    return pos


def generate_sensitivity_plot(bb_sens_path, out_png):
    bbs = []
    with open(bb_sens_path, "r") as f:
        for line in f:
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                bb = int(parts[0])
                sens = int(parts[1])
            except ValueError:
                continue
            bbs.append((bb, sens))
    if not bbs:
        raise RuntimeError(f"no basic block sensitivities found in {bb_sens_path}")

    fig, ax = plt.subplots(figsize=(8, 4))
    bbs_sorted = sorted(bbs, key=lambda x: x[0])
    xs = list(range(len(bbs_sorted)))
    sens_vals = [s for (_, s) in bbs_sorted]
    colors = ["red" if s == 1 else "steelblue" for s in sens_vals]
    ax.bar(xs, [1] * len(bbs_sorted), color=colors, edgecolor="black")
    ax.set_xticks([x for x in xs])
    ax.set_xticklabels([f"bb{bb}" for (bb, _) in bbs_sorted], rotation=45, ha="right")
    ax.set_ylim(0, 2)
    ax.set_yticks([0, 1, 2])
    ax.set_title("PoMMES Basic Block Sensitivity (0=public, 1=secret)", fontsize=14)
    ax.set_ylabel("sensitivity")
    outdir = os.path.dirname(out_png)
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)
    plt.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"wrote sensitivity plot -> {out_png}")


def main(cfg_path, out_png):
    nodes, edges = read_cfg(cfg_path)
    pos = compute_layout(list(nodes.keys()), edges)
    node_ids = sorted(nodes.keys())

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-2, max([p[0] for p in pos.values()]) + 2)
    ax.set_ylim(min([p[1] for p in pos.values()]) - 2, max([p[1] for p in pos.values()]) + 2)
    ax.set_aspect("equal")
    ax.axis("off")

    for (a, b) in edges:
        if a not in pos or b not in pos:
            continue
        (x1, y1), (x2, y2) = pos[a], pos[b]
        dx = max(0.2, (x2 - x1) * 0.5)
        ax.annotate(
            "",
            xy=(x2 - dx if x2 > x1 else x2 + dx, y2),
            xytext=(x1 + dx if x1 < x2 else x1 - dx, y1),
            arrowprops=dict(arrowstyle="->", color="black", lw=2.0),
        )

    for n in node_ids:
        x, y = pos[n]
        bb = nodes[n]
        ax.plot([x - 0.35, x + 0.35], [y - 0.2, y - 0.2], "k-", lw=2)
        ax.plot([x - 0.35, x - 0.35], [y - 0.2, y + 0.2], "k-", lw=2)
        ax.plot([x + 0.35, x + 0.35], [y - 0.2, y + 0.2], "k-", lw=2)
        ax.plot([x - 0.35, x + 0.35], [y + 0.2, y + 0.2], "k-", lw=2)
        ax.text(x, y, f"bb{bb}", ha="center", va="center", fontsize=11, fontweight="bold")

    ax.set_title("PoMMES Control Flow Graph", fontsize=14)
    outdir = os.path.dirname(out_png)
    if outdir and not os.path.isdir(outdir):
        os.makedirs(outdir, exist_ok=True)
    plt.savefig(out_png, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"wrote plot -> {out_png}")


if __name__ == "__main__":
    cfg = sys.argv[1] if len(sys.argv) > 1 else "/tmp/pommes_cfg.txt"
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/pommes_cfg.png"
    sens_out = sys.argv[3] if len(sys.argv) > 3 else "/tmp/pommes_bb_sens.txt"
    sens_out_png = sys.argv[4] if len(sys.argv) > 4 else "/tmp/pommes_bb_sens.png"
    main(cfg, out)
    generate_sensitivity_plot(sens_out, sens_out_png)
