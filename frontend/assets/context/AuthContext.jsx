import React, { createContext, useContext, useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { axiosInstance } from "../api/axios";
import axios from "axios";

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  // Load user on app start
  const loadUser = async () => {
    try {
      const token = await AsyncStorage.getItem("access_token");

      if (!token) return setUser(null);

      const res = await axios.get(
        "https://civilai.onrender.com/api/dj-rest-auth/user/",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      setUser(res.data);
    } catch (err) {
      console.log("USER ERROR:", err.response?.data || err.message);
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  // Login
  const login = async (username, password) => {
    try {
      const res = await axiosInstance.post("/token/", {
        username,
        password,
      });

      console.log("LOGIN RESPONSE:", res.data);

      await AsyncStorage.setItem("access_token", res.data.access);
      await AsyncStorage.setItem("refresh_token", res.data.refresh);

      await loadUser();
    } catch (err) {
      console.log("🔥 LOGIN ERROR FULL:", err.response?.data || err.message);
      throw err; // IMPORTANT
    }
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
