import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "./components/Layout";
import Buyers from "./pages/Buyers";
import CostCalculator from "./pages/CostCalculator";
import CostHeads from "./pages/CostHeads";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Products from "./pages/Products";
import Register from "./pages/Register";
import Reports from "./pages/Reports";
import Suppliers from "./pages/Suppliers";

function Protected({ children }) {
  const token = localStorage.getItem("token");
  return token ? children : <Navigate to="/login" replace />;
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />
      <Route
        path="/*"
        element={
          <Protected>
            <Layout>
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/products" element={<Products />} />
                <Route path="/suppliers" element={<Suppliers />} />
                <Route path="/buyers" element={<Buyers />} />
                <Route path="/cost-heads" element={<CostHeads />} />
                <Route path="/cost-calculator" element={<CostCalculator />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="*" element={<Navigate to="/dashboard" replace />} />
              </Routes>
            </Layout>
          </Protected>
        }
      />
    </Routes>
  );
}
