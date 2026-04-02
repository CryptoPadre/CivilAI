import React, { createContext, useContext, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { axiosInstance } from "../api/axios";

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user on app start
  const loadUser = async () => {
    try {
      const token = await AsyncStorage.getItem("access_token");

      if (!token) {
        setUser(null);
        return;
      }

      const { data } = await axiosInstance.get("/dj-rest-auth/user/");
      setUser(data);
    } catch (err) {
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  // Login
  const login = async (email, password) => {
    const { data } = await axiosInstance.post("/dj-rest-auth/login/", {
      email,
      password,
    });

    await AsyncStorage.setItem("access_token", data.access);
    await AsyncStorage.setItem("refresh_token", data.refresh);

    await loadUser();
  };

  // Logout
  const logout = async () => {
    await AsyncStorage.multiRemove(["access_token", "refresh_token"]);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};
