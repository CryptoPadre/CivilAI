import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  TouchableOpacity,
  StyleSheet,
  Image,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import { useAuth } from "../../assets/context/AuthContext";

export default function Login() {
  const [signInData, setSignInData] = useState({
    username: "",
    password: "",
  });

  const { username, password } = signInData;
  const [errors, setErrors] = useState({});

  const router = useRouter();
  const { login } = useAuth();

  const validateField = (name, value) => {
    setErrors((prev) => {
      const newErrors = { ...prev };

      if (name === "username" && !value.trim()) {
        newErrors.username = ["Username cannot be empty."];
      } else {
        delete newErrors.username;
      }

      if (name === "password" && value.length < 8) {
        newErrors.password = ["Min 8 characters."];
      } else {
        delete newErrors.password;
      }

      return newErrors;
    });
  };

  const handleSubmit = async () => {
    try {
      await login(username, password);
      router.replace("/map");
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

      <TouchableOpacity>
        <Text style={styles.link}>Don’t have an account? Sign up now!</Text>
      </TouchableOpacity>
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
  errorText: {
    marginBottom: 10,
    color: "red",
    textAlign: "center",
  },
  link: {
    marginTop: 20,
    textAlign: "center",
    color: "green",
  },
  image: {
    width: 200,
    height: 400,
    alignSelf: "center",
    marginBottom: 50,
  },
});
