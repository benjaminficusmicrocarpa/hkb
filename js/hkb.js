/* ============================================
   Hong Kong Botanica — Shared JavaScript
   ============================================ */

let currentLang = localStorage.getItem('hkb-lang') || 'en';

const placeholders = {
    en: "Search by scientific name, family, or common name\u2026",
    zh: "透過學名、科名或俗名搜尋\u2026"
};

function applyLanguage() {
    document.documentElement.lang = currentLang;
    document.querySelectorAll('.lang-en').forEach(el => {
        el.classList.toggle('hidden', currentLang !== 'en');
    });
    document.querySelectorAll('.lang-zh').forEach(el => {
        el.classList.toggle('hidden', currentLang !== 'zh');
    });
    document.querySelectorAll('[data-placeholder-en]').forEach(el => {
        el.placeholder = currentLang === 'en'
            ? el.dataset.placeholderEn
            : el.dataset.placeholderZh;
    });
}

function hkbWriteLanguageParam() {
    const url = new URL(location.href);
    url.searchParams.set("language", currentLang === "zh" ? "zh" : "en");
    const next = url.pathname + url.search + url.hash;
    if (next !== location.pathname + location.search + location.hash) {
        history.replaceState(null, "", next);
    }
}

function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'zh' : 'en';
    localStorage.setItem('hkb-lang', currentLang);
    applyLanguage();
    hkbWriteLanguageParam();
    document.querySelectorAll("a[href]").forEach((a) => {
        const href = a.getAttribute("href");
        if (!href || href.startsWith("#")) return;
        const path = href.split("?")[0];
        if (!/(?:^|\/)(?:detail\.html|\d{5}\.html)$/.test(path)) return;
        const url = new URL(href, location.href);
        url.searchParams.set("language", currentLang);
        a.setAttribute("href", path + "?" + url.searchParams.toString());
    });
}

// Mobile nav
function openMobileNav() {
    document.getElementById('mobileOverlay')?.classList.add('open');
    document.getElementById('mobileDrawer')?.classList.add('open');
    document.body.style.overflow = 'hidden';
}
function closeMobileNav() {
    document.getElementById('mobileOverlay')?.classList.remove('open');
    document.getElementById('mobileDrawer')?.classList.remove('open');
    document.body.style.overflow = '';
}

// Search redirect
function handleSearch(e) {
    e.preventDefault();
    const q = e.target.querySelector('input[type="text"], input[type="search"]')?.value?.trim();
    if (q) {
        const base = document.querySelector('meta[name="hkb-base"]')?.content || '.';
        window.location.href = base + '/search/index.html?q=' + encodeURIComponent(q);
    }
}

// Phenology bar helper: parse "3-5" or "11-3" (wrapping) or "5" into array of month numbers
function parseMonths(str) {
    if (!str) return [];
    str = String(str).trim();
    if (str.includes('-')) {
        const [a, b] = str.split('-').map(Number);
        if (a <= b) {
            return Array.from({length: b - a + 1}, (_, i) => a + i);
        }
        // wraps around year end
        const months = [];
        for (let m = a; m <= 12; m++) months.push(m);
        for (let m = 1; m <= b; m++) months.push(m);
        return months;
    }
    if (str.includes(',')) return str.split(',').map(Number);
    return [Number(str)];
}

function hkbPhotoUrl(imageId, variant) {
    const id = String(imageId || "");
    if (!id) return "";
    const kind = variant || "public";
    return "https://imagedelivery.net/w8B9Irt4MxIF11C23YczhQ/" + encodeURIComponent(id) + "/" + kind;
}

function renderPhenologyBar(flowerMonths, fruitMonths, container) {
    const labels = ['J','F','M','A','M','J','J','A','S','O','N','D'];
    const fm = parseMonths(flowerMonths);
    const fr = parseMonths(fruitMonths);
    let html = '<div class="phenology-bar" style="height:28px">';
    for (let m = 1; m <= 12; m++) {
        const isFlower = fm.includes(m);
        const isFruit = fr.includes(m);
        let cls = 'inactive';
        if (isFlower) cls = 'active';
        else if (isFruit) cls = 'fruit';
        html += `<div class="month ${cls}" style="height:${isFlower ? '100%' : isFruit ? '60%' : '30%'}" title="${labels[m-1]}"></div>`;
    }
    html += '</div><div class="phenology-bar" style="height:auto">';
    for (let m = 0; m < 12; m++) {
        html += `<div class="month-label">${labels[m]}</div>`;
    }
    html += '</div>';
    if (container) container.innerHTML = html;
    return html;
}

document.addEventListener('DOMContentLoaded', () => {
    hkbWriteLanguageParam();
    applyLanguage();

    document.querySelectorAll('.search-form').forEach(form => {
        form.addEventListener('submit', handleSearch);
    });

    // Animate elements on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    document.querySelectorAll('.observe-animate').forEach(el => observer.observe(el));
});
