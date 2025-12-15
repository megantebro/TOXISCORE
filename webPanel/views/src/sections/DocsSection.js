export default function DocsSection() {
  return (
    <section id="docs" className="docs">
      <div className="container">
        <h2 className="sectionTitle">Docs</h2>
        <p className="sectionSub">
          Quick start guide. (あとで日本語にしてもOK)
        </p>

        <div className="cards">
          <div className="card">
            <h3>1) Invite</h3>
            <p>First, invite the bot to your server.</p>
          </div>

          <div className="card">
            <h3>2) Login</h3>
            <p>Login with Discord to open the dashboard.</p>
          </div>

          <div className="card">
            <h3>3) Configure</h3>
            <p>Pick a server and change settings.</p>
          </div>
        </div>

        <div className="note">
          <h4>Next step</h4>
          <p>
            次は FastAPI 側に <code>/auth/discord/login</code> を作って、
            Discord OAuth に繋げると “管理画面っぽさ” が一気に出る。
          </p>
        </div>
      </div>
    </section>
  );
}
