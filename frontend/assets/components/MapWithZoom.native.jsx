import MapView, { Marker } from "react-native-maps";
import { View, StyleSheet, Text } from "react-native";
import { useState, useRef, useEffect } from "react";
import { axiosInstance } from "../api/axios";
import NpcCalloutCard from "./NpcCalloutCard";

export default function MapWithZoom() {
  const mapRef = useRef(null);

  const region = {
    latitude: 48.1486,
    longitude: 17.1077,
    latitudeDelta: 5,
    longitudeDelta: 5,
  };

  const [npcs, setNpcs] = useState([]);
  const [selectedNpc, setSelectedNpc] = useState(null);
  const [loadingNpc, setLoadingNpc] = useState(false);
  const requestId = useRef(0);

  useEffect(() => {
    const id = ++requestId.current;

    const min_lat = region.latitude - region.latitudeDelta / 2;
    const max_lat = region.latitude + region.latitudeDelta / 2;
    const min_lng = region.longitude - region.longitudeDelta / 2;
    const max_lng = region.longitude + region.longitudeDelta / 2;

    axiosInstance
      .get("/npc/", {
        params: { min_lat, max_lat, min_lng, max_lng },
      })
      .then((res) => {
        if (id !== requestId.current) return;
        setNpcs(res.data);
      })
      .catch(console.error);
  }, []);

  const handleMarkerPress = async (item) => {
    try {
      setLoadingNpc(true);

      const res = await axiosInstance.get(`/npc/${item.id}/`);
      setSelectedNpc(res.data);
    } catch (error) {
      console.error("Failed to fetch NPC details:", error);
    } finally {
      setLoadingNpc(false);
    }
  };

  return (
    <View style={styles.container}>
      <MapView ref={mapRef} style={styles.map} initialRegion={region}>
        {npcs.map((item) => {
          if (
            item?.latitude == null ||
            item?.longitude == null ||
            isNaN(Number(item.latitude)) ||
            isNaN(Number(item.longitude))
          ) {
            return null;
          }

          return (
            <Marker
              key={String(item.id)}
              coordinate={{
                latitude: Number(item.latitude),
                longitude: Number(item.longitude),
              }}
              onPress={() => handleMarkerPress(item)}
            >
              <View style={styles.dot}>
                <Text style={styles.emoji}>🧍</Text>
              </View>
            </Marker>
          );
        })}
      </MapView>

      <NpcCalloutCard
        npc={selectedNpc}
        loading={loadingNpc}
        onClose={() => setSelectedNpc(null)}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
  dot: {
    alignItems: "center",
    justifyContent: "center",
  },
  emoji: {
    fontSize: 22,
  },
});
