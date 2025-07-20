// filters.js - Handles region/event filters, search, and date range

const regionFilter = document.getElementById('region-filter');
const eventTypeFilter = document.getElementById('event-type-filter');
const searchInput = document.getElementById('search-input');
const dateRange = document.getElementById('date-range');
const clearFiltersBtn = document.getElementById('clear-filters');

const REGIONS = ["Middle East", "Europe", "Asia", "Americas", "US", "China", "Russia", "Iran"];
const EVENT_TYPES = ["sanctions", "military", "trade", "energy", "diplomacy", "cyber", "political"];

// Render region filter buttons
displayRegionFilter();
function displayRegionFilter() {
  regionFilter.innerHTML = REGIONS.map(region =>
    `<button class="btn btn-outline-info btn-sm m-1 region-btn" data-region="${region}">${region}</button>`
  ).join('');
}
// Render event type filter buttons
displayEventTypeFilter();
function displayEventTypeFilter() {
  eventTypeFilter.innerHTML = EVENT_TYPES.map(type =>
    `<button class="btn btn-outline-warning btn-sm m-1 event-btn" data-event="${type}">${type}</button>`
  ).join('');
}

// Filter state
window.currentFilters = {};

// Region filter
regionFilter.addEventListener('click', e => {
  if (e.target.classList.contains('region-btn')) {
    // Remove 'active' from all region buttons
    regionFilter.querySelectorAll('.region-btn').forEach(btn => btn.classList.remove('active'));
    // Add 'active' to the clicked button
    e.target.classList.add('active');
    window.currentFilters.region = e.target.dataset.region;
    fetchAndUpdate();
  }
});
// Event type filter
eventTypeFilter.addEventListener('click', e => {
  if (e.target.classList.contains('event-btn')) {
    eventTypeFilter.querySelectorAll('.event-btn').forEach(btn => btn.classList.remove('active'));
    e.target.classList.add('active');
    window.currentFilters.event_type = e.target.dataset.event;
    fetchAndUpdate();
  }
});
// Search filter
searchInput.addEventListener('input', () => {
  window.currentFilters.search = searchInput.value.trim();
  fetchAndUpdate();
});
// Date range filter
dateRange.addEventListener('change', () => {
  window.currentFilters.date = dateRange.value;
  fetchAndUpdate();
});
// Clear filters
clearFiltersBtn.addEventListener('click', () => {
  window.currentFilters = {};
  searchInput.value = '';
  dateRange.value = '';
  // Remove 'active' from all filter buttons
  regionFilter.querySelectorAll('.region-btn').forEach(btn => btn.classList.remove('active'));
  eventTypeFilter.querySelectorAll('.event-btn').forEach(btn => btn.classList.remove('active'));
  fetchAndUpdate();
});

// Fetch and update dashboard
async function fetchAndUpdate() {
  // Fetch all news, then filter client-side for event_type, search, date
  let url = '/api/news/latest';
  if (window.currentFilters.region) {
    url = `/api/news/by-region/${encodeURIComponent(window.currentFilters.region)}`;
  }
  try {
    const res = await fetch(url);
    const data = await res.json();
    let news = data.news || [];
    // Event type filter
    if (window.currentFilters.event_type) {
      news = news.filter(n => n.event_type === window.currentFilters.event_type);
    }
    // Search filter
    if (window.currentFilters.search) {
      const q = window.currentFilters.search.toLowerCase();
      news = news.filter(n => n.title && n.title.toLowerCase().includes(q));
    }
    // Date filter
    if (window.currentFilters.date) {
      news = news.filter(n => n.publish_date && n.publish_date.slice(0,10) === window.currentFilters.date);
    }
    window.fetchLatestNews = window.fetchLatestNews || (()=>{});
    window.updateCharts = window.updateCharts || (()=>{});
    window.fetchLatestNews(window.currentFilters);
    window.updateCharts(news);
  } catch (err) {
    // fallback: just update news
    window.fetchLatestNews(window.currentFilters);
  }
} 