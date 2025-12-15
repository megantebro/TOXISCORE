import Header from "../components/Header"
import HeroSection from "../sections/HeroSection"
import DocsSection from "../sections/DocsSection"

export default function Home() {
    return (
        <>
        <Header />
        <main>
        <HeroSection />
        <DocsSection />
        </main>
        </>
    );
}