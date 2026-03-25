import { useState } from "react";
import "./styles.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

function App() {

  const [form, setForm] = useState({
    condition: "",
    age: 25,
    severity: 5
  });

  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [detectedCondition, setDetectedCondition] = useState("");

  // =========================
  // 🔥 CONFIDENCE
  // =========================
  const getConfidence = (score, reviews) => {
    const normScore = Math.min(Math.max(score / 15, 0), 1);
    const reviewFactor = Math.min(Math.log1p(reviews) / 10, 1);
    return Math.round((normScore * 0.6 + reviewFactor * 0.4) * 100);
  };

  const getColor = (c) => {
    if (c > 80) return "#22c55e";
    if (c > 60) return "#facc15";
    return "#ef4444";
  };

  // =========================
  // 🔥 SEVERITY COLOR
  // =========================
  const getSeverityColor = (value) => {
    if (value <= 3) return "#22c55e";
    if (value <= 6) return "#facc15";
    return "#ef4444";
  };

  // =========================
  // 🔥 SUGGESTIONS FIXED
  // =========================
  const handleSuggest = async (q) => {
    setForm({ ...form, condition: q });

    const res = await fetch(`http://127.0.0.1:5000/suggest?q=${q}`);
    let data = await res.json();

    // ❌ remove garbage suggestions
    data = data.filter(item => !item.includes("users found"));

    // ❌ remove HTML tags
    data = data.map(item => item.replace(/<[^>]*>/g, ""));

    setSuggestions(data);
  };

  // =========================
  // PREDICT
  // =========================
  const handleSubmit = async () => {
    setLoading(true);
    setResult(null);

    const res = await fetch("http://127.0.0.1:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form)
    });

    const data = await res.json();

    if (data.status === "success") {
      setResult(data);
    }

    setLoading(false);
  };

  // =========================
  // PDF UPLOAD
  // =========================
  const handleReportUpload = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setResult(null);

    const res = await fetch("http://127.0.0.1:5000/analyze-report", {
      method: "POST",
      body: formData
    });

    const data = await res.json();

    if (data.status === "success") {
      setDetectedCondition(data.detected_condition);

      setResult({
        best_drug: data.best_drug,
        top_5: data.top_5
      });
    }

    setLoading(false);
  };

  return (
    <div className="container-main">

      <h1 className="title">💊 AI Drug Recommendation</h1>

      {/* ========================= */}
      {/* REPORT SECTION */}
      {/* ========================= */}
      <div className="card premium-card">
        <h2>🧪 Analyze Medical Report</h2>

        <input
          type="file"
          accept=".pdf"
          onChange={(e) => handleReportUpload(e.target.files[0])}
        />

        {detectedCondition && (
          <p className="detected">
            🧠 {detectedCondition}
          </p>
        )}
      </div>

      {/* ========================= */}
      {/* INPUT SECTION */}
      {/* ========================= */}
      <div className="card premium-card">

        {/* 🔥 SEARCH */}
        <input
          className="search-box"
          placeholder="🔍 Search medical condition..."
          value={form.condition}
          onChange={(e) => handleSuggest(e.target.value)}
        />

        {/* 🔥 SUGGESTIONS */}
        {suggestions.length > 0 && (
          <div className="suggestions">
            {suggestions.map((s, i) => (
              <div
                key={i}
                onClick={() => {
                  setForm({ ...form, condition: s });
                  setSuggestions([]);
                }}
              >
                {s}
              </div>
            ))}
          </div>
        )}

        {/* AGE */}
        <label>Age: {form.age}</label>
        <input
          type="range"
          min="18"
          max="80"
          value={form.age}
          onChange={(e) =>
            setForm({ ...form, age: Number(e.target.value) })
          }
        />

        {/* SEVERITY */}
        <label>Severity: {form.severity}</label>
        <input
          type="range"
          min="1"
          max="10"
          value={form.severity}
          style={{ accentColor: getSeverityColor(form.severity) }}
          onChange={(e) =>
            setForm({ ...form, severity: Number(e.target.value) })
          }
        />

        {/* 🔥 PREMIUM BUTTON */}
        <button className="predict-btn" onClick={handleSubmit}>
          🚀 Predict Best Drug
        </button>

      </div>

      {/* ========================= */}
      {/* LOADER */}
      {/* ========================= */}
      {loading && (
        <div className="loader-wrapper">
          <div className="loader">
            <div className="dash uno"></div>
            <div className="dash dos"></div>
            <div className="dash tres"></div>
            <div className="dash cuatro"></div>
          </div>
          <p>Analyzing medical data...</p>
        </div>
      )}

      {/* ========================= */}
      {/* RESULTS */}
      {/* ========================= */}
      {result && result.top_5 && (
        <div className="card premium-card">

          <h2>✅ Best Drug: {result.best_drug}</h2>

          {/* GRAPH */}
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={result.top_5}>
              <XAxis dataKey="drug" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="score" />
            </BarChart>
          </ResponsiveContainer>

          {/* CARDS */}
          <div className="drug-grid">
            {result.top_5.map((d, i) => {
              const conf = getConfidence(d.score, d.review_count || 0);
              const color = getColor(conf);

              return (
                <div key={i} className="drug-card premium-card">

                  <h3>{d.drug}</h3>

                  <p>🟢 {d.recovery_days}</p>

                  <p>📊 {conf}% confidence</p>
                  <p>👥 {d.review_count || 0} patients</p>

                  {/* 🔥 BAR */}
                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${conf}%`,
                        background: color
                      }}
                    />
                  </div>

                  <button
                    className="explain-btn"
                    onClick={() =>
                      setExpanded(i === expanded ? null : i)
                    }
                  >
                    {expanded === i ? "Hide" : "Explain"}
                  </button>

                  {expanded === i && (
                    <p className="explanation">{d.explanation}</p>
                  )}
                </div>
              );
            })}
          </div>

        </div>
      )}

    </div>
  );
}

export default App;