import { View, Text, StyleSheet } from "react-native";
import { useEffect, useState } from "react";
import { axiosInstance } from "../api/axios";

export default function MapWithZoom() {
  const [npcs, setNpcs] = useState([]);

  useEffect(() => {
    axiosInstance
      .get("/npc/")
      .then((response) => {
        console.log("NPC count:", npcs.length);
        setNpcs(response.data.results);
      })
      .catch(console.error);
  }, []);
  return (
    <>
      {npcs.map((npc) => (
        <View style={styles.container} key={npc.id}>
          <Text>
            {npc.first_name} {npc.last_name} - {npc.occupation}
          </Text>
        </View>
      ))}
    </>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});
