/* Two-species comparison. Pages come from data/pages.json.
   Blocks line up by title. A label lines up only when both accounts use it. */

const COMPARE_BLOCKS = ["Habit", "Leaves", "Flowers", "Fruit"];

let comparePages = [];
const picked = { a: null, b: null };

function compareEsc(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;"
    }[ch]));
}

function comparePair(en, zh) {
    return `<span class="lang-en">${compareEsc(en)}</span><span class="lang-zh hidden">${compareEsc(zh)}</span>`;
}

function compareNorm(value) {
    return String(value ?? "").toLowerCase().replace(/\s+/g, " ").trim();
}

function compareHay(page) {
    return compareNorm([
        page.sci,
        page.chi_line,
        page.genus,
        page.family,
        page.blp,
        ...(page.chi_names || []),
        ...(page.en_names || [])
    ].join(" "));
}

function compareLabel(page) {
    return `${page.sci} · ${page.chi_line || page.blp}`;
}

function compareBySci(a, b) {
    return a.sci.localeCompare(b.sci, "en");
}

function compareFind(blp) {
    return comparePages.find((page) => page.blp === String(blp)) || null;
}

function compareOther(slot) {
    return picked[slot === "a" ? "b" : "a"];
}

function compareMatches(page, query) {
    if (!query) return true;
    return compareHay(page).includes(query);
}

function compareWriteUrl() {
    const url = new URL(location.href);
    if (picked.a) url.searchParams.set("a", picked.a.blp);
    else url.searchParams.delete("a");
    if (picked.b) url.searchParams.set("b", picked.b.blp);
    else url.searchParams.delete("b");
    history.replaceState(null, "", url.pathname + url.search + url.hash);
}

function compareSyncButton() {
    const button = document.getElementById("compareGo");
    const note = document.getElementById("compareNote");
    const same = picked.a && picked.b && picked.a.blp === picked.b.blp;
    button.disabled = !picked.a || !picked.b || same;
    note.hidden = !same;
}

function compareSetPicked(slot, page) {
    picked[slot] = page;
    const input = document.getElementById(slot === "a" ? "pickA" : "pickB");
    const clear = input.parentElement.querySelector(".compare-clear");
    input.value = page ? compareLabel(page) : "";
    input.dataset.blp = page ? page.blp : "";
    clear.hidden = !page;
    compareSyncButton();
}

function compareRenderList(slot) {
    const input = document.getElementById(slot === "a" ? "pickA" : "pickB");
    const list = document.getElementById(slot === "a" ? "listA" : "listB");
    const query = input.dataset.blp ? "" : compareNorm(input.value);
    const other = compareOther(slot);
    const rows = comparePages
        .filter((page) => compareMatches(page, query))
        .sort((a, b) => {
            if (other && a.genus === other.genus && b.genus !== other.genus) return -1;
            if (other && b.genus === other.genus && a.genus !== other.genus) return 1;
            return compareBySci(a, b);
        });
    if (!rows.length) {
        list.innerHTML = `<li class="compare-empty">${comparePair("No published page matches.", "沒有已寫的頁。")}</li>`;
        list.hidden = false;
        return;
    }
    list.innerHTML = rows.map((page) => {
        const taken = other && other.blp === page.blp;
        const genus = other && page.genus === other.genus ? " compare-same-genus" : "";
        return `<li><button type="button" class="compare-option${genus}" data-blp="${compareEsc(page.blp)}" ${taken ? "disabled" : ""}>
            <span class="compare-sci">${compareEsc(page.sci)}</span>
            <span class="compare-meta">${compareEsc(page.chi_line || "")}${page.family ? " · " + compareEsc(page.family) : ""}</span>
        </button></li>`;
    }).join("");
    list.hidden = false;
}

function compareHideList(slot) {
    document.getElementById(slot === "a" ? "listA" : "listB").hidden = true;
}

function compareBlockRows(left, right) {
    const titles = [];
    const seen = new Set();
    function add(title) {
        if (!title || seen.has(title)) return;
        seen.add(title);
        titles.push(title);
    }
    const blocks = [...(left.morphology || []), ...(right.morphology || [])];
    COMPARE_BLOCKS.forEach((title) => {
        if (blocks.some((block) => block.title_en === title)) add(title);
    });
    blocks.forEach((block) => add(block.title_en));
    return titles.map((title) => {
        const a = (left.morphology || []).find((block) => block.title_en === title);
        const b = (right.morphology || []).find((block) => block.title_en === title);
        return {
            title_en: title,
            title_zh: (a || b).title_zh || title,
            rows: compareItemRows(a, b)
        };
    });
}

function compareItemRows(blockA, blockB) {
    const itemsA = (blockA && blockA.items) || [];
    const itemsB = (blockB && blockB.items) || [];
    const used = new Set();
    const rows = [];
    itemsA.forEach((item) => {
        const index = itemsB.findIndex((other, i) => !used.has(i) && other.label_en === item.label_en);
        if (index >= 0) {
            used.add(index);
            rows.push({ label_en: item.label_en, label_zh: item.label_zh, a: item, b: itemsB[index] });
        } else {
            rows.push({ label_en: item.label_en, label_zh: item.label_zh, a: item, b: null });
        }
    });
    itemsB.forEach((item, index) => {
        if (used.has(index)) return;
        rows.push({ label_en: item.label_en, label_zh: item.label_zh, a: null, b: item });
    });
    return rows;
}

function compareEcologyRows(left, right) {
    const order = ["Habitat", "Status", "Distribution"];
    const itemsA = left.ecology || [];
    const itemsB = right.ecology || [];
    const labels = [];
    const seen = new Set();
    function add(label) {
        if (!label || seen.has(label)) return;
        seen.add(label);
        labels.push(label);
    }
    order.forEach((label) => {
        if (itemsA.some((item) => item.label_en === label) || itemsB.some((item) => item.label_en === label)) add(label);
    });
    itemsA.forEach((item) => add(item.label_en));
    itemsB.forEach((item) => add(item.label_en));
    return labels.map((label) => {
        const a = itemsA.find((item) => item.label_en === label);
        const b = itemsB.find((item) => item.label_en === label);
        return { label_en: label, label_zh: (a || b).label_zh || label, a, b };
    });
}

function compareCell(item) {
    if (!item) return `<td class="compare-empty-cell">—</td>`;
    return `<td>${comparePair(item.en, item.zh)}</td>`;
}

function compareHead(page) {
    const href = `../species/${compareEsc(page.blp)}.html`;
    return `<a class="compare-name" href="${href}">
        <span class="compare-sci">${compareEsc(page.sci)}</span>
        <span class="compare-zh">${compareEsc(page.chi_line || "")}</span>
    </a>`;
}

function compareRender() {
    const mount = document.getElementById("compareResult");
    const left = picked.a;
    const right = picked.b;
    if (!left || !right || left.blp === right.blp) {
        mount.hidden = true;
        mount.innerHTML = "";
        return;
    }
    const sections = compareBlockRows(left, right);
    sections.push({
        title_en: "Ecology",
        title_zh: "生態",
        rows: compareEcologyRows(left, right)
    });
    const body = sections.map((section) => {
        const rows = section.rows.map((row) => `<tr>
            <th scope="row">${comparePair(row.label_en, row.label_zh)}</th>
            ${compareCell(row.a)}
            ${compareCell(row.b)}
        </tr>`).join("");
        return `<tbody>
            <tr class="compare-block"><th colspan="3">${comparePair(section.title_en, section.title_zh)}</th></tr>
            ${rows || `<tr><td colspan="3" class="compare-empty-cell">—</td></tr>`}
        </tbody>`;
    }).join("");
    mount.innerHTML = `<table class="compare-table">
        <colgroup><col class="compare-label-col"><col><col></colgroup>
        <thead>
            <tr>
                <th></th>
                <th>${compareHead(left)}</th>
                <th>${compareHead(right)}</th>
            </tr>
        </thead>
        ${body}
    </table>`;
    mount.hidden = false;
    if (typeof applyLanguage === "function") applyLanguage();
    compareWriteUrl();
}

function compareBindPicker(slot) {
    const input = document.getElementById(slot === "a" ? "pickA" : "pickB");
    const list = document.getElementById(slot === "a" ? "listA" : "listB");
    const clear = input.parentElement.querySelector(".compare-clear");
    input.addEventListener("focus", () => {
        input.select();
        compareRenderList(slot);
    });
    input.addEventListener("input", () => {
        input.dataset.blp = "";
        picked[slot] = null;
        clear.hidden = !input.value;
        compareSyncButton();
        document.getElementById("compareResult").hidden = true;
        compareRenderList(slot);
    });
    clear.addEventListener("click", () => {
        compareSetPicked(slot, null);
        document.getElementById("compareResult").hidden = true;
        input.focus();
        compareRenderList(slot);
    });
    list.addEventListener("mousedown", (event) => {
        const button = event.target.closest("[data-blp]");
        if (!button || button.disabled) return;
        event.preventDefault();
        compareSetPicked(slot, compareFind(button.dataset.blp));
        compareHideList(slot);
    });
    input.addEventListener("keydown", (event) => {
        const options = [...list.querySelectorAll(".compare-option:not(:disabled)")];
        const current = list.querySelector(".compare-option.on");
        let index = options.indexOf(current);
        if (event.key === "ArrowDown" || event.key === "ArrowUp") {
            event.preventDefault();
            if (list.hidden) compareRenderList(slot);
            const next = event.key === "ArrowDown" ? index + 1 : index - 1;
            const option = options[(next + options.length) % options.length];
            options.forEach((el) => el.classList.remove("on"));
            if (option) {
                option.classList.add("on");
                option.scrollIntoView({ block: "nearest" });
            }
        } else if (event.key === "Enter") {
            event.preventDefault();
            if (current && !current.disabled) {
                compareSetPicked(slot, compareFind(current.dataset.blp));
                compareHideList(slot);
            } else if (picked.a && picked.b) {
                compareRender();
            }
        } else if (event.key === "Escape") {
            compareHideList(slot);
        }
    });
    input.addEventListener("blur", () => {
        setTimeout(() => compareHideList(slot), 120);
    });
}

document.addEventListener("DOMContentLoaded", () => {
    compareBindPicker("a");
    compareBindPicker("b");
    document.getElementById("compareGo").addEventListener("click", compareRender);
    fetch("../data/pages.json")
        .then((res) => {
            if (!res.ok) throw new Error(String(res.status));
            return res.json();
        })
        .then((data) => {
            comparePages = Object.values(data.pages || {}).sort(compareBySci);
            const params = new URLSearchParams(location.search);
            const a = compareFind(params.get("a"));
            const b = compareFind(params.get("b"));
            if (a) compareSetPicked("a", a);
            if (b) compareSetPicked("b", b);
            if (a && b) compareRender();
        })
        .catch(() => {
            document.getElementById("compareLoad").hidden = false;
        });
});
