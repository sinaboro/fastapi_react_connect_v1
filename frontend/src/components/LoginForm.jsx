import { useState } from "react";
import { login } from "../api/authApi";

function LoginForm({ onLoginSuccess, onSwitchToRegister }) {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [submitting, setSubmitting] = useState(false);
    
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            const data = await login(email, password);
            localStorage.setItem("token", data.access_token);
            onLoginSuccess();
        } catch (e) {
            setError("이메일 또는 비밀번호가 올바르지 않습니다.");
        } finally {
            setSubmitting(false);
        }
    };

    return (
        <div style={{ maxWidth: 360, margin: "80px auto", padding: 24, border: "1px solid #eee", borderRadius: 8 }}>
            <h2 style={{ color: "#1E3A5F" }}>로그인</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 12 }}>
                    <input value={email} onChange={e => setEmail(e.target.value)}
                    placeholder="이메일" type="email" required
                    style={{ width: "100%", padding: "8px 10px", boxSizing: "border-box" }} />
                </div>

                <div style={{ marginBottom: 12 }}>
                    <input value={password} onChange={e => setPassword(e.target.value)}
                    placeholder="비밀번호" type="password" required
                    style={{ width: "100%", padding: "8px 10px", boxSizing: "border-box" }} />
                </div>
                {error && <p style={{ color: "red", fontSize: 14 }}>{error}</p>}
                <button type="submit" disabled={submitting}
                    style={{ width: "100%", padding: "10px", background: "#2E75B6", color: "#fff", border: "none", borderRadius: 4 }}>
                    {submitting ? "로그인 중..." : "로그인"}
                </button>
            </form>
            <p style={{ textAlign: "center", marginTop: 12, fontSize: 14 }}>
                계정이 없으신가요?{" "}
                <button type="button" onClick={onSwitchToRegister}
                    style={{ border: "none", background: "none", color: "#2E75B6", cursor:"pointer" }}>
                    회원가입
                </button>
            </p>
        </div>
    );
}
export default LoginForm;