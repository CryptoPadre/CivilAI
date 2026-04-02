import AsyncStorage from "@react-native-async-storage/async-storage";
import jwtDecode from "jwt-decode";

export const setTokenTimestamp = async (data) => {
  const refreshTokenTimestamp = jwtDecode(data?.access).exp;
  await AsyncStorage.setItem(
    "refreshTokenTimestamp",
    String(refreshTokenTimestamp),
  );
};

export const shouldRefreshToken = async () => {
  const value = await AsyncStorage.getItem("refreshTokenTimestamp");
  return !!value;
};

export const removeTokenTimestamp = async () => {
  await AsyncStorage.removeItem("refreshTokenTimestamp");
};
