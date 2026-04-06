import { useEffect, useState } from "react";
import api from "../services/api";

export default function CostHeads() {
  const [items, setItems] = useState([]);
  const [form, setForm] = useState({ name: "", type: "FOB", is_active: true });

  const load = async () => setItems((await api.get("/cost-heads")).data);
  useEffect(() => {
    load();
  }, []);

  const submit = async (e) => {
    e.preventDefault();
    await api.post("/cost-heads", form);
    setForm({ name: "", type: "FOB", is_active: true });
    load();
  };

  return (
    <div>
      <h3>Cost Heads</h3>
      <form onSubmit={submit}>
        <input
          className="form-control my-2"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
        />
        <select
          className="form-control my-2"
          value={form.type}
          onChange={(e) => setForm({ ...form, type: e.target.value })}
        >
          <option value="FOB">FOB</option>
          <option value="CFR">CFR</option>
          <option value="CPT">CPT</option>
        </select>
        <div className="form-check my-2">
          <input
            id="is_active"
            className="form-check-input"
            type="checkbox"
            checked={form.is_active}
            onChange={(e) => setForm({ ...form, is_active: e.target.checked })}
          />
          <label className="form-check-label" htmlFor="is_active">
            Active
          </label>
        </div>
        <button className="btn btn-primary">Add Cost Head</button>
      </form>

      <table className="table mt-3">
        <thead>
          <tr>
            <th>Name</th>
            <th>Type</th>
            <th>Active</th>
          </tr>
        </thead>
        <tbody>
          {items.map((x) => (
            <tr key={x.id}>
              <td>{x.name}</td>
              <td>{x.type}</td>
              <td>{x.is_active ? "Yes" : "No"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
