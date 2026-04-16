import MapView from "react-native-map-clustering";
import { View, StyleSheet } from "react-native";
import { useState, useRef } from "react";
import ZoomButton from "@/assets/components/zoombutton";
import NPCMarker from "./NPCMarker";

export default function MapWithZoom() {
  const mapRef = useRef(null);

  const [region, setRegion] = useState({
    latitude: 48.1486,
    longitude: 17.1077,
    latitudeDelta: 5,
    longitudeDelta: 5,
  });

  const zoomIn = () => {
    const newRegion = {
      ...region,
      latitudeDelta: region.latitudeDelta / 2,
      longitudeDelta: region.longitudeDelta / 2,
    };

    setRegion(newRegion);
  };

  const zoomOut = () => {
    const newRegion = {
      ...region,
      latitudeDelta: region.latitudeDelta * 2,
      longitudeDelta: region.longitudeDelta * 2,
    };

    setRegion(newRegion);
  };

  return (
    <View style={styles.container}>
      <MapView
        ref={mapRef}
        style={styles.map}
        region={region}
        onRegionChangeComplete={(newRegion) => {
          setRegion(newRegion);
        }}
      >
        <NPCMarker region={region} />
      </MapView>
      <View style={styles.controls}>
        <ZoomButton title="+" onPress={zoomIn} />
        <ZoomButton title="-" onPress={zoomOut} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  map: { flex: 1 },
  controls: {
    position: "absolute",
    bottom: 50,
    right: 20,
  },
});
