import { BrowserRouter, Routes, Route, Navigate} from "react-router-dom";
import Home from "./pages/Home";
import Dashboard from "./pages/Dashboard";
import GuildDashboard from "./pages/GuildDashboard";
import "./App.css";
import CommandsPage from "./pages/CommandsPage"

function App() {
	return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/dashboard/:guildId" element={<GuildDashboard />} />
        <Route path="*" element={<Navigate to="/" replace />} />
        <Route path="/commands" element={<CommandsPage />} />
      </Routes>
    </BrowserRouter>
  );
}


export default App;
