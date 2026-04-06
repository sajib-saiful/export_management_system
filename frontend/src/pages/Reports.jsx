import { useEffect, useState } from "react";
import jsPDF from "jspdf";
import api from "../services/api";

export default function Reports() {
  const [rows, setRows] = useState([]);
  const [calcRows, setCalcRows] = useState([]);
  useEffect(() => {
    (async () => {
      setRows((await api.get("/reports/price-history")).data);
      setCalcRows((await api.get("/calculations")).data);
    })();
  }, []);

  const exportCalcPdf = (row) => {
    const pdf = new jsPDF();
    pdf.text("Calculation Report", 20, 20);
    pdf.text(`ID: ${row.id}`, 20, 35);
    pdf.text(`FOB: ${row.total_fob}`, 20, 45);
    pdf.text(`CFR: ${row.total_cfr}`, 20, 55);
    pdf.text(`CPT: ${row.total_cpt}`, 20, 65);
    pdf.save(`calculation-${row.id}.pdf`);
  };

  return (
    <div>
      <h3>Reports</h3>
      <h5>Product Price History</h5>
      <table className="table"><thead><tr><th>Product</th><th>Date</th><th>Price</th></tr></thead><tbody>{rows.map((r, i) => <tr key={i}><td>{r.product_name}</td><td>{r.date}</td><td>{r.price}</td></tr>)}</tbody></table>
      <h5>Calculation History (PDF)</h5>
      <table className="table"><thead><tr><th>ID</th><th>FOB</th><th>CFR</th><th>CPT</th><th></th></tr></thead><tbody>{calcRows.map((r) => <tr key={r.id}><td>{r.id}</td><td>{r.total_fob}</td><td>{r.total_cfr}</td><td>{r.total_cpt}</td><td><button className="btn btn-sm btn-outline-primary" onClick={() => exportCalcPdf(r)}>Export PDF</button></td></tr>)}</tbody></table>
    </div>
  );
}
