import {
  View,
  Text,
  StyleSheet,
  ImageBackground,
  Pressable,
} from "react-native";
import React from "react";
import bgImage from "@/assets/images/bg-ai.jpg";
import { Link } from "expo-router";
import { useAuth } from "../../assets/context/AuthContext";

const App = () => {
  const { user } = useAuth();

  return (
    <View style={styles.container}>
      <ImageBackground source={bgImage} resizeMode="cover" style={styles.image}>
        <Text style={styles.text}>CivilAI</Text>
        {user && <Text style={styles.text}>Logged in as: {user.username}</Text>}
        {/* Only show buttons if user is not logged in */}
        {!user && (
          <>
            <Link href="/login" style={{ marginHorizontal: "auto" }} asChild>
              <Pressable style={styles.button}>
                <Text style={styles.buttonText}>Login</Text>
              </Pressable>
            </Link>

            <Link href="/register" style={{ marginHorizontal: "auto" }} asChild>
              <Pressable style={styles.button}>
                <Text style={styles.buttonText}>Register</Text>
              </Pressable>
            </Link>
          </>
        )}
      </ImageBackground>
    </View>
  );
};

export default App;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    flexDirection: "column",
  },
  image: {
    width: "100%",
    height: "100%",
    flex: 1,
    resizeMode: "cover",
    justifyContent: "center",
  },
  text: {
    color: "white",
    fontSize: 42,
    fontWeight: "bold",
    textAlign: "center",
    backgroundColor: "rgba(0,0,0,0.5)",
    marginBottom: 120,
  },
  button: {
    height: 60,
    borderRadius: 20,
    justifyContent: "center",
    backgroundColor: "rgba(0,0,0,0.75)",
    padding: 6,
    marginVertical: 10,
  },
  buttonText: {
    color: "white",
    fontSize: 16,
    fontWeight: "bold",
    textAlign: "center",
    padding: 4,
  },
});
