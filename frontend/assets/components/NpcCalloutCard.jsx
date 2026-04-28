import { View, Text, StyleSheet, Pressable, ScrollView } from "react-native";
import { getNpcBiography } from "../constants/npcBiography";

export default function NpcCalloutCard({ npc, loading, onClose }) {
  if (!npc && !loading) return null;

  return (
    <View style={styles.container}>
      {loading ? (
        <Text style={styles.title}>Loading details...</Text>
      ) : (
        <ScrollView>
          <Text style={styles.bioText}>{getNpcBiography(npc)}</Text>

          {/* CLOSE BUTTON */}
          <Pressable style={styles.button} onPress={onClose}>
            <Text style={styles.buttonText}>Close</Text>
          </Pressable>
        </ScrollView>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    position: "absolute",
    left: 20,
    right: 20,
    bottom: 30,
    maxHeight: 500,
    backgroundColor: "white",
    borderRadius: 14,
    padding: 16,
    elevation: 6,
  },

  title: {
    fontSize: 20,
    fontWeight: "bold",
    marginBottom: 10,
  },

  section: {
    marginTop: 14,
    fontWeight: "bold",
  },

  button: {
    marginTop: 14,
    backgroundColor: "#222",
    padding: 10,
    borderRadius: 8,
    alignItems: "center",
  },

  buttonText: {
    color: "white",
    fontWeight: "600",
  },
  bioText: {
    fontSize: 15,
    lineHeight: 22,
    color: "#222",
  },
});
