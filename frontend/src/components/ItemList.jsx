// src/components/ItemList.jsx
import { useEffect, useState } from "react";
import { fetchItems, deleteItem } from "../api/itemApi";

function ItemList({ onEdit, refreshKey }) {
    const [items, setItems] = useState([]);
    const [error, setError] = useState(null); // 에러 상태 추가
    const [loading, setLoading] = useState(false);

    // refreshKey가 바뀔 때마다 목록 새로고침
    useEffect(() => {
        loadItems();
        }, 
        [refreshKey]
    );
    
    const loadItems = async () => {
        setLoading(true);
        setError(null);
        try {
            const data = await fetchItems();
            setItems(data);
        } catch (e) {
            setError("서버에 연결할 수 없습니다. FastAPI 서버가 실행 중인지 확인하세요.");
        } finally {
            setLoading(false);
        }
    };

    const handleDelete = async (id) => {
        if (!window.confirm("삭제하시겠습니까?")) return;
        
        try {
        await deleteItem(id);
            loadItems(); // 삭제 후 목록 새로고침
        } catch (e) {
            alert("삭제에 실패했습니다.");
        }
    };

    if (loading) return <p>불러오는 중...</p>;
    
    if (error) return <p style={{ color: "red" }}>{error}</p>;

    return (
        <div>
            <h2>아이템 목록</h2>
            {items.length === 0 && <p>등록된 아이템이 없습니다.</p>}
            
            <ul style={{ listStyle: "none", padding: 0 }}>
                {items.map(item => (
                    <li key={item.id} style={{ padding: "8px", borderBottom: "1px solid #eee" }}>
                        <strong>{item.name}</strong> — {item.price.toLocaleString()}원
                        <button onClick={() => onEdit(item)}
                        style={{ marginLeft: 12, padding: "4px 10px" }}>수정</button>
                        <button onClick={() => handleDelete(item.id)}
                        style={{ marginLeft: 4, padding: "4px 10px", color: "red" }}>삭제</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ItemList;