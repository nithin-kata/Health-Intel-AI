/* main.js - Client-Side SPA Coordinator for Healthcare Intelligence AI */

// --- Global Application State ---
const state = {
    user: null,
    loggedIn: false,
    demographics: {
        age: 32,
        gender: "Male",
        pre_existing: "None",
        medications: "None"
    },
    vitals: {
        heart_rate: 78,
        active_minutes: 45,
        water_intake: 6,
        health_score: 92
    },
    activeTab: "dashboard",
    analysisResults: null,
    activeSymptomKey: "general",
    chatHistory: [
        {
            role: "assistant",
            content: "Hello! I am your 24/7 AI Medical Assistant. How are you feeling today? You can describe any symptoms you are experiencing, and I will offer clinical guidance and empathetic support."
        }
    ],
    // Chart.js instances
    symptomChart: null,
    vitalsChart: null
};

// --- API Endpoint Clients ---
async function apiPost(url, payload) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });
        return await response.json();
    } catch (e) {
        console.error("API Call Failed:", e);
        return { success: false, message: "Server connection failed." };
    }
}

async function apiGet(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (e) {
        console.error("API Call Failed:", e);
        return null;
    }
}

// --- DOM elements ---
const dom = {
    landingPage: document.getElementById("landing-page"),
    authPage: document.getElementById("auth-page"),
    appShell: document.getElementById("app-shell"),
    
    // Auth
    tabLoginBtn: document.getElementById("tab-login-btn"),
    tabSignupBtn: document.getElementById("tab-signup-btn"),
    formLogin: document.getElementById("form-login"),
    formSignup: document.getElementById("form-signup"),
    loginEmail: document.getElementById("login-email"),
    loginPass: document.getElementById("login-pass"),
    signupName: document.getElementById("signup-name"),
    signupEmail: document.getElementById("signup-email"),
    signupPass: document.getElementById("signup-pass"),
    submitLogin: document.getElementById("submit-login"),
    submitSignup: document.getElementById("submit-signup"),
    authErrorMsg: document.getElementById("auth-error-msg"),
    btnEnterAuth: document.getElementById("btn-enter-auth"),
    btnBackHome: document.getElementById("btn-back-home"),
    btnLogout: document.getElementById("btn-logout"),
    userDisplayName: document.getElementById("user-display-name"),

    // Sidebar Demographics
    demAge: document.getElementById("dem-age"),
    demGender: document.getElementById("dem-gender"),
    demPreexisting: document.getElementById("dem-preexisting"),
    demMedications: document.getElementById("dem-medications"),
    ageValDisplay: document.getElementById("age-val-display"),

    // Vitals Logger Form
    logHr: document.getElementById("log-hr"),
    logActive: document.getElementById("log-active"),
    logWater: document.getElementById("log-water"),
    logScore: document.getElementById("log-score"),
    logHrDisplay: document.getElementById("log-hr-display"),
    logActiveDisplay: document.getElementById("log-active-display"),
    logWaterDisplay: document.getElementById("log-water-display"),
    logScoreDisplay: document.getElementById("log-score-display"),

    // Metrics displays
    metricHr: document.getElementById("metric-hr"),
    metricHrBadge: document.getElementById("metric-hr-badge"),
    metricActive: document.getElementById("metric-active"),
    metricWater: document.getElementById("metric-water"),
    metricWaterBadge: document.getElementById("metric-water-badge"),
    metricScore: document.getElementById("metric-score"),

    // Symptom Analyzer
    symptomDesc: document.getElementById("symptom-desc"),
    symptomSeverity: document.getElementById("symptom-severity"),
    severityValDisplay: document.getElementById("severity-val-display"),
    symptomDuration: document.getElementById("symptom-duration"),
    engineStatusBadge: document.getElementById("engine-status-badge"),
    btnRunAnalysis: document.getElementById("btn-run-analysis"),
    analyzerResultsWrapper: document.getElementById("analyzer-results-wrapper"),
    conditionsListContainer: document.getElementById("conditions-list-container"),

    // Care Guidelines
    guidelinesPlaceholder: document.getElementById("guidelines-placeholder"),
    guidelinesContentWrapper: document.getElementById("guidelines-content-wrapper"),
    redFlagsList: document.getElementById("red-flags-list"),
    guidelinesTailoredTitle: document.getElementById("guidelines-tailored-title"),
    guidelinesImmediateList: document.getElementById("guidelines-immediate-list"),
    guidelinesDietaryList: document.getElementById("guidelines-dietary-list"),
    guidelinesLifestyleList: document.getElementById("guidelines-lifestyle-list"),

    // Chat
    themeToggleBtn: document.getElementById('theme-toggle'),
    themeToggle: function() {
        this.themeToggleBtn.addEventListener('click', () => {
            document.documentElement.classList.toggle('light-theme');
            const icon = document.getElementById('theme-icon');
            if (document.documentElement.classList.contains('light-theme')) {
                icon.classList.remove('fa-sun');
                icon.classList.add('fa-moon');
            } else {
                icon.classList.remove('fa-moon');
                icon.classList.add('fa-sun');
            }
        });
    },
    chatHistoryBox: document.getElementById("chat-history-box"),
    chatUserMessage: document.getElementById("chat-user-message"),
    btnSendChat: document.getElementById("btn-send-chat"),
    btnClearChat: document.getElementById("btn-clear-chat")
};

// --- Initialization ---
document.addEventListener("DOMContentLoaded", () => {
    setupEventHandlers();
    checkActiveSession();
});

// --- Check Session ---
async function checkActiveSession() {
    // Check if session cookie or cached credentials exist
    const cachedUser = localStorage.getItem("health_user_name");
    const cachedLoggedIn = localStorage.getItem("health_logged_in") === "true";
    
    if (cachedUser && cachedLoggedIn) {
        state.user = cachedUser;
        state.loggedIn = true;
        
        dom.userDisplayName.textContent = state.user;
        showLoggedApp();
    } else {
        showLanding();
    }
}

// --- Toggle Shell Panels ---
function showLanding() {
    dom.landingPage.classList.remove("d-none");
    dom.authPage.classList.add("d-none");
    dom.appShell.classList.add("d-none");
}

function showAuth() {
    dom.landingPage.classList.add("d-none");
    dom.authPage.classList.remove("d-none");
    dom.appShell.classList.add("d-none");
    
    // Clear any previous error message
    dom.authErrorMsg.classList.add("d-none");
}

function showLoggedApp() {
    dom.landingPage.classList.add("d-none");
    dom.authPage.classList.add("d-none");
    dom.appShell.classList.remove("d-none");
    
    // Initialize Dashboard Charts
    loadDashboardData();
    updateSidebarEngineBadge();
}

// --- Bind Interactive Events ---
function setupEventHandlers() {
    // Landing CTA
    dom.btnEnterAuth.addEventListener("click", () => showAuth());
    dom.btnBackHome.addEventListener("click", () => showLanding());
    
    // Auth Tab switching
    dom.tabLoginBtn.addEventListener("click", () => {
        dom.tabLoginBtn.classList.add("active");
        dom.tabSignupBtn.classList.remove("active");
        dom.formLogin.classList.add("active");
        dom.formSignup.classList.remove("active");
    });
    
    dom.tabSignupBtn.addEventListener("click", () => {
        dom.tabLoginBtn.classList.remove("active");
        dom.tabSignupBtn.classList.add("active");
        dom.formLogin.classList.remove("active");
        dom.formSignup.classList.add("active");
    });
    
    // Auth Submit
    dom.submitLogin.addEventListener("click", handleLogin);
    dom.submitSignup.addEventListener("click", handleSignup);
    dom.btnLogout.addEventListener("click", handleLogout);
    
    // Sidebar nav switching
    document.querySelectorAll(".nav-item").forEach(item => {
        item.addEventListener("click", (e) => {
            const targetTab = e.currentTarget.getAttribute("data-target");
            switchTab(targetTab);
        });
    });
    
    // Demographics dynamic update
    dom.demAge.addEventListener("input", (e) => {
        state.demographics.age = parseInt(e.target.value);
        dom.ageValDisplay.textContent = state.demographics.age;
    });
    dom.demGender.addEventListener("change", (e) => {
        state.demographics.gender = e.target.value;
    });
    dom.demPreexisting.addEventListener("input", (e) => {
        state.demographics.pre_existing = e.target.value || "None";
    });
    dom.demMedications.addEventListener("input", (e) => {
        state.demographics.medications = e.target.value || "None";
    });
    
    // Vitals Logger Form (Implemented Feature #1!)
    dom.logHr.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        dom.logHrDisplay.textContent = val;
        updateVitalMetric("heart_rate", val);
    });
    dom.logActive.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        dom.logActiveDisplay.textContent = val;
        updateVitalMetric("active_minutes", val);
    });
    dom.logWater.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        dom.logWaterDisplay.textContent = val;
        updateVitalMetric("water_intake", val);
    });
    dom.logScore.addEventListener("input", (e) => {
        const val = parseInt(e.target.value);
        dom.logScoreDisplay.textContent = val;
        updateVitalMetric("health_score", val);
    });
    
    // Symptom presets click
    document.querySelectorAll(".preset-chip[data-symptom]").forEach(chip => {
        chip.addEventListener("click", (e) => {
            const text = e.currentTarget.getAttribute("data-symptom");
            dom.symptomDesc.value = text;
        });
    });
    
    // Severity slider display
    dom.symptomSeverity.addEventListener("input", (e) => {
        const percentVal = Math.round(e.target.value / 10);
        dom.severityValDisplay.textContent = percentVal;
    });
    
    // Run Symptom Analyzer
    dom.btnRunAnalysis.addEventListener("click", handleRunAnalysis);
    
    // Load fallbacks in Guidelines
    document.querySelectorAll(".btn-load-plan").forEach(btn => {
        btn.addEventListener("click", (e) => {
            const type = e.currentTarget.getAttribute("data-type");
            loadFallbackGuidelines(type);
        });
    });
    
    // Chat presets chips
    document.querySelectorAll(".chat-preset-chip").forEach(chip => {
        chip.addEventListener("click", (e) => {
            const text = e.currentTarget.getAttribute("data-query");
            dom.chatUserMessage.value = text;
            handleSendChatMessage();
        });
    });
    
    // Send chat
    dom.btnSendChat.addEventListener("click", handleSendChatMessage);
    dom.chatUserMessage.addEventListener("keypress", (e) => {
        if (e.key === "Enter") handleSendChatMessage();
    });
    dom.btnClearChat.addEventListener("click", clearChatHistory);
    // Initialize theme toggle button
    dom.themeToggle();
}

// --- Navigation Tabs Switcher ---
function switchTab(tabName) {
    state.activeTab = tabName;
    
    // Update Sidebar Navigation state
    document.querySelectorAll(".nav-item").forEach(item => {
        if (item.getAttribute("data-target") === tabName) {
            item.classList.add("active");
        } else {
            item.classList.remove("active");
        }
    });
    
    // Update active content panels
    document.querySelectorAll(".section-panel").forEach(panel => {
        if (panel.id === `panel-${tabName}`) {
            panel.classList.add("active");
        } else {
            panel.classList.remove("active");
        }
    });
}

// --- Authentication Handler Methods ---
async function handleLogin() {
    const email = dom.loginEmail.value.trim();
    const password = dom.loginPass.value;
    
    if (!email || !password) {
        showAuthError("⚠️ All fields are required.");
        return;
    }
    
    dom.submitLogin.disabled = true;
    dom.submitLogin.textContent = "⏳ AUTHORIZING...";
    
    const res = await apiPost("/api/login", { email, password });
    
    dom.submitLogin.disabled = false;
    dom.submitLogin.textContent = "🔓 AUTHORIZE & ENTER";
    
    if (res.success) {
        state.user = res.user_name;
        state.loggedIn = true;
        
        localStorage.setItem("health_user_name", state.user);
        localStorage.setItem("health_logged_in", "true");
        
        dom.userDisplayName.textContent = state.user;
        showLoggedApp();
    } else {
        showAuthError(res.message);
    }
}

async function handleSignup() {
    const name = dom.signupName.value.trim();
    const email = dom.signupEmail.value.trim();
    const password = dom.signupPass.value;
    
    if (!name || !email || !password) {
        showAuthError("⚠️ All fields are required.");
        return;
    }
    
    if (password.length < 8) {
        showAuthError("❌ Password must be at least 8 characters long.");
        return;
    }
    
    dom.submitSignup.disabled = true;
    dom.submitSignup.textContent = "⏳ CREATING...";
    
    const res = await apiPost("/api/signup", { name, email, password });
    
    dom.submitSignup.disabled = false;
    dom.submitSignup.textContent = "🚀 REGISTER ACCOUNT";
    
    if (res.success) {
        state.user = name;
        state.loggedIn = true;
        
        localStorage.setItem("health_user_name", state.user);
        localStorage.setItem("health_logged_in", "true");
        
        dom.userDisplayName.textContent = state.user;
        showLoggedApp();
    } else {
        showAuthError(res.message);
    }
}

async function handleLogout() {
    await apiPost("/api/logout", {});
    state.user = null;
    state.loggedIn = false;
    
    localStorage.removeItem("health_user_name");
    localStorage.removeItem("health_logged_in");
    
    showLanding();
}

function showAuthError(msg) {
    dom.authErrorMsg.textContent = msg;
    dom.authErrorMsg.classList.remove("d-none");
}

// --- Dynamic Vitals Logger Updates (Implemented Feature #1!) ---
function updateVitalMetric(type, val) {
    // 1. Update internal State model
    state.vitals[type] = val;
    
    // 2. Update dashboard UI cards
    if (type === "heart_rate") {
        dom.metricHr.textContent = val;
        // Adjust badge based on heart rate
        if (val >= 60 && val <= 100) {
            dom.metricHrBadge.textContent = "🟢 Normal Range";
            dom.metricHrBadge.className = "metric-subtext";
            dom.metricHrBadge.style.color = "var(--green-primary)";
        } else {
            dom.metricHrBadge.textContent = "⚠️ Brady/Tachycardia Warning";
            dom.metricHrBadge.className = "metric-subtext";
            dom.metricHrBadge.style.color = "var(--red-primary)";
        }
    } else if (type === "active_minutes") {
        dom.metricActive.textContent = val;
    } else if (type === "water_intake") {
        dom.metricWater.textContent = val;
        // Adjust badge based on water target
        const pct = Math.round((val / 8) * 100);
        if (pct >= 100) {
            dom.metricWaterBadge.textContent = "🟢 Target Achieved!";
            dom.metricWaterBadge.style.color = "var(--green-primary)";
        } else {
            dom.metricWaterBadge.textContent = `🟡 ${pct}% of Daily Target`;
            dom.metricWaterBadge.style.color = "var(--yellow-primary)";
        }
    } else if (type === "health_score") {
        dom.metricScore.textContent = val;
    }
    
    // 3. Immediately propagate dynamic changes into Chart.js elements
    updateChartsLatestData();
}

// --- Load Dashboard Chart Data ---
async function loadDashboardData() {
    // Call server to fetch vitals metrics
    const data = await apiGet("/api/vitals");
    if (!data) return;
    
    // Sync logger values from server config defaults
    dom.logHr.value = data.vitals_current.heart_rate;
    dom.logHrDisplay.textContent = data.vitals_current.heart_rate;
    dom.metricHr.textContent = data.vitals_current.heart_rate;
    state.vitals.heart_rate = data.vitals_current.heart_rate;
    
    dom.logActive.value = data.vitals_current.active_minutes;
    dom.logActiveDisplay.textContent = data.vitals_current.active_minutes;
    dom.metricActive.textContent = data.vitals_current.active_minutes;
    state.vitals.active_minutes = data.vitals_current.active_minutes;
    
    dom.logWater.value = data.vitals_current.water_intake;
    dom.logWaterDisplay.textContent = data.vitals_current.water_intake;
    dom.metricWater.textContent = data.vitals_current.water_intake;
    state.vitals.water_intake = data.vitals_current.water_intake;
    
    dom.logScore.value = data.vitals_current.health_score;
    dom.logScoreDisplay.textContent = data.vitals_current.health_score;
    dom.metricScore.textContent = data.vitals_current.health_score;
    state.vitals.health_score = data.vitals_current.health_score;
    
    // Draw neon Charts using Chart.js
    renderNeonCharts(data.history);
}

function renderNeonCharts(history) {
    const labels = history.map(item => item.Date);
    const severityData = history.map(item => item["Symptom Severity (1-10)"]);
    const sleepData = history.map(item => item["Sleep Duration (Hours)"]);
    const waterData = history.map(item => item["Water Intake (Glasses)"]);
    
    // Destroy previous Chart instances if they exist
    if (state.symptomChart) state.symptomChart.destroy();
    if (state.vitalsChart) state.vitalsChart.destroy();
    
    // 1. Neon Symptom Severity Line Chart
    const ctx1 = document.getElementById("symptom-trend-chart").getContext("2d");
    const gradient1 = ctx1.createLinearGradient(0, 0, 0, 250);
    gradient1.addColorStop(0, "rgba(6, 182, 212, 0.4)");
    gradient1.addColorStop(1, "rgba(6, 182, 212, 0)");
    
    state.symptomChart = new Chart(ctx1, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Symptom Severity (1-10)',
                data: severityData,
                borderColor: '#06B6D4',
                borderWidth: 3,
                backgroundColor: gradient1,
                fill: true,
                tension: 0.3,
                pointBackgroundColor: '#FFF',
                pointBorderColor: '#06B6D4',
                pointHoverRadius: 7,
                shadowColor: 'rgba(6, 182, 212, 0.5)',
                shadowBlur: 10
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94A3B8' }
                },
                y: {
                    min: 0,
                    max: 10,
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94A3B8' }
                }
            }
        }
    });
    
    // 2. Sleep vs Water Intake Grouped Bar Chart
    const ctx2 = document.getElementById("vitals-group-chart").getContext("2d");
    state.vitalsChart = new Chart(ctx2, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [
                {
                    label: 'Sleep Duration (Hours)',
                    data: sleepData,
                    backgroundColor: '#8B5CF6',
                    borderRadius: 5,
                    borderWidth: 0
                },
                {
                    label: 'Water Intake (Glasses)',
                    data: waterData,
                    backgroundColor: '#3B82F6',
                    borderRadius: 5,
                    borderWidth: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    labels: { color: '#94A3B8', font: { family: 'Inter' } }
                }
            },
            scales: {
                x: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94A3B8' }
                },
                y: {
                    grid: { color: 'rgba(255, 255, 255, 0.05)' },
                    ticks: { color: '#94A3B8' }
                }
            }
        }
    });
}

function updateChartsLatestData() {
    if (!state.symptomChart || !state.vitalsChart) return;
    
    // 1. Update line chart logic if symptom active exists
    // (Optional: can bind user severity range updates)
    
    // 2. Propagate logged water levels into the latest element in the datasets
    const waterIdx = state.vitalsChart.data.datasets.findIndex(d => d.label.includes("Water"));
    if (waterIdx !== -1) {
        const lastIdx = state.vitalsChart.data.datasets[waterIdx].data.length - 1;
        state.vitalsChart.data.datasets[waterIdx].data[lastIdx] = state.vitals.water_intake;
        state.vitalsChart.update();
    }
}

// --- Update Engine Active Label ---
function updateSidebarEngineBadge() {
    // Show details about active engine config
    const key = localStorage.getItem("groq_api_key") || "";
    const label = (key.startsWith("gsk_")) ? "🌐 Groq Live API Mode Active" : "💻 Local Clinical Simulation Active";
    dom.engineStatusBadge.textContent = label;
}

// --- Run Predictive Clinical Assessment ---
async function handleRunAnalysis() {
    const desc = dom.symptomDesc.value.trim();
    const severityVal = Math.round(dom.symptomSeverity.value / 10);
    const durationVal = dom.symptomDuration.value;
    
    if (!desc) {
        alert("⚠️ Please describe your symptoms or click one of the quick presets before running the assessment.");
        return;
    }
    
    dom.btnRunAnalysis.disabled = true;
    dom.btnRunAnalysis.textContent = "⏳ RUNNING CLINICAL DIAGNOSIS...";
    
    const payload = {
        symptom_text: desc,
        demographics: state.demographics,
        severity: severityVal,
        duration: durationVal
    };
    
    const res = await apiPost("/api/analyze", payload);
    
    dom.btnRunAnalysis.disabled = false;
    dom.btnRunAnalysis.textContent = "🚀 RUN PROACTIVE CLINICAL ASSESSMENT";
    
    if (res.success) {
        state.analysisResults = res.results;
        state.activeSymptomKey = res.symptom_key;
        
        renderAnalysisResults(res.results);
        renderGuidelines(res.results.treatment_plan);
    } else {
        alert("❌ Diagnosis execution failed: " + res.message);
    }
}

function renderAnalysisResults(results) {
    dom.conditionsListContainer.innerHTML = "";
    
    results.conditions.forEach(cond => {
        let riskClass = "badge-low";
        if (cond.risk === "HIGH") riskClass = "badge-high";
        else if (cond.risk === "MEDIUM") riskClass = "badge-med";
        
        const likelihoodDisplay = (cond.likelihood < 1) ? Math.round(cond.likelihood * 100) : cond.likelihood;
        const condHtml = `
            <div class="condition-card">
                <div class="condition-left">
                    <span style="font-size: 1.15rem; font-weight: 700; color: #FFF;">${cond.name}</span>
                    <span class="badge ${riskClass}" style="margin-left: 8px;">${cond.risk} RISK</span>
                    <p style="color:var(--text-muted); font-size:0.9rem; margin-top:8px;">${cond.nlp_reason}</p>
                </div>
                <div class="condition-right">
                    <div style="font-weight: 600; color: var(--cyan-primary); margin-bottom: 5px;">Likelihood: ${likelihoodDisplay}%</div>
                    <div class="condition-progress">
                        <div class="condition-progress-bar" style="width: ${likelihoodDisplay}%"></div>
                    </div>
                </div>
            </div>
        `;
        dom.conditionsListContainer.insertAdjacentHTML("beforeend", condHtml);
    });
    
    dom.analyzerResultsWrapper.classList.remove("d-none");
    
    // If a user clicks to view guidelines, switch tabs smoothly
    // (Self-directed: scroll down to findings)
    dom.analyzerResultsWrapper.scrollIntoView({ behavior: 'smooth' });
}

// --- Load Treatment Plan Guidelines ---
function renderGuidelines(plan) {
    // 1. Hide placeholder card, reveal Guidelines panels
    dom.guidelinesPlaceholder.classList.add("d-none");
    dom.guidelinesContentWrapper.classList.remove("d-none");
    
    // 2. Set title
    const topic = state.activeSymptomKey.replace(/_/g, " ").toUpperCase();
    dom.guidelinesTailoredTitle.textContent = `Tailored Guidelines: ${topic} Support`;
    
    // 3. Render pulsing Safety warnings
    dom.redFlagsList.innerHTML = "";
    plan.red_flags.forEach(item => {
        dom.redFlagsList.insertAdjacentHTML("beforeend", `<li>${item}</li>`);
    });
    
    // 4. Fill Immediate Actions column
    dom.guidelinesImmediateList.innerHTML = "";
    plan.immediate_actions.forEach((act, idx) => {
        dom.guidelinesImmediateList.insertAdjacentHTML("beforeend", `
            <div class="guideline-item">
                <strong>${idx+1}.</strong> ${act}
            </div>
        `);
    });
    
    // 5. Fill Dietary column
    dom.guidelinesDietaryList.innerHTML = "";
    plan.dietary.forEach((diet, idx) => {
        dom.guidelinesDietaryList.insertAdjacentHTML("beforeend", `
            <div class="guideline-item">
                <strong>${idx+1}.</strong> ${diet}
            </div>
        `);
    });
    
    // 6. Fill Lifestyle column
    dom.guidelinesLifestyleList.innerHTML = "";
    plan.lifestyle.forEach((life, idx) => {
        dom.guidelinesLifestyleList.insertAdjacentHTML("beforeend", `
            <div class="guideline-item">
                <strong>${idx+1}.</strong> ${life}
            </div>
        `);
    });
}

// --- Load Guidelines presets directly ---
async function loadFallbackGuidelines(type) {
    const res = await apiPost("/api/analyze", {
        symptom_text: type,
        demographics: state.demographics,
        severity: 5,
        duration: "1-3 Days",
        force_fallback: true
    });
    
    if (res.success) {
        state.activeSymptomKey = res.symptom_key;
        renderGuidelines(res.results.treatment_plan);
    }
}

// --- Empathetic Chatbot Logics ---
function renderChatBubbles() {
    dom.chatHistoryBox.innerHTML = "";
    
    state.chatHistory.forEach(msg => {
        const avatar = (msg.role === "user") ? "👤" : "⚕️";
        const bubbleClass = (msg.role === "user") ? "user" : "assistant";
        
        const bubbleHtml = `
            <div class="chat-bubble ${bubbleClass}">
                <div class="chat-avatar">${avatar}</div>
                <div>${msg.content}</div>
            </div>
        `;
        dom.chatHistoryBox.insertAdjacentHTML("beforeend", bubbleHtml);
    });
    
    // Scroll chat to the bottom
    dom.chatHistoryBox.scrollTop = dom.chatHistoryBox.scrollHeight;
}

async function handleSendChatMessage() {
    const msg = dom.chatUserMessage.value.trim();
    if (!msg) return;
    
    // Clear input box
    dom.chatUserMessage.value = "";
    
    // Append User Message to State & redraw
    state.chatHistory.push({ role: "user", content: msg });
    renderChatBubbles();
    
    // Add dynamic glowing typing state indicator
    const typingHtml = `
        <div id="chat-typing-bubble" class="chat-bubble assistant" style="opacity: 0.65;">
            <div class="chat-avatar">⚕️</div>
            <div>⏳ <i>Assistant is analyzing message...</i></div>
        </div>
    `;
    dom.chatHistoryBox.insertAdjacentHTML("beforeend", typingHtml);
    dom.chatHistoryBox.scrollTop = dom.chatHistoryBox.scrollHeight;
    
    const payload = {
        message: msg,
        history: state.chatHistory.slice(0, -1), // Send history before current msg
        demographics: state.demographics
    };
    
    const res = await apiPost("/api/chat", payload);
    
    // Remove typing bubble
    const typingBubble = document.getElementById("chat-typing-bubble");
    if (typingBubble) typingBubble.remove();
    
    if (res.success) {
        state.chatHistory.push({ role: "assistant", content: res.response });
    } else {
        state.chatHistory.push({ role: "assistant", content: "❌ Failed to connect: " + res.message });
    }
    
    renderChatBubbles();
}

function clearChatHistory() {
    state.chatHistory = [
        {
            role: "assistant",
            content: "Hello! I am your 24/7 AI Medical Assistant. How are you feeling today? You can describe any symptoms you are experiencing, and I will offer clinical guidance and empathetic support."
        }
    ];
    renderChatBubbles();
}
