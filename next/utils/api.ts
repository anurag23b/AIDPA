import axios from 'axios';

if (!process.env.NEXT_PUBLIC_API_URL) {
  throw new Error("API base URL is not defined!");
}
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;

export const fetcher = async (url: string) => {
  const res = await fetch(`${API_BASE_URL}${url}`);
  if (!res.ok) {
    const error = new Error('An error occurred while fetching the data.');
    throw error;
  }
  return res.json();
};

export const postData = async (url: string, data: any) => {
  const response = await axios.post(`${API_BASE_URL}${url}`, data);
  return response.data;
};

export const putData = async (url: string, data: any) => {
  const response = await axios.put(`${API_BASE_URL}${url}`, data);
  return response.data;
};

export const deleteData = async (url: string) => {
  const response = await axios.delete(`${API_BASE_URL}${url}`);
  return response.data;
};
