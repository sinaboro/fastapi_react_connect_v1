// src/api/itemApi.js
import axios from "axios";

const BASE_URL = "http://localhost:8000";


axios.interceptors.request.use((config) => {
    const token = localStorage.getItem("token");
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});




// 아이템 목록 조회 (GET /items)
export const fetchItems = async () => {
    const response = await axios.get(BASE_URL + "/items");
    console.log("-----------------")
    console.log(response)
    console.log("-----------------")
    return response.data;
};

// 아이템 생성 (POST /items)
export const createItem = async (itemData) => {
    const response = await axios.post(BASE_URL + "/items", itemData);
    return response.data;
};

// 아이템 수정 (PUT /items/{id})
export const updateItem = async (id, itemData) => {
    const response = await axios.put(BASE_URL + "/items/" + id, itemData);
    return response.data;
};

// 아이템 삭제 (DELETE /items/{id})
export const deleteItem = async (id) => {
    await axios.delete(BASE_URL + "/items/" + id);
}
