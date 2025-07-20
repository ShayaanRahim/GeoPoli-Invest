// dashboard.js - Handles fetching and displaying news articles

const API_BASE = '/api/news';
const newsList = document.getElementById('news-list');
const newsLoading = document.getElementById('news-loading');
const newsEmpty = document.getElementById('news-empty');
const refreshBtn = document.getElementById('refresh-btn');

async function fetchLatestNews(filters = {}) {
  showLoading();
  let url = `${API_BASE}/latest`;
  // Add region filter if present
  if (filters.region) url = `${API_BASE}/by-region/${encodeURIComponent(filters.region)}`;
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error('Failed to fetch news');
    const data = await res.json();
    renderNews(data.news || []);
  } catch (err) {
    showError('Could not load news. Please try again.');
    renderNews([]);
  } finally {
    hideLoading();
  }
}

function renderNews(news) {
  newsList.innerHTML = '';
  if (!news || news.length === 0) {
    newsEmpty.classList.remove('d-none');
    return;
  }
  newsEmpty.classList.add('d-none');
  news.forEach(article => {
    const card = document.createElement('div');
    card.className = 'card p-3 col-12';
    card.innerHTML = `
      <div class="card-body">
        <h5 class="card-title">${escapeHTML(article.title)}</h5>
        <h6 class="card-subtitle mb-2 text-muted">${escapeHTML(article.source || '')} &middot; <span class="news-date">${formatDate(article.publish_date)}</span></h6>
        <p class="card-text">${escapeHTML(article.content ? article.content.slice(0, 180) : '')}${article.content && article.content.length > 180 ? '...' : ''}</p>
        <div class="d-flex flex-wrap gap-2 mt-2">
          ${article.region ? `<span class="badge bg-info">${escapeHTML(article.region)}</span>` : ''}
          ${article.event_type ? `<span class="badge bg-warning text-dark">${escapeHTML(article.event_type)}</span>` : ''}
          ${article.market_sentiment ? `<span class="badge ${sentimentBadge(article.market_sentiment)}">${escapeHTML(article.market_sentiment)}</span>` : ''}
        </div>
      </div>
    `;
    newsList.appendChild(card);
  });
}

function showLoading() {
  newsLoading.style.display = 'block';
}
function hideLoading() {
  newsLoading.style.display = 'none';
}
function showError(msg) {
  showToast(msg, 'danger');
}
function showToast(msg, type = 'info') {
  let toast = document.querySelector('.toast');
  if (!toast) {
    toast = document.createElement('div');
    toast.className = 'toast';
    document.body.appendChild(toast);
  }
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3500);
}
function formatDate(dateStr) {
  if (!dateStr) return '';
  const d = new Date(dateStr);
  return d.toLocaleString(undefined, { dateStyle: 'medium', timeStyle: 'short' });
}
function sentimentBadge(sentiment) {
  if (sentiment === 'positive') return 'bg-success';
  if (sentiment === 'negative') return 'bg-danger';
  if (sentiment === 'neutral') return 'bg-secondary';
  return 'bg-info';
}
function escapeHTML(str) {
  return (str || '').replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','\'':'&#39;','"':'&quot;'}[c]));
}

// Refresh button
if (refreshBtn) {
  refreshBtn.addEventListener('click', async () => {
    showLoading();
    try {
      await fetch('/api/news/refresh', { method: 'POST' });
      await fetchLatestNews(window.currentFilters || {});
      showToast('News refreshed!', 'success');
    } catch {
      showError('Failed to refresh news.');
    } finally {
      hideLoading();
    }
  });
}

// Initial load
window.addEventListener('DOMContentLoaded', () => {
  fetchLatestNews();
});

// Expose for filters.js
window.fetchLatestNews = fetchLatestNews; 