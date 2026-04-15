import { useEffect, useState } from "react";
import { Marker } from "react-native-maps";
import { View, Text } from "react-native";
import { axiosInstance } from "../api/axios";

export default function NPCMarker() {
  const [npcs, setNpcs] = useState([]);

  useEffect(() => {
    axiosInstance
      .get("/api/npc/")
      .then((response) => {
        setNpcs(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <>
      {npcs.map((npc) => (
        <Marker
          key={npc.id}
          coordinate={{
            latitude: npc.latitude,
            longitude: npc.longitude,
          }}
          title={npc.first_name}
          description={String(npc.age)}
        >
          <View
            style={{ padding: 5, backgroundColor: "white", borderRadius: 10 }}
          >
            <Text>{npc.icon || "🧍"}</Text>
          </View>
        </Marker>
      ))}
    </>
  );
}
