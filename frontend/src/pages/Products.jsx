import { useEffect, useState } from "react";
import api from "../services/api";

export default function Products() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: "", category: "", grade: "", unit: "" });
  const load = async () => setItems((await api.get("/products")).data);
  useEffect(() => { load(); }, []);
  const submit = async (e) => { e.preventDefault(); await api.post("/products", form); setForm({ name: "", category: "", grade: "", unit: "" }); load(); };
  return (
    <div>
      <h3>Products</h3>
      <form className="row g-2" onSubmit={submit}>
        {Object.keys(form).map((k) => <input key={k} className="form-control" placeholder={k} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />)}
        <button className="btn btn-primary">Add Product</button>
      </form>
      <table className="table mt-3"><thead><tr><th>Name</th><th>Category</th><th>Grade</th><th>Unit</th></tr></thead><tbody>{items.map((x) => <tr key={x.id}><td>{x.name}</td><td>{x.category}</td><td>{x.grade}</td><td>{x.unit}</td></tr>)}</tbody></table>
    </div>
  );
}
