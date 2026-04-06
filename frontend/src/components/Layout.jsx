import { Link, useLocation } from "react-router-dom";
import { useEffect, useState } from "react";
import api from "../services/api";

const menu = [
  { label: "Dashboard", path: "/dashboard", module: null },
  { label: "Products", path: "/products", module: "products" },
  { label: "Suppliers", path: "/suppliers", module: "suppliers" },
  { label: "Buyers", path: "/buyers", module: "buyers" },
  { label: "Cost Heads", path: "/cost-heads", module: "cost_heads" },
  { label: "Cost Calculator", path: "/cost-calculator", module: "calculations" },
  { label: "Reports", path: "/reports", module: "reports" },
];

export default function Layout({ children }) {
  const location = useLocation();
  const [allowed, setAllowed] = useState([]);
  useEffect(() => {
    (async () => {
      try {
        const { data } = await api.get("/auth/permissions");
        setAllowed(data.filter((x) => x.can_view).map((x) => x.module));
      } catch {
        setAllowed([]);
      }
    })();
  }, []);
  return (
    <div className="d-flex">
      <aside className="bg-dark text-light p-3" style={{ minWidth: 220, minHeight: "100vh" }}>
        <h5>EMS</h5>
        {menu
          .filter((item) => !item.module || allowed.includes(item.module))
          .map((item) => (
          <div key={item.path}>
            <Link className={`text-decoration-none ${location.pathname === item.path ? "text-warning" : "text-light"}`} to={item.path}>
              {item.label}
            </Link>
          </div>
        ))}
      </aside>
      <main className="p-4 w-100">{children}</main>
    </div>
  );
}
