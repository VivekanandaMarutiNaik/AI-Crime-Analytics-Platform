const BASE_URL = "http://127.0.0.1:8000";

export async function getDashboardSummary(district = "") {
  let url = `${BASE_URL}/api/dashboard/summary`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard summary");
  }

  return await response.json();
}

export async function getCrimes(limit = 100, district = "") {
  let url = `${BASE_URL}/crimes?limit=${limit}`;

  if (district) {
    url += `&district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch crimes");
  }

  return await response.json();
}

export async function getDistricts() {
  const response = await fetch(`${BASE_URL}/districts`);

  if (!response.ok) {
    throw new Error("Failed to fetch districts");
  }

  return await response.json();
}

export async function getHotspots(district = "") {
  let url = `${BASE_URL}/hotspots`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch hotspots");
  }

  return await response.json();
}

export async function getExistingCCTV(district = "") {
  let url = `${BASE_URL}/api/cctv/existing`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch existing CCTV locations");
  }

  return await response.json();
}

export async function getRecommendedCCTV(district = "") {
  let url = `${BASE_URL}/api/cctv/recommendations`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch CCTV recommendations");
  }

  return await response.json();
}

export async function getDashboardCharts(district = "") {
  let url = `${BASE_URL}/api/dashboard/charts`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch dashboard charts");
  }

  return await response.json();
}

export async function getAIInsights(district = "") {
  let url = `${BASE_URL}/api/dashboard/insights`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch AI insights");
  }

  return await response.json();
}