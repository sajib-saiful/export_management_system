import { useEffect, useState } from "react";
import api from "../services/api";

export default function Suppliers() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: "", phone: "", district: "", address: "" });
  const load = async () => setItems((await api.get("/suppliers")).data);
  useEffect(() => { load(); }, []);
  const submit = async (e) => { e.preventDefault(); await api.post("/suppliers", form); setForm({ name: "", phone: "", district: "", address: "" }); load(); };
  return (
    <div>
      <h3>Suppliers</h3>
      <form onSubmit={submit}>
        {Object.keys(form).map((k) => <input key={k} className="form-control my-2" placeholder={k} value={form[k]} onChange={(e) => setForm({ ...form, [k]: e.target.value })} />)}
        <button className="btn btn-primary">Add Supplier</button>
      </form>
      <table className="table mt-3"><thead><tr><th>Name</th><th>Phone</th><th>District</th><th>Address</th></tr></thead><tbody>{items.map((x) => <tr key={x.id}><td>{x.name}</td><td>{x.phone}</td><td>{x.district}</td><td>{x.address}</td></tr>)}</tbody></table>
    </div>
  );
}
