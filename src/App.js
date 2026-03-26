import { useState, useEffect } from "react";

const BASE = "http://127.0.0.1:8000";

export default function App() {
  const [showLogin, setShowLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [tasks, setTasks] = useState([]);
  const [title, setTitle] = useState("");

  const token = localStorage.getItem("token");

  const request = async (url, method, body) => {
    const res = await fetch(BASE + url, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: token || "",
      },
      body: body ? JSON.stringify(body) : null,
    });
    return res.json();
  };

 const load = async () => {
  const data = await request("/tasks", "GET");
  setTasks(Array.isArray(data) ? data : []);
};

  useEffect(() => {
    if (token) {
      setShowLogin(false);
      load();
    }
  }, []);

  // 🔐 LOGIN
  const login = async () => {
    const res = await request("/login", "POST", { email, password });
    if (res.access_token) {
      localStorage.setItem("token", res.access_token);
      setShowLogin(false);
      load();
    }
  };

  // ➕ TASK
  const add = async () => {
    if (!title) return;
    await request("/tasks", "POST", { title });
    setTitle("");
    load();
  };

  const toggle = async (id) => {
    await request(`/tasks/${id}`, "PUT");
    load();
  };

  const del = async (id) => {
    await request(`/tasks/${id}`, "DELETE");
    load();
  };

  const logout = () => {
    localStorage.removeItem("token");
    setShowLogin(true);
  };

  return (
    <div style={{ fontFamily: "Arial", padding: 20 }}>
      <h2 style={{ textAlign: "center" }}>Task Manager</h2>

      {/* 🔐 LOGIN POPUP */}
      {showLogin && (
        <div style={overlay}>
          <div style={modal}>
            <h3>Login</h3>
            <input
              placeholder="Email"
              onChange={(e) => setEmail(e.target.value)}
              style={input}
            />
            <input
              type="password"
              placeholder="Password"
              onChange={(e) => setPassword(e.target.value)}
              style={input}
            />
            <button onClick={login} style={button}>
              Login
            </button>
          </div>
        </div>
      )}

      {/* 📋 DASHBOARD */}
      {!showLogin && (
        <div style={{ maxWidth: 500, margin: "auto" }}>
          <div style={{ display: "flex", gap: 10, marginBottom: 20 }}>
            <input
              value={title}
              placeholder="Enter task..."
              onChange={(e) => setTitle(e.target.value)}
              style={input}
            />
            <button onClick={add} style={button}>
              Add
            </button>
          </div>

          {tasks.map((t) => (
            <div key={t.id} style={taskCard}>
              <div>
                <input
                  type="checkbox"
                  checked={t.completed}
                  onChange={() => toggle(t.id)}
                />
                <span
                  style={{
                    marginLeft: 10,
                    textDecoration: t.completed ? "line-through" : "none",
                  }}
                >
                  {t.title}
                </span>
              </div>

              <button onClick={() => del(t.id)} style={deleteBtn}>
                Delete
              </button>
            </div>
          ))}

          <button onClick={logout} style={logoutBtn}>
            Logout
          </button>
        </div>
      )}
    </div>
  );
}

// 🎨 STYLES
const overlay = {
  position: "fixed",
  top: 0,
  left: 0,
  width: "100%",
  height: "100%",
  background: "rgba(0,0,0,0.5)",
  display: "flex",
  justifyContent: "center",
  alignItems: "center",
};

const modal = {
  background: "white",
  padding: 20,
  borderRadius: 10,
  display: "flex",
  flexDirection: "column",
  gap: 10,
  width: 300,
};

const input = {
  padding: 10,
  borderRadius: 8,
  border: "1px solid #ccc",
  width: "100%",
};

const button = {
  padding: 10,
  borderRadius: 8,
  background: "#4CAF50",
  color: "white",
  border: "none",
  cursor: "pointer",
};

const deleteBtn = {
  background: "red",
  color: "white",
  border: "none",
  padding: "5px 10px",
  borderRadius: 6,
};

const logoutBtn = {
  marginTop: 20,
  width: "100%",
  padding: 10,
  background: "#333",
  color: "white",
  border: "none",
  borderRadius: 8,
};

const taskCard = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: 12,
  marginBottom: 10,
  borderRadius: 10,
  background: "#f5f5f5",
};