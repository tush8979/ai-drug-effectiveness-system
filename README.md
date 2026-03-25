<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>💊 AI Drug Effectiveness Prediction System</title>
  <style>
    body {
      font-family: "Segoe UI", sans-serif;
      background: #f8f9fa;
      color: #333;
      margin: 0;
      padding: 40px 20px;
    }
    h1 {
      margin: 0 0 16px 0;
      text-align: center;
      color: #2c3e50;
    }
    p {
      text-align: center;
      margin: 0 0 24px 0;
    }
    .badges {
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
      gap: 8px;
      margin: 24px 0;
    }
    .badge {
      display: inline-block;
      margin: 4px;
      padding: 4px 12px;
      border-radius: 4px;
      font-size: 12px;
      font-weight: bold;
    }
    .badge-react {
      background: #61dafb;
      color: #2c3e50;
    }
    .badge-flask {
      background: #222222;
      color: #fff;
    }
    .badge-sklearn {
      background: #fab03d;
      color: #2c3e50;
    }
    .badge-llama {
      background: #7ac143;
      color: #2c3e50;
    }
    .badge-active {
      background: #28a745;
      color: #fff;
    }
    .badge-yt {
      background: #e74c3c;
      color: #fff;
    }
    hr {
      border: 1px solid #ddd;
      margin: 32px 0;
    }
    section {
      max-width: 900px;
      margin: 0 auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      margin: 16px 0;
    }
    th, td {
      border: 1px solid #ddd;
      padding: 8px 12px;
      text-align: left;
    }
    th {
      background: #eaeaea;
    }
    img {
      display: block;
      margin: 16px auto;
    }
    pre {
      background: #f4f4f4;
      padding: 12px;
      border-radius: 4px;
      overflow-x: auto;
    }
  </style>
</head>
<body>

  <section>

    <h1 align="center">💊 AI Drug Effectiveness Prediction System</h1>

    <p align="center">
      <b>Predict the most effective drug using ML + LLM based on real patient data</b>
    </p>

    <div class="badges" align="center">
      <span class="badge badge-react">Frontend: React</span>
      <span class="badge badge-flask">Backend: Flask</span>
      <span class="badge badge-sklearn">ML: Scikit‑Learn</span>
      <span class="badge badge-llama">LLM: LLaMA (Local)</span>
      <span class="badge badge-active">Status: Active</span>
    </div>

    <hr />

    <h2>🎥 Demo Video</h2>
    <p align="center">
      <a href="https://youtu.be/MpBNdcjojZE" target="_blank">
        <span class="badge badge-yt">▶️ Watch Demo (YouTube)</span>
      </a>
    </p>

    <hr />

    <h2>🧠 Core Idea</h2>
    <p>
      This system compares different drugs used for the <strong>same medical condition</strong> and determines:
    </p>
    <ul>
      <li>⏱️ Recovery duration (days)</li>
      <li>📊 Drug effectiveness across patients</li>
      <li>⚠️ Side effect risk</li>
      <li>📃 Medical reviews</li>
      <li>👥 Patient review count</li>
    </ul>
    <p>
      👉 Goal: Identify the <strong>most effective drug with faster recovery and fewer side effects</strong>.
    </p>

    <hr />

    <h2>🔥 Features</h2>
    <ul>
      <li>✅ ML‑based drug ranking system</li>
      <li>⏱️ Recovery duration prediction (e.g., 18–21 days, 24–27 days)</li>
      <li>📊 Confidence score based on patient reviews</li>
      <li>👥 Patient count for real‑world validation</li>
      <li>🤖 LLM‑based personalized drug explanations</li>
      <li>📄 Blood report PDF → auto disease detection</li>
      <li>🔍 Smart condition search (fuzzy matching)</li>
      <li>🎯 Drug effectiveness comparison across multiple patients</li>
    </ul>

    <hr />

    <h2>🧪 Machine Learning Models Used</h2>
    <ul>
      <li>🔹 Regression Model (Scikit‑learn)</li>
      <li>🔹 Feature Scaling (StandardScaler)</li>
      <li>🔹 Custom Hybrid Scoring System</li>
      <li>🔹 Fuzzy Matching (Difflib)</li>
    </ul>

    <hr />

    <h2>📊 How It Works</h2>
    <ol>
      <li><strong>User inputs:</strong>
        <ul>
          <li>Condition</li>
          <li>Age</li>
          <li>Severity</li>
        </ul>
      </li>
      <li><strong>System:</strong>
        <ul>
          <li>Matches condition using fuzzy logic</li>
          <li>Filters relevant drugs</li>
          <li>Calculates effectiveness score</li>
          <li>Ranks top drugs</li>
        </ul>
      </li>
      <li><strong>Output:</strong>
        <ul>
          <li>🏆 Best drug</li>
          <li>⏱️ Recovery duration range</li>
          <li>📊 Confidence score</li>
          <li>👥 Number of patients</li>
          <li>💡 Explanation (LLM)</li>
        </ul>
      </li>
    </ol>

    <hr />

    <h2>⚙️ Tech Stack</h2>
    <table>
      <tr>
        <th>Layer</th>
        <th>Technology</th>
      </tr>
      <tr>
        <td>Frontend</td>
        <td>React.js</td>
      </tr>
      <tr>
        <td>Backend</td>
        <td>Flask</td>
      </tr>
      <tr>
        <td>ML</td>
        <td>Scikit‑learn</td>
      </tr>
      <tr>
        <td>LLM</td>
        <td>LLaMA (Local)</td>
      </tr>
      <tr>
        <td>Data</td>
        <td>Pandas, NumPy</td>
      </tr>
    </table>

    <hr />

    <h2>🔄 System Flow</h2>
    <pre>
A [User Input] --&gt; B [Condition Matching]
B --&gt; C [Drug Filtering]
C --&gt; D [ML + Statistical Scoring]
D --&gt; E [Top Drug Ranking]
E --&gt; F [Recovery Time + Confidence]
F --&gt; G [LLM Explanation]
    </pre>

    <hr />

    <h2>📸 Screenshots</h2>
    <p align="center">
      <img src="screenshots/home.png" alt="Home Page" width="80%"/>
    </p>
    <p align="center">
      <img src="screenshots/search.png" alt="Search Page" width="80%"/>
    </p>
    <p align="center">
      <img src="screenshots/result.png" alt="Result Page" width="80%"/>
    </p>

    <hr />

    <h2>▶️ Run Locally</h2>
    <pre>
cd backend
pip install -r requirements.txt
python app.py

cd frontend
npm install
npm start
    </pre>

    <p align="center">
      🚀 Built with passion for AI in Healthcare
    </p>

  </section>

</body>
</html>
