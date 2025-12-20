import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { apiGet } from "../api/http";

export default function GuildDashboard() {
  const { guildId } = useParams();
  const [stats, setStats] = useState(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    (async () => {
      try {
        const s = await apiGet(`/api/guilds/${guildId}/stats`)
        setStats(s);
      } catch (e) {
        setErr("取得できなかった（ログイン切れかも）");
      }
    })();
  }, [guildId]);

  if (err) return <div style={{ padding: 24 }}>{err}</div>;
  if (!stats) return <div style={{ padding: 24 }}>Loading...</div>;

  return (
    <div style={{ padding: 24 }}>
      <Link to="/dashboard">← Back</Link>
      <h2 style={{ marginTop: 10 }}>Guild Stats</h2>
      <div style={{ opacity: 0.7, marginBottom: 12 }}>guild_id: {guildId}</div>

      <ul>
        <li>avg_all: {stats.avg_all}</li>
        <li>avg_today: {stats.avg_today}</li>
      </ul>
    </div>
  );
}
