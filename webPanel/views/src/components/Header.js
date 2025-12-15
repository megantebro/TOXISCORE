export default function Header(){
    const scrollToDocs = () => {
        const el = document.getElementById("docs")
        if(el) el.scrollIntoView({behavior: "smooth"})
    };

    return (
    <header className="header">
      <div className="brand">
        <div className="brandDot" />
        <span className="brandName">ToxiScore</span>
      </div>

      <nav className="nav">
        <button className="navLink" onClick={scrollToDocs}>
          Docs
        </button>
      </nav>
    </header>
  );
}