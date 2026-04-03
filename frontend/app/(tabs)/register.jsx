import React, { useState } from "react";
import {
  View,
  Text,
  TextInput,
  Button,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from "react-native";
import { useRouter } from "expo-router";
import axios from "axios";

export default function Register() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password1: "",
    password2: "",
  });

  const { username, email, password1, password2 } = formData;
  const [errors, setErrors] = useState({});

  const router = useRouter();

  const validateField = (name, value) => {
    setErrors((prev) => {
      const newErrors = { ...prev };

      if (name === "username" && !value.trim()) {
        newErrors.username = ["Username is required."];
      } else if (name === "username") {
        delete newErrors.username;
      }

      if (name === "email" && !value.includes("@")) {
        newErrors.email = ["Enter a valid email."];
      } else if (name === "email") {
        delete newErrors.email;
      }

      if (name === "password1" && value.length < 8) {
        newErrors.password1 = ["Min 8 characters."];
      } else if (name === "password1") {
        delete newErrors.password1;
      }

      if (name === "password2" && value !== password1) {
        newErrors.password2 = ["Passwords do not match."];
      } else if (name === "password2") {
        delete newErrors.password2;
      }

      return newErrors;
    });
  };

  const handleSubmit = async () => {
    const newErrors = {};
    if (!username) newErrors.username = ["Required"];
    if (!email) newErrors.email = ["Required"];
    if (!password1) newErrors.password1 = ["Required"];
    if (password1 !== password2) newErrors.password2 = ["Passwords must match"];

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    try {
      await axios.post(
        "https://civilai.onrender.com/api/dj-rest-auth/registration/",
        formData,
      );

      // after successful registration → go to login
      router.replace("/login");
    } catch (err) {
      console.log(err.response?.data);
      if (err.response?.data) {
        setErrors(err.response.data);
      } else {
        setErrors({ general: ["Registration failed"] });
      }
    }
  };

  return (
    <KeyboardAvoidingView
      behavior="padding"
      style={styles.container}
      keyboardVerticalOffset={Platform.OS === "ios" ? 100 : 0}
    >
      <Text style={styles.title}>Register</Text>

      <TextInput
        style={styles.input}
        placeholder="Username"
        value={username}
        onChangeText={(text) => {
          setFormData((prev) => ({ ...prev, username: text }));
          validateField("username", text);
        }}
      />
      {errors.username && <Text style={styles.error}>{errors.username}</Text>}

      <TextInput
        style={styles.input}
        placeholder="Email"
        value={email}
        onChangeText={(text) => {
          setFormData((prev) => ({ ...prev, email: text }));
          validateField("email", text);
        }}
      />
      {errors.email && <Text style={styles.error}>{errors.email}</Text>}

      <TextInput
        style={styles.input}
        placeholder="Password"
        secureTextEntry
        value={password1}
        onChangeText={(text) => {
          setFormData((prev) => ({ ...prev, password1: text }));
          validateField("password1", text);
        }}
      />
      {errors.password1 && <Text style={styles.error}>{errors.password1}</Text>}

      <TextInput
        style={styles.input}
        placeholder="Confirm Password"
        secureTextEntry
        value={password2}
        onChangeText={(text) => {
          setFormData((prev) => ({ ...prev, password2: text }));
          validateField("password2", text);
        }}
      />
      {errors.password2 && <Text style={styles.error}>{errors.password2}</Text>}

      {errors.general && <Text style={styles.error}>{errors.general}</Text>}

      <Button title="Register" onPress={handleSubmit} />

      <TouchableOpacity onPress={() => router.replace("/login")}>
        <Text style={styles.link}>Already have an account? Login</Text>
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
  title: {
    fontSize: 28,
    textAlign: "center",
    marginBottom: 20,
  },
  input: {
    borderWidth: 1,
    borderColor: "#ccc",
    borderRadius: 8,
    padding: 12,
    marginBottom: 10,
    textAlign: "center",
  },
  error: {
    color: "red",
    textAlign: "center",
    marginBottom: 8,
  },
  link: {
    marginTop: 20,
    textAlign: "center",
    color: "green",
  },
});
