import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiGet } from "../api/http";

export default function Dashboard() {
  const [guilds, setGuilds] = useState([]);
  const [me, setMe] = useState(null);
  const [err, setErr] = useState("");
  const nav = useNavigate();

  useEffect(() => {
    (async () => {
      try {
        const user = await apiGet("/api/me");
        setMe(user);
        const gs = await apiGet("/api/guilds");
        setGuilds(gs);
      } catch (e) {
        setErr("ログインしてないっぽい。HomeからLoginしてね。");
      }
    })();
  }, []);

  if (err) return <div style={{ padding: 24 }}>{err}</div>;

  return (
    <div style={{ padding: 24 }}>
      <h2>Dashboard</h2>
      {me && <div style={{ opacity: 0.8, marginBottom: 12 }}>Hello, {me.username}</div>}

      <div style={{ display: "grid", gap: 12, gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))" }}>
        {guilds.map((g) => (
          <button
            key={g.id}
            onClick={() => nav(`/dashboard/${g.id}`)}
            style={{
              textAlign: "left",
              padding: 14,
              borderRadius: 12,
              border: "1px solid rgba(255,255,255,.12)",
              background: "rgba(255,255,255,.05)",
              color: "white",
              cursor: "pointer",
            }}
          >
            <div style={{ fontWeight: 700 }}>{g.name}</div>
            <div style={{ opacity: 0.7, fontSize: 12 }}>guild_id: {g.id}</div>
          </button>
        ))}
      </div>
    </div>
  );
}
