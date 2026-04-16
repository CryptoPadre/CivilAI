import { useEffect, useState } from "react";
import { Marker } from "react-native-maps";
import { View, Text } from "react-native";
import { axiosInstance } from "../api/axios";

export default function NPCMarker({ region }) {
  const [npcs, setNpcs] = useState([]);

  useEffect(() => {
    if (!region) return;

    if (region.latitudeDelta > 40) {
      setNpcs([]);
      return;
    }

    const timeout = setTimeout(() => {
      const min_lat = region.latitude - region.latitudeDelta / 2;
      const max_lat = region.latitude + region.latitudeDelta / 2;
      const min_lng = region.longitude - region.longitudeDelta / 2;
      const max_lng = region.longitude + region.longitudeDelta / 2;

      axiosInstance
        .get("/npc/", {
          params: { min_lat, max_lat, min_lng, max_lng },
        })
        .then((res) => setNpcs(res.data.results))
        .catch(console.error);
    }, 400); //

    return () => clearTimeout(timeout);
  }, [region]);

  return (
    <>
      {npcs.map((npc) => (
        <Marker
          key={npc.id}
          coordinate={{
            latitude: npc.latitude,
            longitude: npc.longitude,
          }}
          title={npc.first_name + " " + npc.last_name}
        >
          <View style={{ padding: 5, borderRadius: 10 }}>
            <Text>🧍</Text>
          </View>
        </Marker>
      ))}
    </>
  );
}
