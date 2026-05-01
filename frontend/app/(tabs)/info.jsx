import { Text, StyleSheet, ScrollView, Platform } from "react-native";
import React from "react";
import { useColorScheme } from "react-native";

export default function Info() {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === "dark";
  const isWeb = Platform.OS === "web";

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text
        style={[
          styles.header,
          { color: isDark ? "white" : "black" },
          { marginTop: isWeb ? 20 : 100 },
        ]}
      >
        Info about CivilAI
      </Text>

      <Text
        style={[
          styles.text,
          { color: isDark ? "white" : "black" },
          { textAlign: isWeb ? "center" : "left" },
        ]}
      >
        It is a civilization simulation where the user can observe the daily
        life of NPCs.
        {"\n\n"}1 real day equals 1 year in the game.
        {"\n\n"}
        Daily tasks run every 5 minutes and update NPC status and map position.
        {"\n\n"}
        Every 24 hours NPCs age and may have children.
        {"\n\n"}
        Every 96 hours global events occur and NPCs choose their leader.
        {"\n\n"}
        Some NPCs may have degenerative conditions affecting their surroundings.
        {"\n\n"}
        The map cannot be zoomed out to keep the exploration experience focused.
        {"\n\n"}
        Tap a marker to inspect NPC details.
        {"\n\n"}
        Development phases:
        {"\n\n"}
        Phase 1: Start simulation with 1000 NPCs + aging + breeding + global
        events
        {"\n\n"}
        Phase 2: NPC friendships, unions and communities
        {"\n\n"}
        Phase 3: Communities become towns, cities and countries
        {"\n\n"}
        Phase 4: Fully autonomous ecosystem learning from history
      </Text>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingBottom: 80,
  },
  header: {
    fontFamily:
      Platform.OS === "IOS" ? "AcademyEngravedLetPlain" : "sans-serif-medium",
    textAlign: "center",
    fontWeight: "bold",
    fontSize: 24,
  },
  text: {
    fontFamily:
      Platform.OS === "IOS" ? "AcademyEngravedLetPlain" : "sans-serif-medium",
    fontWeight: "500",
    fontSize: 18,
    marginTop: 40,
    paddingHorizontal: 20,
    lineHeight: 26,
  },
});
