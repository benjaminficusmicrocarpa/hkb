/* Shared loader for hkb/data/taxa.json. Taxon names only — no photo counts. */

const HKB_RANK = {
    SPECIES: ["Species", "種"],
    VARIETY: ["Variety", "變種"],
    SUBSPECIES: ["Subspecies", "亞種"],
    FORM: ["Form", "變型"],
    Cultivar: ["Cultivar", "栽培品種"],
    XSPECIES: ["Not to species", "未定種"],
    Section: ["Section", "系"]
};

function hkbEsc(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;"
    }[ch]));
}

function hkbRankLabel(rank) {
    const pair = HKB_RANK[rank] || [rank || "—", rank || "—"];
    return `<span class="lang-en">${hkbEsc(pair[0])}</span><span class="lang-zh hidden">${hkbEsc(pair[1])}</span>`;
}

function hkbSciHtml(sci) {
    const text = String(sci ?? "");
    const quoted = text.match(/^(.*?)(\s+'.*')$/);
    if (quoted) {
        return `<span class="italic">${hkbEsc(quoted[1])}</span> ${hkbEsc(quoted[2].trim())}`;
    }
    return `<span class="italic">${hkbEsc(text)}</span>`;
}

function hkbLoadTaxa() {
    const base = document.querySelector('meta[name="hkb-base"]')?.content || "..";
    return fetch(base + "/data/taxa.json").then((res) => {
        if (!res.ok) throw new Error("taxa.json " + res.status);
        return res.json();
    });
}

function hkbFormatCount(n) {
    return Number(n).toLocaleString("en-GB");
}
