const API_URL = "";

// Handle file selection styling
document.getElementById('fileInput').addEventListener('change', function(e) {
  const fileName = e.target.files[0] ? e.target.files[0].name : "Select PDF Resume";
  document.getElementById('fileName').innerText = fileName;
});

async function uploadReady() {
  const fileInput = document.getElementById("fileInput");
  const uploadStatus = document.getElementById("uploadStatus");
  const btn = document.getElementById("uploadBtn");

  if (!fileInput.files[0]) {
    uploadStatus.innerText = "Please select a file first.";
    uploadStatus.style.color = "#ef4444"; // red
    return;
  }

  const formData = new FormData();
  formData.append("file", fileInput.files[0]);

  btn.innerText = "Analyzing...";
  btn.disabled = true;
  uploadStatus.innerText = "";

  try {
    const res = await fetch(`${API_URL}/upload/`, {
      method: "POST",
      body: formData
    });

    const data = await res.json();
    
    if (res.ok) {
      uploadStatus.innerText = "Resume Initialized! You can now analyze it.";
      uploadStatus.style.color = "var(--success)";
      document.getElementById('tabs').style.display = 'flex';
      document.getElementById('qaTab').style.display = 'block';
    } else {
      uploadStatus.innerText = data.detail || "Upload failed.";
      uploadStatus.style.color = "#ef4444";
    }
  } catch (error) {
    uploadStatus.innerText = "Server connection error.";
    uploadStatus.style.color = "#ef4444";
  } finally {
    btn.innerText = "Initialize Resume";
    btn.disabled = false;
  }
}

function switchTab(tabId) {
  document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none');
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  
  document.getElementById(tabId).style.display = 'block';
  event.target.classList.add('active');
}

async function analyzeQA() {
  const query = document.getElementById("query").value;
  const resultDiv = document.getElementById("qaResult");
  const loader = document.getElementById("qaLoader");

  if (!query) return;

  resultDiv.style.display = 'none';
  loader.style.display = 'block';

  try {
    const res = await fetch(`${API_URL}/analyze/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query })
    });

    const data = await res.json();
    loader.style.display = 'none';
    resultDiv.style.display = 'block';
    
    if (res.ok) {
      // Basic markdown formatting to HTML for bolding/bullets can be added here if needed
      resultDiv.innerHTML = data.result.replace(/\n/g, '<br>');
    } else {
      resultDiv.innerText = "Error: " + data.detail;
    }
  } catch (error) {
    loader.style.display = 'none';
    resultDiv.style.display = 'block';
    resultDiv.innerText = "Server error.";
  }
}

async function analyzeJD() {
  const jobDesc = document.getElementById("jobDesc").value;
  const dashboard = document.getElementById("jdDashboard");
  const loader = document.getElementById("jdLoader");

  if (!jobDesc) return;

  dashboard.classList.add('hidden');
  loader.style.display = 'block';

  try {
    const res = await fetch(`${API_URL}/score/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ job_description: jobDesc })
    });

    const data = await res.json();
    loader.style.display = 'none';
    dashboard.classList.remove('hidden');
    
    if (res.ok) {
        animateScore(parseInt(data.score) || 0);
        document.getElementById('missingSkillsResult').innerHTML = formatResult(data.missing_skills);
        document.getElementById('improvementsResult').innerHTML = formatResult(data.improvements);
    } else {
        document.getElementById('missingSkillsResult').innerText = "Error: " + data.detail;
    }
  } catch (error) {
    loader.style.display = 'none';
    dashboard.classList.remove('hidden');
    document.getElementById('missingSkillsResult').innerText = "Server error.";
  }
}

function formatResult(text) {
    if (!text) return "None detected.";
    return text.replace(/-/g, '<br>• ').replace(/\n/g, '');
}

function animateScore(score) {
  const path = document.getElementById('scorePath');
  const text = document.getElementById('scoreText');
  
  // Set stroke-dasharray. First value is length, second is gap.
  // 100 max circle length.
  path.style.strokeDasharray = `${score}, 100`;
  
  // Change color based on score
  if(score >= 80) path.style.stroke = "var(--success)";
  else if (score >= 50) path.style.stroke = "#f59e0b"; // yellow
  else path.style.stroke = "#ef4444"; // red

  // Animate text counter
  let current = 0;
  let interval = setInterval(() => {
    if(current >= score) {
      clearInterval(interval);
      text.textContent = score;
    } else {
      current++;
      text.textContent = current;
    }
  }, 20);
}
