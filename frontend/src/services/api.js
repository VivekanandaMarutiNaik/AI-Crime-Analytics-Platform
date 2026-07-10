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

export async function getCrimeCategory(district = "") {
  let url = `${BASE_URL}/api/dashboard/crime-category`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
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

export async function getCrimeSeverity(district = "") {
  let url = `${BASE_URL}/api/dashboard/crime-severity`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch crime severity");
  }

  return await response.json();
}

export async function getMonthlyTrend(district = "") {
  let url = `${BASE_URL}/api/dashboard/monthly-trend`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch monthly trend");
  }

  return await response.json();
}

export async function getDistrictWise() {
  const response = await fetch(`${BASE_URL}/api/dashboard/district-wise`);

  if (!response.ok) {
    throw new Error("Failed to fetch district-wise data");
  }

  return await response.json();
}

export async function getCaseStatus(district = "") {
  let url = `${BASE_URL}/api/dashboard/case-status`;

  if (district) {
    url += `?district=${encodeURIComponent(district)}`;
  }

  const response = await fetch(url);

  if (!response.ok) {
    throw new Error("Failed to fetch case status");
  }

  return await response.json();
}