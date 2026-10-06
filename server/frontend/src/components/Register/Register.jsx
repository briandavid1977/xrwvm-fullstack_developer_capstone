import React, { useState } from "react";
import Header from "../Header/Header";
import "./Register.css";

export default function Register() {
  const [form, setForm] = useState({
    userName: "",
    firstName: "",
    lastName: "",
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  const update = (event) => {
    setForm({ ...form, [event.target.name]: event.target.value });
  };

  const register = async (event) => {
    event.preventDefault();
    setError("");
    setBusy(true);

    try {
      const response = await fetch("/djangoapp/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      const data = await response.json();

      if (response.ok && data.status === "Authenticated") {
        sessionStorage.setItem("username", data.userName);
        window.location.href = "/";
      } else {
        setError(data.error || "Registration failed. Please try again.");
      }
    } catch (error) {
      setError("Could not reach the server. Please try again.");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div>
      <Header />
      <form className="register_container" onSubmit={register}>
        <h2 style={{ textAlign: "center" }}>Create an account</h2>
        <div className="inputs">
          <label htmlFor="register-username">Username</label>
          <input id="register-username" className="input_field"
            name="userName" value={form.userName} onChange={update}
            autoComplete="username" maxLength={150} required />

          <label htmlFor="register-firstname">First name</label>
          <input id="register-firstname" className="input_field"
            name="firstName" value={form.firstName} onChange={update}
            autoComplete="given-name" maxLength={150} required />

          <label htmlFor="register-lastname">Last name</label>
          <input id="register-lastname" className="input_field"
            name="lastName" value={form.lastName} onChange={update}
            autoComplete="family-name" maxLength={150} required />

          <label htmlFor="register-email">Email</label>
          <input id="register-email" className="input_field" type="email"
            name="email" value={form.email} onChange={update}
            autoComplete="email" maxLength={254} required />

          <label htmlFor="register-password">Password</label>
          <input id="register-password" className="input_field" type="password"
            name="password" value={form.password} onChange={update}
            autoComplete="new-password" minLength={8} required />

          <p style={{ padding: "0 20px" }}>
            Use at least 8 characters. Avoid common passwords or only numbers.
          </p>
          {error && <p role="alert" style={{ padding: "0 20px" }}>{error}</p>}
        </div>

        <div className="submit_panel">
          <button className="submit" type="submit" disabled={busy}>
            {busy ? "Creating..." : "Register"}
          </button>
          <a href="/login" style={{ textAlign: "center", marginTop: "15px" }}>
            Already have an account? Login
          </a>
          <a href="/" style={{ textAlign: "center", marginTop: "10px" }}>
            Cancel
          </a>
        </div>
      </form>
    </div>
  );
}
