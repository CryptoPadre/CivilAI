import { View, Text, StyleSheet } from "react-native";

export default function MapWithZoom() {
  return (
    <View style={styles.container}>
      <Text>Map is not available on web. Please use mobile.</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
});
