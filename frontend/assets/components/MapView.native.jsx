import MapView, { Marker, PROVIDER_GOOGLE } from "react-native-maps";
import { View, StyleSheet, Platform, Text } from "react-native";
import { useState, useRef, useCallback, useEffect, useMemo } from "react";
import Supercluster from "supercluster";
import { axiosInstance } from "../api/axios";
import NpcCalloutCard from "./NpcCalloutCard";

const INITIAL_REGION = {
  latitude: 64.1466,
  longitude: -21.9426,
  latitudeDelta: Platform.OS === "android" ? 1 : 0.01,
  longitudeDelta: Platform.OS === "android" ? 1 : 0.01,
};

const getZoom = (longitudeDelta) => {
  return Math.round(Math.log(360 / longitudeDelta) / Math.LN2);
};

export default function Map() {
  const mapRef = useRef(null);
  const requestId = useRef(0);
  const timeoutRef = useRef(null);

  const [region, setRegion] = useState(INITIAL_REGION);
  const [npcs, setNpcs] = useState([]);
  const [selectedNpc, setSelectedNpc] = useState(null);
  const [loadingNpc, setLoadingNpc] = useState(false);

  const fetchMapData = useCallback(async (mapRegion) => {
    const id = ++requestId.current;

    const min_lat = mapRegion.latitude - mapRegion.latitudeDelta / 2;
    const max_lat = mapRegion.latitude + mapRegion.latitudeDelta / 2;
    const min_lng = mapRegion.longitude - mapRegion.longitudeDelta / 2;
    const max_lng = mapRegion.longitude + mapRegion.longitudeDelta / 2;

    try {
      const res = await axiosInstance.get("/npc/", {
        params: { min_lat, max_lat, min_lng, max_lng },
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

  const points = useMemo(() => {
    return npcs
      .filter((npc) => {
        const lat = Number(npc.latitude);
        const lng = Number(npc.longitude);
        return Number.isFinite(lat) && Number.isFinite(lng);
      })
      .map((npc) => ({
        type: "Feature",
        properties: {
          cluster: false,
          npc,
          npcId: npc.id,
        },
        geometry: {
          type: "Point",
          coordinates: [Number(npc.longitude), Number(npc.latitude)],
        },
      }));
  }, [npcs]);

  const clusterIndex = useMemo(() => {
    const index = new Supercluster({
      radius: 80,
      maxZoom: 20,
    });

    index.load(points);
    return index;
  }, [points]);

  const clusters = useMemo(() => {
    const zoom = getZoom(region.longitudeDelta);

    return clusterIndex.getClusters(
      [
        region.longitude - region.longitudeDelta,
        region.latitude - region.latitudeDelta,
        region.longitude + region.longitudeDelta,
        region.latitude + region.latitudeDelta,
      ],
      zoom,
    );
  }, [clusterIndex, region]);

  const handleRegionChangeComplete = useCallback(
    (nextRegion) => {
      setRegion(nextRegion);

      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current);
      }

      timeoutRef.current = setTimeout(() => {
        fetchMapData(nextRegion);
      }, 600);
    },
    [fetchMapData],
  );

  const handleMarkerPress = useCallback(async (item) => {
    try {
      setLoadingNpc(true);
      const res = await axiosInstance.get(`/npc/${item.id}/`);
      setSelectedNpc(res.data);
    } catch (error) {
      console.error("Failed to fetch NPC details:", error);
    } finally {
      setLoadingNpc(false);
    }
  }, []);

  const handleClusterPress = useCallback(
    (cluster) => {
      const [longitude, latitude] = cluster.geometry.coordinates;
      const expansionZoom = Math.min(
        clusterIndex.getClusterExpansionZoom(cluster.properties.cluster_id),
        20,
      );

      const longitudeDelta = 360 / Math.pow(2, expansionZoom);
      const latitudeDelta = longitudeDelta;

      mapRef.current?.animateToRegion(
        {
          latitude,
          longitude,
          latitudeDelta,
          longitudeDelta,
        },
        350,
      );
    },
    [clusterIndex],
  );

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
        provider={Platform.OS === "android" ? PROVIDER_GOOGLE : undefined}
        initialRegion={INITIAL_REGION}
        onRegionChangeComplete={handleRegionChangeComplete}
      >
        {clusters.map((cluster) => {
          const [longitude, latitude] = cluster.geometry.coordinates;
          const isCluster = cluster.properties.cluster;

          if (isCluster) {
            return (
              <Marker
                key={`cluster-${cluster.properties.cluster_id}`}
                coordinate={{ latitude, longitude }}
                onPress={() => handleClusterPress(cluster)}
              >
                <View style={styles.clusterMarker}>
                  <Text style={styles.clusterText}>
                    {cluster.properties.point_count}
                  </Text>
                </View>
              </Marker>
            );
          }

          const npc = cluster.properties.npc;

          return (
            <Marker
              key={`npc-${npc.id}`}
              coordinate={{
                latitude,
                longitude,
              }}
              title={`NPC #${npc.id}`}
              description="Npc"
              onPress={() => handleMarkerPress(npc)}
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
  container: {
    flex: 1,
  },
  map: {
    flex: 1,
  },
  clusterMarker: {
    width: 42,
    height: 42,
    borderRadius: 21,
    backgroundColor: "#2f6fed",
    alignItems: "center",
    justifyContent: "center",
    borderWidth: 2,
    borderColor: "white",
  },
  clusterText: {
    color: "white",
    fontWeight: "bold",
  },
});
