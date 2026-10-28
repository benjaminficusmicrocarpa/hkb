/* Taxonomic tree: collapsible outline and column browser. */

const TX_RANK = {
    kingdom: ["Kingdom", "界"],
    phylum: ["Phylum", "門"],
    major_group: ["Group", "大類"],
    class: ["Class", "綱"],
    subclass: ["Subclass", "亞綱"],
    clade: ["Clade", "演化支"],
    order: ["Order", "目"],
    suborder: ["Suborder", "亞目"],
    family: ["Family", "科"],
    genus: ["Genus", "屬"],
    species: ["Species", "種"],
    variety: ["Variety", "變種"],
    subspecies: ["Subspecies", "亞種"],
    form: ["Form", "變型"],
    cultivar: ["Cultivar", "栽培品種"],
    xspecies: ["Not to species", "未定種"],
    section: ["Section", "系"]
};

const TX_GROUP = {
    lycophyte: ["Lycophytes", "石松類"],
    fern: ["Ferns", "蕨類"],
    gymnosperm: ["Gymnosperms", "裸子植物"],
    angiosperm: ["Angiosperms", "被子植物"]
};

const TX_ITALIC = new Set(["genus", "species", "variety", "subspecies", "form", "cultivar", "xspecies"]);
const TX_ABOVE_FAMILY = new Set(["kingdom", "phylum", "major_group", "class", "subclass", "clade", "order", "suborder"]);

let TX = null;
let TX_ROOT = null;
let TX_BY_ID = new Map();
let TX_ROWS = [];
let txView = "tree";
let txSelected = null;
let txExpanded = new Set();
let txQuery = "";

function txIsLeaf(node) {
    return Boolean(node && node.b);
}

function txId(node) {
    return node._id;
}

function txRankHtml(rank) {
    const pair = TX_RANK[rank] || [rank || "—", rank || "—"];
    return `<span class="lang-en">${hkbEsc(pair[0])}</span><span class="lang-zh hidden">${hkbEsc(pair[1])}</span>`;
}

function txLabelHtml(node) {
    const latin = TX_ITALIC.has(node.r) ? hkbSciHtml(node.n) : hkbEsc(node.n);
    if (!node.z) return latin;
    return latin + `<span class="tx-zh"> ${hkbEsc(node.z)}</span>`;
}

function txLabelText(node) {
    const parts = [node.n, node.z];
    if (node.r === "major_group" && TX_GROUP[node.n]) parts.push.apply(parts, TX_GROUP[node.n]);
    return parts.filter(Boolean).join(" ");
}

function txIndex(node, parent) {
    const id = (parent ? parent._id + "/" : "") + node.r + ":" + node.n + (node.b ? ":" + node.b : "");
    node._id = id;
    node._parent = parent || null;
    TX_BY_ID.set(id, node);
    const parts = [node.n, node.z, node.a, node.b, txLabelText(node)];
    if (node.b) parts.push("blp-" + node.b, "blp " + node.b);
    TX_ROWS.push({ id, node, blob: parts.filter(Boolean).join(" ").toLowerCase() });
    (node.k || []).forEach((child) => txIndex(child, node));
}

function txAncestor(node, rank) {
    let cursor = node;
    while (cursor) {
        if (cursor.r === rank) return cursor.n;
        cursor = cursor._parent;
    }
    return "";
}

function txMajorGroup(node) {
    let cursor = node;
    while (cursor) {
        if (cursor.r === "major_group") return cursor.n;
        cursor = cursor._parent;
    }
    return "";
}

function txPath(node) {
    const path = [];
    let cursor = node;
    while (cursor) {
        path.push(cursor);
        cursor = cursor._parent;
    }
    return path.reverse();
}

function txSkippable(node) {
    return Boolean(node && node.k && node.k.length === 1 && node.k[0].k && !txIsLeaf(node.k[0]));
}

function txDrill(node) {
    let cursor = node;
    let guard = 0;
    while (txSkippable(cursor) && guard < 12) {
        cursor = cursor.k[0];
        guard += 1;
    }
    return cursor;
}

function txAutoExpand(node) {
    txExpanded.add(node._id);
    if (node.k && node.k.length === 1 && !txIsLeaf(node.k[0])) txAutoExpand(node.k[0]);
}

function txOpen(id) {
    const node = TX_BY_ID.get(id);
    if (!node) return;
    txExpanded.add(id);
    let cursor = node;
    while (cursor.k && cursor.k.length === 1 && !txIsLeaf(cursor.k[0])) {
        cursor = cursor.k[0];
        txExpanded.add(cursor._id);
    }
}

function txExpandTo(node) {
    let cursor = node;
    while (cursor) {
        if (cursor._parent) txExpanded.add(cursor._parent._id);
        cursor = cursor._parent;
    }
}

function txExpandToFamilies(node) {
    if (!node || txIsLeaf(node) || !node.k) return;
    if (node === TX_ROOT || TX_ABOVE_FAMILY.has(node.r)) {
        txExpanded.add(node._id);
        node.k.forEach(txExpandToFamilies);
    }
}

function txVisibleIds() {
    const q = txQuery.trim().toLowerCase();
    if (!q) return null;
    const show = new Set();
    TX_ROWS.forEach((row) => {
        if (!row.blob.includes(q)) return;
        let cursor = row.node;
        while (cursor) {
            show.add(cursor._id);
            cursor = cursor._parent;
        }
    });
    return show;
}

function txWriteUrl() {
    const params = new URLSearchParams(location.search);
    params.set("view", txView);
    if (txSelected) params.set("node", txSelected);
    else params.delete("node");
    const next = location.pathname + "?" + params.toString();
    if (next !== location.pathname + location.search) {
        history.replaceState(null, "", next);
    }
}

function txSelect(id, opts) {
    const node = TX_BY_ID.get(id);
    if (!node) return;
    txSelected = id;
    txExpandTo(node);
    txOpen(id);
    txWriteUrl();
    txRender();
    if (!opts || opts.scroll !== false) {
        const el = document.querySelector(`[data-tx-id="${CSS.escape(id)}"]`);
        if (el) el.scrollIntoView({ block: "nearest", inline: "nearest" });
    }
}

function txDirHref(node) {
    const family = node.r === "family" ? node.n : txAncestor(node, "family");
    const genus = node.r === "genus" ? node.n : txAncestor(node, "genus");
    if (genus && family) {
        return "../species/index.html?" + new URLSearchParams({ genus, family }).toString();
    }
    if (family) return "../species/index.html?" + new URLSearchParams({ family }).toString();
    if (node.r === "order") return "../families/index.html#order-" + encodeURIComponent(node.n);
    return "";
}

const TX_RANK_ORDER = Object.keys(TX_RANK);

function txLowerCounts(node) {
    const counts = new Map();
    function walk(current) {
        (current.k || []).forEach((child) => {
            counts.set(child.r, (counts.get(child.r) || 0) + 1);
            if (child.k) walk(child);
        });
    }
    walk(node);
    const here = TX_RANK_ORDER.indexOf(node.r);
    return TX_RANK_ORDER.filter((rank, index) => index > here && counts.get(rank)).map((rank) => ({
        rank,
        n: counts.get(rank)
    }));
}

function txLowerHtml(node) {
    const rows = txLowerCounts(node);
    if (!rows.length) return "";
    const max = Math.max.apply(null, rows.map((row) => row.n));
    const tiles = rows.map((row) => {
        const pair = TX_RANK[row.rank] || [row.rank, row.rank];
        const width = Math.max(8, Math.round(Math.log(row.n + 1) / Math.log(max + 1) * 100));
        return `<div class="tx-stat${row.rank === "species" ? " species" : ""}">
            <div class="tx-stat-n">${hkbFormatCount(row.n)}</div>
            <span class="tx-stat-zh">${hkbEsc(pair[1])}</span>
            <span class="tx-stat-en">${hkbEsc(pair[0])}</span>
            <div class="tx-stat-track" aria-hidden="true"><span style="width:${width}%"></span></div>
        </div>`;
    }).join("");
    return `<div class="tx-below">
        <p class="tx-below-kicker"><span class="lang-en">Ranks below</span><span class="lang-zh hidden">以下階層</span></p>
        <div class="tx-below-grid">${tiles}</div>
    </div>`;
}

function txDetail(node) {
    if (!node) {
        return `<p class="tx-muted"><span class="lang-en">Select a branch.</span><span class="lang-zh hidden">選一個分支。</span></p>`;
    }
    const crumbs = txPath(node).map((step) => {
        const current = step._id === node._id ? " aria-current=\"page\"" : "";
        return `<button type="button" class="tx-crumb" data-tx-select="${hkbEsc(step._id)}"${current}>${txLabelHtml(step)}</button>`;
    }).join("<span class=\"tx-crumb-sep\">/</span>");
    const group = txMajorGroup(node);
    const system = group && TX.systems[group]
        ? `<p class="tx-system"><span class="lang-en">${hkbEsc(TX.systems[group][0])}</span><span class="lang-zh hidden">${hkbEsc(TX.systems[group][1])}</span></p>`
        : "";
    if (txIsLeaf(node)) {
        const page = node.p
            ? `<a class="tx-go" href="../species/${hkbEsc(node.b)}.html"><span class="lang-en">Open page</span><span class="lang-zh hidden">打開頁面</span></a>`
            : `<span class="tx-pill"><span class="lang-en">No page</span><span class="lang-zh hidden">未有頁面</span></span>`;
        const dir = txDirHref(node);
        const dirLink = dir
            ? `<a class="tx-go tx-go-quiet" href="${hkbEsc(dir)}"><span class="lang-en">In the directory</span><span class="lang-zh hidden">在目錄中</span></a>`
            : "";
        const alt = node.a ? `<p class="tx-alt">${hkbEsc(node.a)}</p>` : "";
        return `<div class="tx-crumbs">${crumbs}</div>
            <p class="tx-rankline">${txRankHtml(node.r)}</p>
            <h2 class="tx-detail-name">${txLabelHtml(node)}</h2>
            ${alt}
            <p class="tx-blp">BLP ${hkbEsc(node.b)}</p>
            ${system}
            <div class="tx-actions">${page}${dirLink}</div>`;
    }
    const dir = txDirHref(node);
    const dirLink = dir
        ? `<a class="tx-go" href="${hkbEsc(dir)}"><span class="lang-en">Open this rank in the directory</span><span class="lang-zh hidden">在目錄中打開這一階</span></a>`
        : "";
    const countLabel = node.r === "kingdom" || node.r === "phylum"
        ? ""
        : `<p class="tx-countline">${hkbFormatCount(node.c)} <span class="lang-en">taxa</span><span class="lang-zh hidden">分類群</span></p>`;
    return `<div class="tx-crumbs">${crumbs}</div>
        <p class="tx-rankline">${txRankHtml(node.r)}</p>
        <h2 class="tx-detail-name">${txLabelHtml(node)}</h2>
        ${countLabel}
        ${txLowerHtml(node)}
        ${system}
        ${dirLink}`;
}

function txRowHtml(node, depth, show) {
    const kids = node.k || [];
    const visibleKids = show ? kids.filter((child) => show.has(child._id)) : kids;
    const hasKids = visibleKids.length > 0;
    const open = hasKids && (show ? true : txExpanded.has(node._id));
    const selected = node._id === txSelected ? " selected" : "";
    const toggle = hasKids
        ? `<button type="button" class="tx-toggle${open ? " open" : ""}" data-tx-toggle="${hkbEsc(node._id)}" aria-expanded="${open ? "true" : "false"}" aria-label="${open ? "Collapse" : "Expand"}"></button>`
        : `<span class="tx-toggle spacer"></span>`;
    const meta = txIsLeaf(node)
        ? (node.p ? `<span class="tx-dot" title="Page"></span>` : "")
        : `<span class="tx-meta">${hkbFormatCount(node.c)}</span>`;
    const childHtml = open
        ? `<div class="tx-children">${visibleKids.map((child) => txRowHtml(child, depth + 1, show)).join("")}</div>`
        : "";
    return `<div class="tx-node" role="treeitem" aria-expanded="${hasKids ? (open ? "true" : "false") : "false"}">
        <div class="tx-row${selected}" data-tx-id="${hkbEsc(node._id)}" style="padding-left:${depth * 14}px">
            ${toggle}
            <button type="button" class="tx-name" data-tx-select="${hkbEsc(node._id)}">${txLabelHtml(node)}</button>
            <span class="tx-rank">${txRankHtml(node.r)}</span>
            ${meta}
        </div>
        ${childHtml}
    </div>`;
}

function txTreeHtml(show) {
    let start = TX_ROOT;
    while (start.k && start.k.length === 1 && !txIsLeaf(start.k[0])) start = start.k[0];
    const kids = start.k || [];
    const visible = show ? kids.filter((child) => show.has(child._id)) : kids;
    if (txQuery && !visible.length) {
        return `<p class="tx-muted"><span class="lang-en">No matches.</span><span class="lang-zh hidden">沒有符合的。</span></p>`;
    }
    return visible.map((child) => txRowHtml(child, 0, show)).join("");
}

function txColumns(selected) {
    const start = txDrill(TX_ROOT);
    const cols = [];
    let parent = start;
    let guard = 0;
    while (parent && guard < 24) {
        const shown = txDrill(parent);
        const items = shown.k || [];
        if (!items.length) break;
        const hit = selected
            ? items.find((item) => item === selected || txPath(selected).includes(item))
            : null;
        cols.push({ items, selectedId: hit ? hit._id : null });
        if (!hit) break;
        if (hit === selected) {
            if (hit.k && hit.k.length) cols.push({ items: txDrill(hit).k || hit.k, selectedId: null });
            break;
        }
        parent = hit;
        guard += 1;
    }
    if (!cols.length && start.k) cols.push({ items: start.k, selectedId: null });
    return cols;
}

function txBrowserHtml() {
    const selected = txSelected ? TX_BY_ID.get(txSelected) : null;
    const q = txQuery.trim().toLowerCase();
    if (q) {
        const hits = TX_ROWS.filter((row) => row.blob.includes(q)).slice(0, 40);
        if (!hits.length) {
            return `<p class="tx-muted"><span class="lang-en">No matches.</span><span class="lang-zh hidden">沒有符合的。</span></p>`;
        }
        return `<div class="tx-results" role="listbox">${hits.map((row) => {
            const parent = row.node._parent;
            const where = parent ? txLabelHtml(parent) : "";
            return `<button type="button" class="tx-result" data-tx-select="${hkbEsc(row.id)}">
                <span class="tx-result-name">${txLabelHtml(row.node)}</span>
                <span class="tx-result-meta">${txRankHtml(row.node.r)}${where ? " · " + where : ""}</span>
            </button>`;
        }).join("")}</div>`;
    }
    const cols = txColumns(selected);
    return `<div class="tx-cols">${cols.map((col) => {
        const rows = col.items.map((item) => {
            const on = item._id === col.selectedId ? " selected" : "";
            const more = item.k && item.k.length ? `<span class="tx-more" aria-hidden="true"></span>` : "";
            const sub = txIsLeaf(item) ? "" : hkbFormatCount(item.c);
            return `<button type="button" class="tx-col-row${on}" data-tx-id="${hkbEsc(item._id)}" data-tx-select="${hkbEsc(item._id)}">
                <span class="tx-col-name">${txLabelHtml(item)}${item.p ? `<span class="tx-dot"></span>` : ""}</span>
                <span class="tx-col-sub">${txRankHtml(item.r)}${sub ? " · " + sub : ""}</span>
                ${more}
            </button>`;
        }).join("");
        return `<div class="tx-col" role="listbox">${rows}</div>`;
    }).join("")}</div>`;
}

function txRender() {
    const show = txVisibleIds();
    const stage = document.getElementById("txStage");
    stage.innerHTML = txView === "browser" ? txBrowserHtml() : `<div class="tx-tree" role="tree">${txTreeHtml(show)}</div>`;
    document.getElementById("txDetail").innerHTML = txDetail(txSelected ? TX_BY_ID.get(txSelected) : null);
    document.getElementById("btnTree").classList.toggle("active", txView === "tree");
    document.getElementById("btnBrowser").classList.toggle("active", txView === "browser");
    document.getElementById("treeTools").style.display = txView === "tree" ? "" : "none";
    const q = txQuery.trim().toLowerCase();
    const n = q ? TX_ROWS.filter((row) => row.blob.includes(q)).length : 0;
    const count = document.getElementById("txHitCount");
    count.style.display = q ? "" : "none";
    count.innerHTML = q
        ? `${hkbFormatCount(n)} <span class="lang-en">matches</span><span class="lang-zh hidden">項符合</span>`
        : "";
    if (typeof applyLanguage === "function") applyLanguage();
}

function txBind() {
    document.getElementById("txStage").addEventListener("click", (event) => {
        const toggle = event.target.closest("[data-tx-toggle]");
        if (toggle) {
            const id = toggle.getAttribute("data-tx-toggle");
            if (txExpanded.has(id)) txExpanded.delete(id);
            else txOpen(id);
            txRender();
            return;
        }
        const select = event.target.closest("[data-tx-select]");
        if (select) txSelect(select.getAttribute("data-tx-select"));
    });
    document.getElementById("txDetail").addEventListener("click", (event) => {
        const select = event.target.closest("[data-tx-select]");
        if (select) txSelect(select.getAttribute("data-tx-select"));
    });
    document.getElementById("btnTree").addEventListener("click", () => {
        txView = "tree";
        if (txSelected) txExpandTo(TX_BY_ID.get(txSelected));
        txWriteUrl();
        txRender();
    });
    document.getElementById("btnBrowser").addEventListener("click", () => {
        txView = "browser";
        txWriteUrl();
        txRender();
    });
    document.getElementById("txSearch").addEventListener("input", (event) => {
        txQuery = event.target.value;
        txRender();
    });
    document.getElementById("txExpand").addEventListener("click", () => {
        txExpandToFamilies(TX_ROOT);
        txRender();
    });
    document.getElementById("txCollapse").addEventListener("click", () => {
        txExpanded = new Set();
        txAutoExpand(TX_ROOT);
        txRender();
    });
}

function txFillStats() {
    const item = (n, en, zh) => `<div><span class="text-2xl font-serif font-bold text-stone-800">${hkbFormatCount(n)}</span> <span class="text-sm text-stone-500"><span class="lang-en">${en}</span><span class="lang-zh hidden">${zh}</span></span></div>`;
    document.getElementById("txStats").innerHTML = [
        item(TX.n_orders, "Orders", "目"),
        item(TX.n_families, "Families", "科"),
        item(TX.n_genera, "Genera", "屬"),
        item(TX.n_taxa, "Taxa", "分類群")
    ].join('<span class="hidden sm:block text-stone-300 text-xl">·</span>');
    const counts = TX.counts || {};
    const group = (key, en, zh) => `<span>${hkbFormatCount(counts[key] || 0)} <span class="lang-en">${en}</span><span class="lang-zh hidden">${zh}</span></span>`;
    document.getElementById("txGroups").innerHTML = [
        group("lycophyte", "lycophytes", "石松類"),
        group("fern", "ferns", "蕨類植物"),
        group("gymnosperm", "gymnosperms", "裸子植物"),
        group("angiosperm", "angiosperms", "被子植物")
    ].join('<span class="tx-dot-sep">·</span>');
}

function txBoot() {
    const base = document.querySelector('meta[name="hkb-base"]')?.content || "..";
    fetch(base + "/data/taxonomy-tree.json").then((res) => {
        if (!res.ok) throw new Error("taxonomy-tree.json " + res.status);
        return res.json();
    }).then((data) => {
        TX = data;
        TX_ROOT = data.root;
        txIndex(TX_ROOT, null);
        const leaves = TX_ROWS.filter((row) => row.node.b).length;
        if (TX_ROOT.c !== data.n_taxa || leaves !== data.n_taxa) {
            throw new Error("tree count mismatch");
        }
        txAutoExpand(TX_ROOT);
        const params = new URLSearchParams(location.search);
        txView = params.get("view") === "browser" ? "browser" : "tree";
        const requested = params.get("node");
        if (requested && TX_BY_ID.has(requested)) {
            txSelected = requested;
            txExpandTo(TX_BY_ID.get(requested));
        }
        txFillStats();
        txBind();
        txRender();
    }).catch((err) => {
        document.getElementById("txStats").textContent = "Could not load the taxonomic tree. " + err.message;
    });
}

txBoot();
