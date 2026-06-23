import { useState } from "react";
import { register } from "../api/authApi";

function RegisterForm({ onRegisterSuccess, onSwitchToLogin }) {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(null);
    const [submitting, setSubmitting] = useState(false);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setSubmitting(true);
        try {
            await register({ username, email, password });
            alert("회원가입이 완료되었습니다. 로그인해주세요.");
            onSwitchToLogin();
        } catch (e) {
            const detail = e.response?.data?.detail;
            setError(detail || "회원가입에 실패했습니다. 입력값을 확인하세요.");
        } finally {
            setSubmitting(false);
        }
    };
    return (
        <div style={{ maxWidth: 360, margin: "80px auto", padding: 24, border: "1px solid #eee", borderRadius: 8 }}>
            <h2 style={{ color: "#1E3A5F" }}>회원가입</h2>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: 12 }}>
                    <input value={username} onChange={e => setUsername(e.target.value)}
                    placeholder="아이디 (영문/숫자, 3~20자)" required
                    style={{ width: "100%", padding: "8px 10px", boxSizing: "border-box" }} />
                </div>
                <div style={{ marginBottom: 12 }}>
                    <input value={email} onChange={e => setEmail(e.target.value)}
                    placeholder="이메일" type="email" required
                    style={{ width: "100%", padding: "8px 10px", boxSizing: "border-box" }} />
                </div>
                <div style={{ marginBottom: 12 }}>
                    <input value={password} onChange={e => setPassword(e.target.value)}
                    placeholder="비밀번호 (8자 이상)" type="password" required
                    style={{ width: "100%", padding: "8px 10px", boxSizing: "border-box" }} />
                </div>
                {error && <p style={{ color: "red", fontSize: 14 }}>{error}</p>}
                <button type="submit" disabled={submitting}
                    style={{ width: "100%", padding: "10px", background: "#2E75B6", color: "#fff",
                    border: "none", borderRadius: 4 }}>
                    {submitting ? "처리 중..." : "가입하기"}
                </button>
            </form>
            <p style={{ textAlign: "center", marginTop: 12, fontSize: 14 }}>
            이미 계정이 있으신가요?{" "}
                <button type="button" onClick={onSwitchToLogin}
                    style={{ border: "none", background: "none", color: "#2E75B6", cursor:
                    "pointer" }}>
                    로그인
                </button>
            </p>
        </div>
    );
}

export default RegisterForm;