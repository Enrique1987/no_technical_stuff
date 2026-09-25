const grid = document.querySelector("#video-grid");
const filters = document.querySelector("#filters");
const search = document.querySelector("#search");
const resultTitle = document.querySelector("#result-title");
const resultCount = document.querySelector("#result-count");
const emptyState = document.querySelector("#empty-state");
const dialog = document.querySelector("#player-dialog");
const player = document.querySelector("#player");
const loader = document.querySelector("#loader");
const loaderProgress = document.querySelector("#loader-progress");
const playerError = document.querySelector("#player-error");

const state = { videos: [], category: "all", query: "", objectUrl: null, controller: null };
const videoParam = "video";

function normalized(value) {
  return value.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
}

function visibleVideos() {
  const query = normalized(state.query.trim());
  return state.videos.filter((video) => {
    const inCategory = state.category === "all" || video.category === state.category;
    const haystack = normalized(`${video.topic} ${video.creator} ${video.categoryLabel} ${video.filename}`);
    return inCategory && (!query || haystack.includes(query));
  });
}

function renderCards() {
  const videos = visibleVideos();
  const selected = filters.querySelector(`[data-category="${state.category}"]`);
  resultTitle.textContent = state.category === "all" ? "All videos" : selected?.dataset.label || "Videos";
  resultCount.textContent = `${videos.length} ${videos.length === 1 ? "result" : "results"}`;
  emptyState.hidden = videos.length > 0;

  grid.replaceChildren(...videos.map((video) => {
    const card = document.createElement("button");
    card.className = "video-card";
    card.type = "button";
    card.innerHTML = `
      <span class="card-top">
        <span class="pill">${video.categoryLabel}</span>
        <span class="play-mark" aria-hidden="true">▶</span>
      </span>
      <h3>${video.topic}</h3>
      <span class="creator">${video.creator}</span>`;
    card.addEventListener("click", () => openVideo(video));
    return card;
  }));
}

function renderFilters() {
  const counts = new Map();
  state.videos.forEach((video) => counts.set(video.category, {
    label: video.categoryLabel,
    count: (counts.get(video.category)?.count || 0) + 1,
  }));
  const options = [["all", { label: "All", count: state.videos.length }], ...counts.entries()];
  filters.replaceChildren(...options.map(([id, item]) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = `filter${id === state.category ? " active" : ""}`;
    button.dataset.category = id;
    button.dataset.label = item.label;
    button.textContent = `${item.label} · ${item.count}`;
    button.addEventListener("click", () => {
      state.category = id;
      filters.querySelectorAll(".filter").forEach((filter) => filter.classList.toggle("active", filter === button));
      renderCards();
    });
    return button;
  }));
}

function releaseVideo() {
  state.controller?.abort();
  state.controller = null;
  player.pause();
  player.removeAttribute("src");
  player.load();
  if (state.objectUrl) URL.revokeObjectURL(state.objectUrl);
  state.objectUrl = null;
}

async function loadVideo(video) {
  releaseVideo();
  loader.hidden = false;
  playerError.hidden = true;
  player.hidden = true;
  loaderProgress.textContent = "Downloading from Git LFS";
  state.controller = new AbortController();

  try {
    const response = await fetch(video.mediaUrl, { signal: state.controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const total = Number(response.headers.get("content-length")) || 0;
    let bytes;

    if (response.body && total) {
      const reader = response.body.getReader();
      const chunks = [];
      let received = 0;
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        chunks.push(value);
        received += value.length;
        loaderProgress.textContent = `Downloading · ${Math.round((received / total) * 100)}%`;
      }
      bytes = new Uint8Array(received);
      let offset = 0;
      for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    } else {
      bytes = new Uint8Array(await response.arrayBuffer());
    }

    state.objectUrl = URL.createObjectURL(new Blob([bytes], { type: "video/mp4" }));
    player.src = state.objectUrl;
    player.hidden = false;
    loader.hidden = true;
    player.load();
  } catch (error) {
    if (error.name === "AbortError") return;
    console.error(error);
    loader.hidden = true;
    playerError.hidden = false;
  }
}

function setVideoParam(videoId) {
  const url = new URL(window.location.href);
  if (videoId) url.searchParams.set(videoParam, videoId);
  else url.searchParams.delete(videoParam);
  window.history.replaceState({}, "", url);
}

function openVideo(video, { updateUrl = true } = {}) {
  document.querySelector("#player-category").textContent = video.categoryLabel;
  document.querySelector("#player-title").textContent = video.topic;
  document.querySelector("#player-creator").textContent = video.creator;
  document.querySelector("#instagram-link").href = video.instagram;
  document.querySelector("#download-link").href = video.mediaUrl;
  if (updateUrl) setVideoParam(video.id);
  if (!dialog.open) dialog.showModal();
  loadVideo(video);
}

document.querySelector("#close-player").addEventListener("click", () => dialog.close());
dialog.addEventListener("close", () => {
  releaseVideo();
  setVideoParam(null);
});
dialog.addEventListener("click", (event) => { if (event.target === dialog) dialog.close(); });
search.addEventListener("input", () => { state.query = search.value; renderCards(); });
document.querySelector("#clear-search").addEventListener("click", () => {
  state.category = "all";
  state.query = "";
  search.value = "";
  renderFilters();
  renderCards();
});

fetch("videos.json")
  .then((response) => {
    if (!response.ok) throw new Error("The catalogue could not be loaded");
    return response.json();
  })
  .then((videos) => {
    state.videos = videos;
    document.querySelector("#video-count").textContent = videos.length;
    document.querySelector("#category-count").textContent = new Set(videos.map((video) => video.category)).size;
    renderFilters();
    renderCards();
    const requestedId = new URLSearchParams(window.location.search).get(videoParam);
    const requestedVideo = videos.find((video) => video.id === requestedId || video.filename === requestedId);
    if (requestedVideo) openVideo(requestedVideo, { updateUrl: false });
  })
  .catch((error) => {
    console.error(error);
    resultTitle.textContent = "The catalogue could not be loaded";
  });
