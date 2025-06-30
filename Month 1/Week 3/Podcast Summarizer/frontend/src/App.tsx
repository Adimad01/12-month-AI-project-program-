import React, { useState } from "react";
import axios from "axios";
import "./PodcastSummarizer.css";

export default function PodcastSummarizer() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [summary, setSummary] = useState("");
  const [quotes, setQuotes] = useState<string[]>([]);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post("http://localhost:5050/upload", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setSummary(response.data.summary);
      setQuotes(response.data.quotes);
    } catch (err) {
      console.error("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="card">
        <h1 className="title">🎧 Podcast Summarizer</h1>
        <input
          type="file"
          accept="audio/*"
          onChange={(e) => {
            const files = e.target.files;
            if (files && files.length > 0) setFile(files[0]);
          }}
          className="file-input"
        />
        <button
          onClick={handleUpload}
          className="upload-button"
          disabled={loading}
        >
          {loading ? "Processing..." : "Summarize Podcast"}
        </button>
      </div>

      {summary && (
        <div className="summary-section">
          <h2 className="section-title">📄 Summary (via Ollama)</h2>
          <p className="summary-text">{summary}</p>
        </div>
      )}

      {quotes.length > 0 && (
        <div className="quotes-section">
          <h2 className="section-title">💬 Notable Quotes</h2>
          <ul className="quotes-list">
            {quotes.map((q, idx) => (
              <li key={idx} className="quote-item">“{q}”</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}