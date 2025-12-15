export default function HeroSection() {
    const scrollToDocs = () =>{
        const el = document.getElementById("docs");
        if(el) el.scrollIntoView({behavior: "smooth"})
    }

     // TODO: あとで本物のURLに差し替え
  const inviteBot = () => {
    // 例：permissions は後で調整、client_id は BotのID
    const url =
      "https://discord.com/oauth2/authorize?client_id=YOUR_BOT_ID&scope=bot%20applications.commands&permissions=8";
    window.open(url, "_blank", "noopener,noreferrer");
  };

  const login = () => {
    // FastAPI 側で /auth/discord/login を作ってそこに飛ばす想定
    window.location.href = "http://localhost:8000/auth/discord/login";
  };

  return (
    <section className="hero">
      <div className="heroBg" aria-hidden="true" />

      <div className="heroInner">
        <div className="pill">Discord Bot Dashboard</div>

        <h1 className="heroTitle">
          Manage your bot with a <span className="accent">clean dashboard</span>.
        </h1>

        <p className="heroSub">
          Invite the bot, login with Discord, and configure everything from one
          place.
        </p>

        <div className="heroButtons">
          <button className="btn btnPrimary" onClick={inviteBot}>
            Invite Bot
          </button>
          <button className="btn btnGhost" onClick={login}>
            Login
          </button>
        </div>

        <button className="scrollHint" onClick={scrollToDocs}>
          ↓ Scroll or click Docs
        </button>
      </div>
    </section>
  );

}