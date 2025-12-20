
import { useState } from "react";
export default function CommandsPage() {
  const commands = [
  {
    name: "/avg_toxiscore",
    description: "ユーザーの平均暴言スコアを取得します",
    usage: "/avg_toxiscore [user]",
    notes: [
      "user を指定しない場合は自分のスコアを表示します。",
      "ユーザーがまだ発言していない場合はメッセージが表示されます。",
    ],
  },
  {
    name: "/toxicity_rank",
    description: "サーバー平均と比較した治安影響スコアを表示します",
    usage: "/toxicity_rank [user]",
    notes: [
      "user を指定しない場合は自分のスコアを表示します。",
      "平均暴言スコア・サーバー平均・影響度（平均との差）・Z値を表示します。",
      "Z値によって評価メッセージが変わります（普通/口が悪い/治安を良くする/治安悪化など）。",
    ],
  },
  {
    name: "/add_exclude_channel",
    description: "AIが暴言を検知しなくなるチャンネルを設定します",
    usage: "/add_exclude_channel <channel>",
    notes: [
      "指定したチャンネルIDを config.json の exclude_channel_ids に追加します。",
      "除外したチャンネルでは暴言検知が行われません。",
    ],
  },
  {
    name: "/remove_exclude_channel",
    description: "チャンネルを除外リストから削除します",
    usage: "/remove_exclude_channel <channel>",
    notes: [
      "指定したチャンネルIDを config.json の exclude_channel_ids から削除します。",
      "除外リストに存在しない場合はその旨を表示します。",
    ],
  },
  {
    name: "/ranking",
    description: "サーバーの治安にどのくらい影響を与えているかのランキングを表示します",
    usage: "/ranking [worst] [limit] [min_post] [type]",
    options: [
      { name: "worst", description: "true で「治安悪化寄り（平均暴言度が高い）」ランキング", required: false },
      { name: "limit", description: "表示件数（デフォルト: 5）", required: false },
      { name: "min_post", description: "ランキング対象に必要な最低発言数（デフォルト: 10）", required: false },
      { name: "type", description: "avg（平均） / total（合計） ※totalは未実装っぽい", required: false },
    ],
    notes: [
      "デフォルトでは『サーバーの優良ユーザーランキング』を表示します。",
      "worst=true で『サーバー平均暴言度ランキング』になります。",
      "ephemeral=true なので実行者にのみ表示されます。",
    ],
  },
];


  
const [selected, setSelected] = useState(null);

  // ======================
  // 詳細画面
  // ======================
  if (selected) {
    return (
      <section className="docs">
        <div className="container">
          <button
            className="backButton"
            onClick={() => setSelected(null)}
          >
            ← Back
          </button>

          <div className="card">
            <h3>{selected.name}</h3>
            <p>{selected.description}</p>

            <pre className="commandUsage">
              {selected.usage}
            </pre>

            {selected.notes?.length && (
              <div className="commandNotes">
                <h4>Details</h4>
                <ul>
                  {selected.notes.map((note, i) => (
                    <li key={i}>{note}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      </section>
    );
  }

  // ======================
  // 一覧画面
  // ======================
  return (
    <section className="docs">
      <div className="container">
        <h2 className="sectionTitle">Commands</h2>
        <p className="sectionSub">
          Click a command to see details
        </p>

        <div className="cards">
          {commands.map((cmd) => (
            <div
              key={cmd.name}
              className="card clickable"
              onClick={() => setSelected(cmd)}
            >
              <h3>{cmd.name}</h3>
              <p>{cmd.description}</p>
              <span className="cardLink">View details →</span>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}