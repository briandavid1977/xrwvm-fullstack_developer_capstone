import RegisterPanel from "./components/Register/Register";
import LoginPanel from "./components/Login/Login"
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <Routes>
      <Route path="/register" element={<RegisterPanel />} />
      <Route path="/login" element={<LoginPanel />} />
    </Routes>
  );
}
export default App;
