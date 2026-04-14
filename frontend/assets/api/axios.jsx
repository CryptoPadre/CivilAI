import axios from "axios";
import AsyncStorage from "@react-native-async-storage/async-storage";

const BASE_URL = "https://civilai.onrender.com/api/";

export const axiosInstance = axios.create({
  baseURL: BASE_URL,
});

// Attach JWT token
axiosInstance.interceptors.request.use(async (config) => {
  const token = await AsyncStorage.getItem("access_token");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// Refresh token on 401
axiosInstance.interceptors.response.use(
  (res) => res,
  async (err) => {
    const originalRequest = err.config;

    if (err.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refresh = await AsyncStorage.getItem("refresh_token");

        const { data } = await axios.post(
          `${BASE_URL}dj-rest-auth/token/refresh/`,
          { refresh },
        );

        await AsyncStorage.setItem("access_token", data.access);

        originalRequest.headers.Authorization = `Bearer ${data.access}`;
        return axiosInstance(originalRequest);
      } catch (refreshError) {
        await AsyncStorage.multiRemove(["access_token", "refresh_token"]);
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(err);
  },
);
