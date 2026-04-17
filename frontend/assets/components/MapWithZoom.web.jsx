import React, { useEffect, useRef, useState } from "react";
import { axiosInstance } from "../api/axios";

export default function NpcTestList() {
  const [npcs, setNpcs] = useState([]);
  const requestId = useRef(0);

  const region = {
    latitude: 49.2992,
    longitude: 19.9496,
    latitudeDelta: 2,
    longitudeDelta: 2,
  };

  useEffect(() => {
    const id = ++requestId.current;

    const min_lat = region.latitude - region.latitudeDelta / 2;
    const max_lat = region.latitude + region.latitudeDelta / 2;
    const min_lng = region.longitude - region.longitudeDelta / 2;
    const max_lng = region.longitude + region.longitudeDelta / 2;
    console.log("log in consolse");
    axiosInstance
      .get("/npc/", {
        params: { min_lat, max_lat, min_lng, max_lng },
      })
      .then((res) => {
        if (id !== requestId.current) return;

        const data = Array.isArray(res.data)
          ? res.data
          : res.data?.results || [];

        setNpcs(data);
      })
      .catch((err) => {
        console.error("NPC fetch failed:", err);
      });
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h2>NPC List Test</h2>

      {npcs.length === 0 && <p>No NPCs loaded</p>}

      {npcs.map((npc) => (
        <div
          key={npc.id}
          style={{
            padding: 10,
            marginBottom: 10,
            border: "1px solid #ddd",
            borderRadius: 6,
          }}
        >
          <strong style={{ color: "white" }}>
            {npc.first_name} {npc.last_name}
          </strong>
          <div>{npc.occupation}</div>
        </div>
      ))}
    </div>
  );
}
