const BASE_URL = "http://localhost:8000"; //fix later

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {});
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}