import MapView from "react-native-map-clustering";
import { Marker } from "react-native-maps";
import { View, StyleSheet } from "react-native";
import { useState, useRef, useCallback, useEffect } from "react";
import { axiosInstance } from "../api/axios";
import NpcCalloutCard from "./NpcCalloutCard";

const INITIAL_REGION = {
  latitude: 49.2992,
  longitude: 19.9496,
  latitudeDelta: 0.1,
  longitudeDelta: 0.1,
};

export default function MapWithZoom() {
  const mapRef = useRef(null);
  const requestId = useRef(0);
  const timeoutRef = useRef(null);

  const [npcs, setNpcs] = useState([]);
  const [selectedNpc, setSelectedNpc] = useState(null);
  const [loadingNpc, setLoadingNpc] = useState(false);

  const fetchMapData = useCallback(async (region) => {
    const id = ++requestId.current;

    const min_lat = region.latitude - region.latitudeDelta / 2;
    const max_lat = region.latitude + region.latitudeDelta / 2;
    const min_lng = region.longitude - region.longitudeDelta / 2;
    const max_lng = region.longitude + region.longitudeDelta / 2;

    try {
      const res = await axiosInstance.get("/npc/", {
        params: {
          min_lat,
          max_lat,
          min_lng,
          max_lng,
        },
      });

      if (id !== requestId.current) return;

      const data = Array.isArray(res.data)
        ? res.data
        : Array.isArray(res.data?.results)
          ? res.data.results
          : [];

      setNpcs(data);
    } catch (error) {
      console.error("Failed to fetch NPCs:", error);
    }
  }, []);

  const handleRegionChangeComplete = useCallback(
    (region) => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        fetchMapData(region);
      }, 250);
    },
    [fetchMapData],
  );

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

  useEffect(() => {
    fetchMapData(INITIAL_REGION);

    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }
    };
  }, [fetchMapData]);

  return (
    <View style={styles.container}>
      <MapView
        ref={mapRef}
        style={styles.map}
        initialRegion={INITIAL_REGION}
        onRegionChangeComplete={handleRegionChangeComplete}
        animationEnabled={false}
        preserveClusterPressBehavior={false}
        clusterColor="#2f6fed"
        clusterTextColor="#ffffff"
        minDelta={0.01}
        maxDelta={0.1}
      >
        {npcs.map((item) => {
          const lat = Number(item?.latitude);
          const lng = Number(item?.longitude);

          if (!Number.isFinite(lat) || !Number.isFinite(lng)) {
            return null;
          }

          return (
            <Marker
              key={String(item.id)}
              coordinate={{ latitude: lat, longitude: lng }}
              title={`NPC #${item.id}`}
              description={"Npc"}
              onPress={() => handleMarkerPress(item)}
              tracksViewChanges={false}
            />
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
});
