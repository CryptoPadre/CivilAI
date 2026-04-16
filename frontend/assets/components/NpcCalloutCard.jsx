import { View, Text, StyleSheet, Pressable, ScrollView } from "react-native";

export default function NpcCalloutCard({ npc, loading, onClose }) {
  if (!npc && !loading) return null;

  return (
    <View style={styles.container}>
      {loading ? (
        <Text style={styles.title}>Loading NPC details...</Text>
      ) : (
        <ScrollView>
          {/* HEADER */}
          <Text style={styles.title}>
            {npc.first_name} {npc.last_name}
          </Text>

          {/* BASIC INFO */}
          <Text>Sex: {npc.sex}</Text>
          <Text>Age: {npc.age}</Text>
          <Text>Born: {npc.born_at?.split("T")[0]}</Text>
          <Text>Occupation: {npc.occupation}</Text>
          <Text>Job level: {npc.job_level}</Text>
          <Text>Wealth: {npc.wealth}</Text>

          {/* PERSONALITY */}
          <Text style={styles.section}>Personality</Text>
          <Text>Traits: {npc.personality_traits?.join(", ") || "None"}</Text>
          <Text>Orientation: {npc.sexual_orientation}</Text>
          <Text>Fertility: {npc.fertility}</Text>
          <Text>Adventurous: {npc.is_adventurous ? "Yes" : "No"}</Text>

          {/* FAMILY */}
          <Text style={styles.section}>Family</Text>
          <Text>Mother: {npc.mother || "Unknown"}</Text>
          <Text>Father: {npc.father || "Unknown"}</Text>
          <Text>Kids: {npc.has_kids || "No"}</Text>
          <Text>
            Previous partners:
            {npc.previous_partners?.length
              ? ` ${npc.previous_partners.join(", ")}`
              : " None"}
          </Text>

          {/* STATS */}
          <Text style={styles.section}>Stats</Text>
          <Text>Fitness: {npc.fitness_level}</Text>
          <Text>Intelligence: {npc.intelligence_level}</Text>
          <Text>Charisma: {npc.charisma_level}</Text>
          <Text>Empathy: {npc.empathy_level}</Text>
          <Text>Morality: {npc.morality_level}</Text>
          <Text>Aggression: {npc.aggression_level}</Text>
          <Text>Stress: {npc.stress_level}</Text>
          <Text>Happiness: {npc.happiness_level}</Text>
          <Text>Health: {npc.health_level}</Text>
          <Text>Energy: {npc.energy_level}</Text>
          <Text>Introversion: {npc.introversion_level}</Text>

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
});
