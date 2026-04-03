import React, { useState, useEffect } from "react";
import {
  Text,
  TextInput,
  Button,
  StyleSheet,
  Image,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useAuth } from "../../assets/context/AuthContext";
import { useRouter } from "expo-router";

export default function Login() {
  const [signInData, setSignInData] = useState({ username: "", password: "" });
  const { username, password } = signInData;
  const [errors, setErrors] = useState({});

  const { login, user } = useAuth();
  const router = useRouter();
  // Redirect logged-in user to main page automatically
  useEffect(() => {
    if (user) {
      router.replace("/");
    }
  }, [user]);

  const validateField = (name, value) => {
    setErrors((prev) => {
      const newErrors = { ...prev };
      if (name === "username" && !value.trim()) {
        newErrors.username = ["Username cannot be empty."];
      } else delete newErrors.username;

      if (name === "password" && value.length < 8) {
        newErrors.password = ["Min 8 characters."];
      } else delete newErrors.password;

      return newErrors;
    });
  };

  const handleSubmit = async () => {
    if (!username || !password) {
      setErrors({ general: ["Fill in both fields"] });
      return;
    }

    try {
      await login(username, password);
    } catch (err) {
      setErrors({ general: ["Invalid credentials"] });
    }
  };

  return (
    <KeyboardAvoidingView
      behavior="padding"
      style={styles.container}
      keyboardVerticalOffset={Platform.OS === "ios" ? 100 : 0}
    >
      <Image
        source={require("@/assets/images/loginimg.png")}
        style={styles.image}
      />
      {errors.general && (
        <Text style={styles.errorText}>{errors.general[0]}</Text>
      )}
      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={(text) => {
          setSignInData((prev) => ({ ...prev, username: text }));
          validateField("username", text);
        }}
      />
      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password}
        onChangeText={(text) => {
          setSignInData((prev) => ({ ...prev, password: text }));
          validateField("password", text);
        }}
      />
      <Button title="Login" onPress={handleSubmit} />
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 20,
    backgroundColor: "#fff",
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    marginBottom: 10,
    textAlign: "center",
    backgroundColor: "green",
    color: "white",
  },
  errorText: { marginBottom: 10, color: "red", textAlign: "center" },
  image: { width: 200, height: 400, alignSelf: "center", marginBottom: 50 },
});
