import { Text, View, StyleSheet } from "react-native";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";

export default function Map() {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>
        Map exploration is available in the mobile app
      </Text>

      <View style={styles.storesRow}>
        <View style={styles.storeCard}>
          <MaterialIcons name="android" style={styles.androidIcon} />
          <Text style={styles.androidText}>Android Store</Text>
        </View>

        <View style={styles.storeCard}>
          <MaterialIcons name="apple" style={styles.appleIcon} />
          <Text style={styles.appleText}>App Store</Text>
        </View>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: "black",
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 24,
  },
  title: {
    color: "white",
    textAlign: "center",
    fontSize: 40,
    fontFamily: "AcademyEngravedLetPlain",
    marginBottom: 80,
    maxWidth: 900,
  },
  storesRow: {
    flexDirection: "row",
    gap: 80,
    alignItems: "center",
    justifyContent: "center",
    flexWrap: "wrap",
  },
  storeCard: {
    alignItems: "center",
    justifyContent: "center",
  },
  androidIcon: {
    fontSize: 56,
    color: "green",
    marginBottom: 12,
  },
  appleIcon: {
    fontSize: 56,
    color: "white",
    marginBottom: 12,
  },
  androidText: {
    color: "green",
    fontSize: 24,
    fontFamily: "AcademyEngravedLetPlain",
    textAlign: "center",
  },
  appleText: {
    color: "white",
    fontSize: 24,
    fontFamily: "AcademyEngravedLetPlain",
    textAlign: "center",
  },
});
