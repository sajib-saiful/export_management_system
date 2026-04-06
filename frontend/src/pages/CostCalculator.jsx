import { useEffect, useMemo, useState } from "react";
import api from "../services/api";

export default function CostCalculator() {
  const [products, setProducts] = useState([]);
  const [heads, setHeads] = useState([]);
  const [productId, setProductId] = useState("");
  const [amounts, setAmounts] = useState({});
  const [result, setResult] = useState(null);

  useEffect(() => {
    (async () => {
      setProducts((await api.get("/products")).data);
      setHeads((await api.get("/cost-heads")).data.filter((x) => x.is_active));
    })();
  }, []);

  const payload = useMemo(
    () => ({
      product_id: Number(productId),
      entries: heads.map((h) => ({ cost_head_id: h.id, amount: Number(amounts[h.id] || 0) })),
    }),
    [heads, productId, amounts]
  );

  const submit = async (e) => {
    e.preventDefault();
    const { data } = await api.post("/calculations", payload);
    setResult(data);
  };

  return (
    <div>
      <h3>Dynamic Cost Calculator</h3>
      <form onSubmit={submit}>
        <select className="form-control my-2" value={productId} onChange={(e) => setProductId(e.target.value)}>
          <option value="">Select Product</option>
          {products.map((p) => <option key={p.id} value={p.id}>{p.name}</option>)}
        </select>
        {heads.map((h) => (
          <input key={h.id} className="form-control my-2" type="number" step="0.01" placeholder={`${h.name} (${h.type})`} onChange={(e) => setAmounts({ ...amounts, [h.id]: e.target.value })} />
        ))}
        <button className="btn btn-success">Calculate</button>
      </form>
      {result && <div className="mt-3 alert alert-info">FOB: {result.total_fob} | CFR: {result.total_cfr} | CPT: {result.total_cpt}</div>}
    </div>
  );
}
