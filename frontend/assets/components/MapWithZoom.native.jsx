import MapViewClustering from "react-native-map-clustering";
import { View, StyleSheet, Text } from "react-native";
import { useState, useRef, useEffect } from "react";
import { Marker } from "react-native-maps";
import ZoomButton from "@/assets/components/zoombutton";
import { axiosInstance } from "../api/axios";

export default function MapWithZoom() {
  const mapRef = useRef(null);

  const [region, setRegion] = useState({
    latitude: 48.1486,
    longitude: 17.1077,
    latitudeDelta: 5,
    longitudeDelta: 5,
  });

  const [npcs, setNpcs] = useState([]);
  const lastRegionRef = useRef(null);

  // ----------------------------
  // ZOOM CONTROLS
  // ----------------------------
  const zoomIn = () => {
    const newRegion = {
      ...region,
      latitudeDelta: Math.max(region.latitudeDelta / 2, 0.01),
      longitudeDelta: Math.max(region.longitudeDelta / 2, 0.01),
    };

    setRegion(newRegion);
    mapRef.current?.animateToRegion(newRegion, 300);
  };

  const zoomOut = () => {
    const newRegion = {
      ...region,
      latitudeDelta: Math.min(region.latitudeDelta * 2, 100),
      longitudeDelta: Math.min(region.longitudeDelta * 2, 100),
    };

    setRegion(newRegion);
    mapRef.current?.animateToRegion(newRegion, 300);
  };

  // ----------------------------
  // FETCH NPCs
  // ----------------------------
  useEffect(() => {
    if (!region) return;

    // skip extreme zoom out
    if (region.latitudeDelta > 40) {
      setNpcs([]);
      return;
    }

    // prevent tiny movements from spamming API
    if (lastRegionRef.current) {
      const dr = Math.abs(lastRegionRef.current.latitude - region.latitude);
      const dl = Math.abs(lastRegionRef.current.longitude - region.longitude);

      if (dr < 0.01 && dl < 0.01) return;
    }

    lastRegionRef.current = region;

    const timeout = setTimeout(() => {
      const min_lat = region.latitude - region.latitudeDelta / 2;
      const max_lat = region.latitude + region.latitudeDelta / 2;
      const min_lng = region.longitude - region.longitudeDelta / 2;
      const max_lng = region.longitude + region.longitudeDelta / 2;

      axiosInstance
        .get("/npc/", {
          params: { min_lat, max_lat, min_lng, max_lng },
        })
        .then((res) => {
          setNpcs(res.data);
        })
        .catch(console.error);
    }, 100);

    return () => clearTimeout(timeout);
  }, [region]);

  // ----------------------------
  // RENDER
  // ----------------------------
  return (
    <View style={styles.container}>
      <MapViewClustering
        ref={mapRef}
        style={styles.map}
        initialRegion={region}
        onRegionChangeComplete={(newRegion) => setRegion(newRegion)}
      >
        {npcs.map((npc) => (
          <Marker
            key={npc.id}
            coordinate={{
              latitude: npc.latitude,
              longitude: npc.longitude,
            }}
            title={`${npc.first_name} ${npc.last_name}`}
          >
            <View
              style={{
                padding: 6,
                backgroundColor: "#4F46E5",
                borderRadius: 20,
                borderWidth: 2,
                borderColor: "white",
              }}
            >
              <Text style={{ color: "white" }}>🧍</Text>
            </View>
          </Marker>
        ))}
      </MapViewClustering>

      <View style={styles.controls}>
        <ZoomButton title="+" onPress={zoomIn} />
        <ZoomButton title="-" onPress={zoomOut} />
      </View>
    </View>
  );
}

// ----------------------------
// STYLES
// ----------------------------
const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
  controls: {
    position: "absolute",
    bottom: 50,
    right: 20,
  },
});
