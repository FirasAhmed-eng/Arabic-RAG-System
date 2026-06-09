import axios from "axios";

const API_URL = "http://localhost:8000";

export async function getFiles(): Promise<string[]> {
  const response = await axios.get(`${API_URL}/api/files`);

  return response.data.files;
}
