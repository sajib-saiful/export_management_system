import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Register() {
  const [form, setForm] = useState({ company_name: "", full_name: "", email: "", password: "" });
  const [error, setError] = useState("");
  const nav = useNavigate();

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const { data } = await api.post("/auth/register", form);
      localStorage.setItem("token", data.access_token);
      nav("/dashboard");
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Registration failed. Check backend/CORS.";
      setError(String(msg));
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: 500 }}>
      <h3>Register</h3>
      {error && <div className="alert alert-danger">{error}</div>}
      <form onSubmit={submit}>
        {Object.keys(form).map((k) => (
          <input
            key={k}
            className="form-control my-2"
            type={k === "password" ? "password" : "text"}
            placeholder={k}
            value={form[k]}
            onChange={(e) => setForm({ ...form, [k]: e.target.value })}
          />
        ))}
        <button className="btn btn-success w-100">Register</button>
      </form>
    </div>
  );
}
