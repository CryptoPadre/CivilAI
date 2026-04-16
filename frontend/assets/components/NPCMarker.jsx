import { useEffect, useState } from "react";
import { Marker } from "react-native-maps";
import { View, Text } from "react-native";
import { axiosInstance } from "../api/axios";

export default function NPCMarker({ region }) {
  const [npcs, setNpcs] = useState([]);

  useEffect(() => {
    if (!region) return;

    const min_lat = region.latitude - region.latitudeDelta / 2;
    const max_lat = region.latitude + region.latitudeDelta / 2;
    const min_lng = region.longitude - region.longitudeDelta / 2;
    const max_lng = region.longitude + region.longitudeDelta / 2;

    axiosInstance
      .get("/npc/", {
        params: { min_lat, max_lat, min_lng, max_lng },
      })
      .then((response) => {
        setNpcs(response.data.results);
      })
      .catch(console.error);
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
          title={npc.first_name}
        >
          <View
            style={{ padding: 5, backgroundColor: "white", borderRadius: 10 }}
          >
            {/*<Text>{npc.last_name}</Text>*/}
          </View>
        </Marker>
      ))}
    </>
  );
}
