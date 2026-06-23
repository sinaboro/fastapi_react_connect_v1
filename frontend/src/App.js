import { useState, useEffect } from "react";
import ItemList from "./components/ItemList";
import ItemForm from "./components/ItemForm";
import LoginForm from "./components/LoginForm";
import RegisterForm from "./components/RegisterForm";
import { fetchMyInfo } from "./api/authApi";

function App() {
  const [user, setUser] = useState(null);
  const [authView, setAuthView] = useState("login");
  const [checking, setChecking] = useState(true);
  const [editItem, setEditItem] = useState(null);
  const [refreshKey, setRefreshKey] = useState(0);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) { setChecking(false); return; }
    fetchMyInfo()
    .then(data => setUser(data))
    .catch(() => localStorage.removeItem("token"))
    .finally(() => setChecking(false));
  }, []);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  const handleItemSuccess = () => {
    setEditItem(null);
    setRefreshKey(k => k + 1);
  };

  if (checking) return <p style={{ textAlign: "center", marginTop: 80 }}>로딩 중...</p>;
  
  if (!user) {
    return authView === "login" ? (
        <LoginForm
        onLoginSuccess={() => fetchMyInfo().then(setUser)}
        onSwitchToRegister={() => setAuthView("register")}
        />
      ) : 
      (
        <RegisterForm
        onRegisterSuccess={() => setAuthView("login")}
        onSwitchToLogin={() => setAuthView("login")}
        />
      );
  }
  return (
    <div style={{ maxWidth: 700, margin: "40px auto", padding: "0 20px", fontFamily:"sans-serif" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems:"center" }}>
        <h1 style={{ color: "#1E3A5F" }}>FastAPI + React 아이템 관리</h1>
        <div>
          <span style={{ marginRight: 12, color: "#555" }}>{user.username}님</span>
          <button onClick={handleLogout} style={{ padding: "6px 12px" }}>로그아웃</button>
        </div>
      </div>
      <ItemForm editItem={editItem} onSuccess={handleItemSuccess} />
      <ItemList refreshKey={refreshKey} onEdit={setEditItem} />
    </div>
  );
}
export default App;


