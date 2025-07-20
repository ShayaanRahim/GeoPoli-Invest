// charts.js - Handles Chart.js visualizations for the dashboard

let regionBarChart, eventPieChart, sentimentLineChart;

function renderRegionBarChart(data) {
  const ctx = document.getElementById('region-bar-chart').getContext('2d');
  if (regionBarChart) regionBarChart.destroy();
  regionBarChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: 'News Volume',
        data: data.values,
        backgroundColor: '#4fd1c5',
        borderRadius: 6
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { display: false } },
      scales: { x: { grid: { color: '#23272f' } }, y: { grid: { color: '#23272f' } } }
    }
  });
}

function renderEventPieChart(data) {
  const ctx = document.getElementById('event-pie-chart').getContext('2d');
  if (eventPieChart) eventPieChart.destroy();
  eventPieChart = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: data.labels,
      datasets: [{
        data: data.values,
        backgroundColor: ['#4fd1c5', '#e53e3e', '#4299e1', '#ecc94b', '#38a169', '#a0aec0', '#f5f6fa']
      }]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom' } }
    }
  });
}

function renderSentimentLineChart(data) {
  const ctx = document.getElementById('sentiment-line-chart').getContext('2d');
  if (sentimentLineChart) sentimentLineChart.destroy();
  sentimentLineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data.labels,
      datasets: [
        {
          label: 'Positive',
          data: data.positive,
          borderColor: '#38a169',
          backgroundColor: 'rgba(56,161,105,0.2)',
          tension: 0.3
        },
        {
          label: 'Negative',
          data: data.negative,
          borderColor: '#e53e3e',
          backgroundColor: 'rgba(229,62,62,0.2)',
          tension: 0.3
        },
        {
          label: 'Neutral',
          data: data.neutral,
          borderColor: '#a0aec0',
          backgroundColor: 'rgba(160,174,192,0.2)',
          tension: 0.3
        }
      ]
    },
    options: {
      responsive: true,
      plugins: { legend: { position: 'bottom' } },
      scales: { x: { grid: { color: '#23272f' } }, y: { grid: { color: '#23272f' } } }
    }
  });
}

// Example: updateCharts(news)
function updateCharts(news) {
  // Bar: News volume by region
  const regionCounts = {};
  const eventCounts = {};
  const sentimentTimeline = {};
  news.forEach(n => {
    // Region
    if (n.region) regionCounts[n.region] = (regionCounts[n.region] || 0) + 1;
    // Event type
    if (n.event_type) eventCounts[n.event_type] = (eventCounts[n.event_type] || 0) + 1;
    // Sentiment over time (by date)
    const date = n.publish_date ? n.publish_date.slice(0, 10) : 'Unknown';
    if (!sentimentTimeline[date]) sentimentTimeline[date] = { positive: 0, negative: 0, neutral: 0 };
    if (n.market_sentiment === 'positive') sentimentTimeline[date].positive++;
    else if (n.market_sentiment === 'negative') sentimentTimeline[date].negative++;
    else sentimentTimeline[date].neutral++;
  });
  renderRegionBarChart({
    labels: Object.keys(regionCounts),
    values: Object.values(regionCounts)
  });
  renderEventPieChart({
    labels: Object.keys(eventCounts),
    values: Object.values(eventCounts)
  });
  // Line chart
  const sortedDates = Object.keys(sentimentTimeline).sort();
  renderSentimentLineChart({
    labels: sortedDates,
    positive: sortedDates.map(d => sentimentTimeline[d].positive),
    negative: sortedDates.map(d => sentimentTimeline[d].negative),
    neutral: sortedDates.map(d => sentimentTimeline[d].neutral)
  });
}

// Listen for news updates from dashboard.js
window.addEventListener('DOMContentLoaded', () => {
  window.updateCharts = updateCharts;
}); 