/* Photo viewer for a generated species page.
   Text is already in the HTML. data/build_pages.py writes that HTML.
   Address: 49562.html?language=en
   Photos are in #page-photos. Do not fetch pages.json here. */

function hkbPageEsc(value) {
    return String(value ?? "").replace(/[&<>"']/g, (ch) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        "\"": "&quot;",
        "'": "&#39;"
    }[ch]));
}

function hkbPair(en, zh) {
    return `<span class="lang-en">${hkbPageEsc(en)}</span><span class="lang-zh hidden">${hkbPageEsc(zh)}</span>`;
}

(function hkbSyncLanguageFromUrl() {
    const lang = new URLSearchParams(location.search).get("language");
    if (lang === "en" || lang === "zh") {
        currentLang = lang;
        localStorage.setItem("hkb-lang", lang);
    }
})();


function hkbPhotoViewer(photos) {
    const mount = document.getElementById("photoMount");
    if (!photos || !photos.length) {
        mount.innerHTML = `<p class="text-sm text-stone-400">${hkbPair("No representative photographs yet.", "尚未有代表照片。")}</p>`;
        return;
    }
    const state = { i: 0, scale: 1, open: false, controls: true, panX: 0, panY: 0 };
    mount.innerHTML = `<div id="photoStage" class="photo-stage">
        <button type="button" class="photo-toggle" id="photoToggle" aria-pressed="true">
            <i class="fa-solid fa-sliders"></i>
            <span class="lang-en">Controls</span><span class="lang-zh hidden">控制</span>
        </button>
        <button type="button" class="photo-arrow prev" data-act="left" aria-label="Left"><i class="fa-solid fa-chevron-left"></i></button>
        <button type="button" class="photo-arrow next" data-act="right" aria-label="Right"><i class="fa-solid fa-chevron-right"></i></button>
        <img id="photoImg" alt="" draggable="false">
        <p id="photoCaption" class="photo-caption"></p>
        <div id="photoDock" class="photo-dock">
            <button type="button" data-act="enlarge"><i class="fa-solid fa-magnifying-glass-plus"></i><span class="lang-en">Enlarge</span><span class="lang-zh hidden">放大</span></button>
            <button type="button" data-act="contract"><i class="fa-solid fa-magnifying-glass-minus"></i><span class="lang-en">Contract</span><span class="lang-zh hidden">縮小</span></button>
            <button type="button" data-act="left"><i class="fa-solid fa-chevron-left"></i><span class="lang-en">Left</span><span class="lang-zh hidden">向左</span></button>
            <button type="button" data-act="right"><i class="fa-solid fa-chevron-right"></i><span class="lang-en">Right</span><span class="lang-zh hidden">向右</span></button>
            <button type="button" data-act="close"><i class="fa-solid fa-xmark"></i><span class="lang-en">Close</span><span class="lang-zh hidden">關閉</span></button>
        </div>
    </div>
    <div id="photoThumbs" class="photo-thumbs"></div>
    <p id="photoCount" class="text-xs text-stone-400 mt-2"></p>`;

    const stage = document.getElementById("photoStage");
    const img = document.getElementById("photoImg");
    const thumbs = document.getElementById("photoThumbs");
    thumbs.innerHTML = photos.map((photo, i) => `<button type="button" class="photo-thumb" data-i="${i}"><img src="${hkbPageEsc(photo.image_id ? hkbPhotoUrl(photo.image_id, "H300") : photo.src)}" alt=""></button>`).join("");

    function applyFrame() {
        const photo = photos[state.i];
        img.src = photo.image_id ? hkbPhotoUrl(photo.image_id) : photo.src;
        img.alt = photo.en || "";
        document.getElementById("photoCaption").innerHTML = hkbPair(photo.en, photo.zh);
        document.getElementById("photoCount").textContent = `${state.i + 1} / ${photos.length}`;
        thumbs.querySelectorAll(".photo-thumb").forEach((btn, i) => btn.classList.toggle("on", i === state.i));
        img.style.transform = `translate(${state.panX}px, ${state.panY}px) scale(${state.scale})`;
        stage.classList.toggle("is-enlarged", state.open);
        stage.classList.toggle("controls-off", !state.controls);
        document.getElementById("photoToggle").setAttribute("aria-pressed", state.controls ? "true" : "false");
        document.body.style.overflow = state.open ? "hidden" : "";
        if (typeof applyLanguage === "function") applyLanguage();
    }

    function flip(step) {
        state.i = (state.i + step + photos.length) % photos.length;
        state.scale = 1;
        state.panX = 0;
        state.panY = 0;
        applyFrame();
    }

    function enlarge() {
        if (!state.open) {
            state.open = true;
            state.scale = 1;
        } else {
            state.scale = Math.min(3, Math.round((state.scale + 0.5) * 10) / 10);
        }
        applyFrame();
    }

    function contract() {
        if (state.scale > 1) {
            state.scale = Math.max(1, Math.round((state.scale - 0.5) * 10) / 10);
            if (state.scale === 1) {
                state.panX = 0;
                state.panY = 0;
            }
        } else if (state.open) {
            state.open = false;
            state.panX = 0;
            state.panY = 0;
        }
        applyFrame();
    }

    function closeViewer() {
        state.open = false;
        state.scale = 1;
        state.panX = 0;
        state.panY = 0;
        applyFrame();
    }

    function act(name) {
        if (name === "left") flip(-1);
        else if (name === "right") flip(1);
        else if (name === "enlarge") enlarge();
        else if (name === "contract") contract();
        else if (name === "close") closeViewer();
    }

    stage.addEventListener("click", (event) => {
        const button = event.target.closest("[data-act]");
        if (button) {
            event.preventDefault();
            act(button.dataset.act);
            return;
        }
        if (event.target.id === "photoToggle" || event.target.closest("#photoToggle")) {
            state.controls = !state.controls;
            applyFrame();
            return;
        }
        if (event.target === img) {
            if (!state.open) enlarge();
            else if (!state.controls) {
                state.controls = true;
                applyFrame();
            }
        }
    });
    thumbs.addEventListener("click", (event) => {
        const button = event.target.closest("[data-i]");
        if (!button) return;
        state.i = parseInt(button.dataset.i, 10);
        state.scale = 1;
        state.panX = 0;
        state.panY = 0;
        applyFrame();
    });

    let drag = null;
    img.addEventListener("pointerdown", (event) => {
        if (!state.open || state.scale <= 1) {
            drag = { x: event.clientX, y: event.clientY, swipe: true };
            return;
        }
        drag = { x: event.clientX, y: event.clientY, panX: state.panX, panY: state.panY, swipe: false };
        img.setPointerCapture(event.pointerId);
    });
    img.addEventListener("pointermove", (event) => {
        if (!drag || drag.swipe) return;
        state.panX = drag.panX + (event.clientX - drag.x);
        state.panY = drag.panY + (event.clientY - drag.y);
        img.style.transform = `translate(${state.panX}px, ${state.panY}px) scale(${state.scale})`;
    });
    img.addEventListener("pointerup", (event) => {
        if (!drag) return;
        const dx = event.clientX - drag.x;
        if (drag.swipe && Math.abs(dx) > 48 && Math.abs(dx) > Math.abs(event.clientY - drag.y)) {
            flip(dx < 0 ? 1 : -1);
        }
        drag = null;
    });

    document.addEventListener("keydown", (event) => {
        if (event.target.matches("input, textarea")) return;
        if (event.key === "ArrowLeft") act("left");
        else if (event.key === "ArrowRight") act("right");
        else if (event.key === "Escape") closeViewer();
        else if (event.key === "+" || event.key === "=") enlarge();
        else if (event.key === "-" || event.key === "_") contract();
    });

    applyFrame();
}

document.addEventListener("DOMContentLoaded", () => {
    const photosEl = document.getElementById("page-photos");
    if (!photosEl || !document.getElementById("photoMount")) return;
    let photos = [];
    try {
        photos = JSON.parse(photosEl.textContent);
    } catch (err) {
        return;
    }
    hkbPhotoViewer(photos);
    if (typeof applyLanguage === "function") applyLanguage();
});
