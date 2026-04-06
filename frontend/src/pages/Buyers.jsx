import { useEffect, useState } from "react";
import api from "../services/api";

export default function Buyers() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: "", company_name: "", country: "", email: "", phone: "" });
  const load = async () => setItems((await api.get("/buyers")).data);
  useEffect(() => { load(); }, []);
  const submit = async (e) => { e.preventDefault(); await api.post("/buyers", form); setForm({ name: "", company_name: "", country: "", email: "", phone: "" }); load(); };
  return (
    <div>
      <h3>Buyers</h3>
      <form onSubmit={submit}>
        {Object.keys(form).map((k) => <input key={k} className="form-control my-2" placeholder={k} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />)}
        <button className="btn btn-primary">Add Buyer</button>
      </form>
      <table className="table mt-3"><thead><tr><th>Name</th><th>Company</th><th>Country</th><th>Email</th><th>Phone</th></tr></thead><tbody>{items.map((x) => <tr key={x.id}><td>{x.name}</td><td>{x.company_name}</td><td>{x.country}</td><td>{x.email}</td><td>{x.phone}</td></tr>)}</tbody></table>
    </div>
  );
}
