// src/components/ItemForm.jsx
import { useState, useEffect } from "react";
import { createItem, updateItem } from "../api/itemApi";

// editItem prop이 있으면 수정 모드, 없으면 등록 모드
function ItemForm({ editItem, onSuccess }) {
    const [name, setName] = useState("");
    const [price, setPrice] = useState("");
    const [submitting, setSubmitting] = useState(false);

    // editItem이 바뀔 때마다 폼 초기값 설정
    useEffect(() => {
        if (editItem) {
            setName(editItem.name);
            setPrice(String(editItem.price));
        } else {
            setName("");
            setPrice("");
        }
    }, [editItem]);

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (!name.trim() || !price) return;
        setSubmitting(true);
        
        try {
            const payload = { name: name.trim(), price: Number(price) };
            if (editItem) {
                await updateItem(editItem.id, payload); // PUT /items/{id}
            } else {
                await createItem(payload); // POST /items
            }
            onSuccess(); // 부모에게 완료 알림 → 목록 새로고침
        } catch (e) {
            alert("저장에 실패했습니다. 입력값을 확인하세요.");
        } finally {
            setSubmitting(false);
        }
    };

    return (
    <div style={{ marginBottom: 24, padding: 16, background: "#f9f9f9", borderRadius:8 }}>
        <h2>{editItem ? "아이템 수정" : "아이템 등록"}</h2>
        <form onSubmit={handleSubmit}>
            <input value={name} onChange={e => setName(e.target.value)}
                placeholder="이름" required
                style={{ marginRight: 8, padding: "6px 10px" }} />
            <input value={price} onChange={e => setPrice(e.target.value)}
                placeholder="가격" type="number" min="1" required
                style={{ marginRight: 8, padding: "6px 10px" }} />
            <button type="submit" disabled={submitting}
                style={{ padding: "6px 16px", background: "#2E75B6", color: "#fff", border:
                "none", borderRadius: 4 }}>
                {submitting ? "저장 중..." : editItem ? "수정 완료" : "등록"}
            </button>
            {   editItem && 
                (<button type="button" onClick={onSuccess} style={{ marginLeft: 8, padding: "6px 12px" }}>취소</button>)
            }
        </form>
    </div>
    );
}

export default ItemForm;
