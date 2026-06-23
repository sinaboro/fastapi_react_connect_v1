import axios from "axios";
const BASE_URL = "http://localhost:8000";

export const register = async (userData) => {
    const response = await axios.post(BASE_URL + "/auth/register", userData);
    return response.data;
};

export const login = async (email, password) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);
    
    const response = await axios.post(BASE_URL + "/auth/login", params, {
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });

    return response.data;
};

export const fetchMyInfo = async () => {
    const token = localStorage.getItem("token");
    const response = await axios.get(BASE_URL + "/auth/me", {
    headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
};
