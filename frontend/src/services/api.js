const API_BASE_URL = "http://127.0.0.1:8000";

export async function getMetadata() {
  const response = await fetch(`${API_BASE_URL}/metadata`);

  if (!response.ok) {
    throw new Error("Failed to fetch metadata");
  }

  return response.json();
}

export async function predictPrice(flightData) {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(flightData),
  });

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "Prediction failed");
  }

  return response.json();
}