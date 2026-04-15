import { useEffect, useState } from "react";
import { Marker } from "react-native-maps";
import { View, Text } from "react-native";
import { axiosInstance } from "../api/axios";

export default function NPCMarker() {
  const [npc, setNpc] = useState(null);

  useEffect(() => {
    axiosInstance
      .get("/npc/2/")
      .then((response) => {
        setNpc(response.data);
      })
      .catch(console.error);
  }, []);

  if (!npc) return null;

  return (
    <Marker
      coordinate={{
        latitude: npc.latitude,
        longitude: npc.longitude,
      }}
      title={npc.first_name}
    >
      <View style={{ padding: 5, backgroundColor: "white", borderRadius: 10 }}>
        <Text>{npc.icon || "🧍"}</Text>
      </View>
    </Marker>
  );
}
