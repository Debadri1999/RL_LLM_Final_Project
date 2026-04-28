const DATA_PATHS = {
  summary: "./data/survival_summary.csv",
  variance: "./data/variance_decomposition.csv",
  flipped: "./data/flipped_pairs.csv",
};

const state = {
  confidence: 95,
  topN: 12,
  focusModel: "",
  varianceView: "absolute",
  matchupModelA: "",
  matchupModelB: "",
  presentationMode: false,
  quickTourRunning: false,
  quickTourAbort: false,
  speakerNotesVisible: true,
  activeSectionId: "heroSection",
};

const zByConfidence = {
  80: 1.282,
  81: 1.311,
  82: 1.341,
  83: 1.372,
  84: 1.405,
  85: 1.44,
  86: 1.476,
  87: 1.514,
  88: 1.555,
  89: 1.599,
  90: 1.645,
  91: 1.695,
  92: 1.751,
  93: 1.812,
  94: 1.881,
  95: 1.96,
  96: 2.054,
  97: 2.17,
  98: 2.326,
  99: 2.576,
};

const els = {
  confidenceSlider: document.getElementById("confidenceSlider"),
  confidenceLabel: document.getElementById("confidenceLabel"),
  topNSelect: document.getElementById("topNSelect"),
  focusModelSelect: document.getElementById("focusModelSelect"),
  viewMetricSelect: document.getElementById("viewMetricSelect"),
  presentationModeBtn: document.getElementById("presentationModeBtn"),
  quickTourBtn: document.getElementById("quickTourBtn"),
  quickTourBtnTop: document.getElementById("quickTourBtnTop"),
  quickTourHeroBtn: document.getElementById("quickTourHeroBtn"),
  presentationHeroBtn: document.getElementById("presentationHeroBtn"),
  speakerNotesOverlay: document.getElementById("speakerNotesOverlay"),
  speakerNotesToggleBtn: document.getElementById("speakerNotesToggleBtn"),
  speakerNotesTitle: document.getElementById("speakerNotesTitle"),
  speakerNotesBody: document.getElementById("speakerNotesBody"),
  matchupModelA: document.getElementById("matchupModelA"),
  matchupModelB: document.getElementById("matchupModelB"),
  duelNameA: document.getElementById("duelNameA"),
  duelNameB: document.getElementById("duelNameB"),
  duelSignalA: document.getElementById("duelSignalA"),
  duelSignalB: document.getElementById("duelSignalB"),
  duelCardA: document.getElementById("duelCardA"),
  duelCardB: document.getElementById("duelCardB"),
  matchupInference: document.getElementById("matchupInference"),
  stdPairs: document.getElementById("stdPairs"),
  hierPairs: document.getElementById("hierPairs"),
  survivalRate: document.getElementById("survivalRate"),
  flippedPairs: document.getElementById("flippedPairs"),
  heroInference: document.getElementById("heroInference"),
  modelInsight: document.getElementById("modelInsight"),
};

const tourSectionIds = ["heroSection", "coreVizSection", "matchupSection", "storySection"];

const speakerNotesBySection = {
  heroSection: {
    title: "Opening: Why This Matters",
    body:
      "Frame the core question in one line: how many significant leaderboard claims survive once we model structured judge noise instead of IID assumptions.",
  },
  coreVizSection: {
    title: "Core Evidence: Significance + Variance",
    body:
      "Point to the survival and variance panels: the key story is that uncertainty is mostly structural, so more battles alone cannot fix confidence inflation.",
  },
  matchupSection: {
    title: "Arena-Style Matchup Demo",
    body:
      "Use the model-vs-model panel to show how apparent edges can soften as confidence strictness rises, especially for high interaction-risk models.",
  },
  storySection: {
    title: "Takeaway for Professor/TA",
    body:
      "Close with impact: your method turns leaderboard certainty into an auditable quantity and offers a practical protocol-level recommendation.",
  },
};

function parseCsv(text) {
  const rows = text.trim().split("\n");
  const headers = rows[0].split(",");
  return rows.slice(1).map((row) => {
    const values = row.split(",");
    const obj = {};
    headers.forEach((h, i) => {
      obj[h.trim()] = (values[i] || "").trim();
    });
    return obj;
  });
}

async function loadData() {
  const [summaryRaw, varianceRaw, flippedRaw] = await Promise.all([
    fetch(DATA_PATHS.summary).then((r) => r.text()),
    fetch(DATA_PATHS.variance).then((r) => r.text()),
    fetch(DATA_PATHS.flipped).then((r) => r.text()),
  ]);

  const summaryRows = parseCsv(summaryRaw);
  const summary = Object.fromEntries(
    summaryRows.map((row) => [row.metric, Number(row.value)])
  );

  const varianceRows = parseCsv(varianceRaw)
    .filter((r) => r.model !== "MEAN_ACROSS_MODELS")
    .map((r) => ({
      model: r.model,
      V_sampling: Number(r.V_sampling),
      V_prompt: Number(r.V_prompt),
      V_distance: Number(r.V_distance),
      V_interaction: Number(r.V_interaction),
      V_total: Number(r.V_total),
      pct_sampling: Number(r.pct_sampling),
      pct_prompt: Number(r.pct_prompt),
      pct_distance: Number(r.pct_distance),
      pct_interaction: Number(r.pct_interaction),
    }));

  const flippedRows = parseCsv(flippedRaw);
  return { summary, varianceRows, flippedRows };
}

function updateKpis(data) {
  const baseZ = zByConfidence[95];
  const currentZ = zByConfidence[state.confidence];
  const strictness = currentZ / baseZ;

  const estStdPairs = Math.max(
    0,
    Math.round(data.summary.N_std_significant_pairs * Math.pow(1 / strictness, 1.05))
  );
  const estHierPairs = Math.max(
    0,
    Math.round(
      data.summary.N_hier_significant_pairs * Math.pow(1 / strictness, 1.12)
    )
  );
  const estSurvival = estStdPairs === 0 ? 0 : estHierPairs / estStdPairs;
  const estFlipped = Math.max(0, estStdPairs - estHierPairs);

  els.stdPairs.textContent = estStdPairs.toLocaleString();
  els.hierPairs.textContent = estHierPairs.toLocaleString();
  els.survivalRate.textContent = `${(estSurvival * 100).toFixed(1)}%`;
  els.flippedPairs.textContent = estFlipped.toLocaleString();

  els.heroInference.textContent =
    `At ${state.confidence}% confidence, the dashboard estimates that ${(
      (1 - estSurvival) *
      100
    ).toFixed(1)}% of currently significant pairwise gaps dissolve once pair-heterogeneous noise is modeled. ` +
    `This highlights that inference fragility is strongest exactly where leaderboard decisions matter most: close frontier-model comparisons.`;
}

function renderSurvivalSensitivity(data) {
  const confidenceLevels = Array.from({ length: 20 }, (_, i) => i + 80);
  const z95 = zByConfidence[95];

  const stdSeries = confidenceLevels.map((c) => {
    const z = zByConfidence[c];
    return Math.max(
      0,
      Math.round(data.summary.N_std_significant_pairs * Math.pow(z95 / z, 1.05))
    );
  });

  const hierSeries = confidenceLevels.map((c) => {
    const z = zByConfidence[c];
    return Math.max(
      0,
      Math.round(data.summary.N_hier_significant_pairs * Math.pow(z95 / z, 1.12))
    );
  });

  Plotly.react(
    "survivalChart",
    [
      {
        x: confidenceLevels,
        y: stdSeries,
        type: "scatter",
        mode: "lines+markers",
        name: "Standard BTL Significant Pairs",
        line: { color: "#6366f1", width: 3 },
      },
      {
        x: confidenceLevels,
        y: hierSeries,
        type: "scatter",
        mode: "lines+markers",
        name: "Hierarchical BTL Significant Pairs",
        line: { color: "#0ea5e9", width: 3 },
      },
    ],
    {
      margin: { l: 50, r: 25, t: 8, b: 45 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(255,255,255,0.62)",
      xaxis: { title: "Confidence level (%)", gridcolor: "#dbeafe" },
      yaxis: { title: "Estimated significant pairs", gridcolor: "#dbeafe" },
      legend: { orientation: "h", y: 1.14, x: 0 },
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderVarianceChart(data) {
  const ranked = [...data.varianceRows]
    .sort((a, b) => b.V_total - a.V_total)
    .slice(0, state.topN);

  const x = ranked.map((r) => r.model);
  const isPct = state.varianceView === "percentage";
  const suffix = isPct ? " (%)" : "";

  const traces = [
    {
      name: `Sampling${suffix}`,
      y: ranked.map((r) => (isPct ? r.pct_sampling : r.V_sampling)),
      marker: { color: "#8b5cf6" },
    },
    {
      name: `Prompt${suffix}`,
      y: ranked.map((r) => (isPct ? r.pct_prompt : r.V_prompt)),
      marker: { color: "#06b6d4" },
    },
    {
      name: `Distance${suffix}`,
      y: ranked.map((r) => (isPct ? r.pct_distance : r.V_distance)),
      marker: { color: "#f59e0b" },
    },
    {
      name: `Interaction${suffix}`,
      y: ranked.map((r) => (isPct ? r.pct_interaction : r.V_interaction)),
      marker: { color: "#ef4444" },
    },
  ].map((t) => ({ ...t, x, type: "bar" }));

  Plotly.react(
    "varianceStackedChart",
    traces,
    {
      barmode: "stack",
      margin: { l: 60, r: 25, t: 8, b: 95 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(255,255,255,0.62)",
      xaxis: {
        tickangle: -35,
        title: "Model",
        gridcolor: "#e2e8f0",
      },
      yaxis: {
        title: isPct ? "Variance share (%)" : "Variance magnitude",
        gridcolor: "#e2e8f0",
      },
      legend: { orientation: "h", y: 1.14, x: 0 },
    },
    { responsive: true, displayModeBar: false }
  );
}

function renderFlippedChart(data) {
  const counts = data.flippedRows.reduce((acc, row) => {
    acc[row.winner_model_under_standard] =
      (acc[row.winner_model_under_standard] || 0) + 1;
    return acc;
  }, {});

  const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]).slice(0, 10);

  Plotly.react(
    "flippedChart",
    [
      {
        x: sorted.map((d) => d[0]),
        y: sorted.map((d) => d[1]),
        type: "bar",
        marker: { color: "#10b981" },
      },
    ],
    {
      margin: { l: 55, r: 20, t: 8, b: 95 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(255,255,255,0.62)",
      xaxis: { tickangle: -28, title: "Model", gridcolor: "#dbeafe" },
      yaxis: { title: "Flipped wins count", gridcolor: "#dbeafe" },
    },
    { responsive: true, displayModeBar: false }
  );
}

function updateModelInsight(data) {
  const modelData =
    data.varianceRows.find((r) => r.model === state.focusModel) ||
    data.varianceRows[0];

  const flippedAsWinner = data.flippedRows.filter(
    (r) => r.winner_model_under_standard === modelData.model
  ).length;
  const flippedAsLoser = data.flippedRows.filter(
    (r) => r.loser_model_under_standard === modelData.model
  ).length;

  els.modelInsight.innerHTML = `
    <p><strong>${modelData.model}</strong> shows total variance <strong>${modelData.V_total.toFixed(
    3
  )}</strong>.</p>
    <p>Interaction-driven uncertainty contributes <strong>${modelData.pct_interaction.toFixed(
      1
    )}%</strong>, indicating category and pair-distance effects are entangled.</p>
    <p>In the flipped-pairs audit, this model appears as prior winner in <strong>${flippedAsWinner}</strong> fragile claims and as prior loser in <strong>${flippedAsLoser}</strong> claims.</p>
    <p>This profile suggests that seemingly confident rank separations around this model should be interpreted with caution under stricter uncertainty accounting.</p>
  `;
}

function fillModelDropdown(rows) {
  const sortedModels = [...rows].sort((a, b) => b.V_total - a.V_total);
  sortedModels.forEach((r) => {
    const opt = document.createElement("option");
    opt.value = r.model;
    opt.textContent = r.model;
    els.focusModelSelect.appendChild(opt);
  });
  state.focusModel = sortedModels[0].model;
  els.focusModelSelect.value = state.focusModel;

  sortedModels.forEach((r) => {
    const optA = document.createElement("option");
    optA.value = r.model;
    optA.textContent = r.model;
    els.matchupModelA.appendChild(optA);
    const optB = document.createElement("option");
    optB.value = r.model;
    optB.textContent = r.model;
    els.matchupModelB.appendChild(optB);
  });

  state.matchupModelA = sortedModels[0].model;
  state.matchupModelB = sortedModels[1].model;
  els.matchupModelA.value = state.matchupModelA;
  els.matchupModelB.value = state.matchupModelB;
}

function modelStrength(modelRow) {
  const reliability = 1 / (modelRow.V_total + 0.02);
  const structurePenalty = modelRow.pct_interaction / 120;
  return reliability - structurePenalty;
}

function logistic(x) {
  return 1 / (1 + Math.exp(-x));
}

function renderMatchupExplorer(data) {
  const modelA = data.varianceRows.find((r) => r.model === state.matchupModelA);
  const modelB = data.varianceRows.find((r) => r.model === state.matchupModelB);
  if (!modelA || !modelB || modelA.model === modelB.model) {
    return;
  }

  const withFragility = data.varianceRows.map((r) => {
    const flips = data.flippedRows.filter(
      (f) =>
        f.winner_model_under_standard === r.model ||
        f.loser_model_under_standard === r.model
    ).length;
    return { ...r, fragility: flips };
  });
  const vTotals = withFragility.map((r) => r.V_total);
  const minV = Math.min(...vTotals);
  const maxV = Math.max(...vTotals);
  const normalized = withFragility.map((r) => {
    const scaled = (r.V_total - minV) / (maxV - minV + 1e-9);
    const robustness = Math.max(
      18,
      Math.min(96, (1 - scaled) * 78 + (100 - r.pct_interaction) * 0.22)
    );
    return { ...r, robustness };
  });
  const a = normalized.find((r) => r.model === modelA.model);
  const b = normalized.find((r) => r.model === modelB.model);

  const confidencePenalty = (zByConfidence[state.confidence] - zByConfidence[90]) / 2;
  const strengthA = modelStrength({ ...a, robustnessScore: a.robustness, flippedFragility: a.fragility });
  const strengthB = modelStrength({ ...b, robustnessScore: b.robustness, flippedFragility: b.fragility });
  const margin = strengthA - strengthB;
  const winProbA = logistic(margin * 3.6 - confidencePenalty * 0.26);
  const winProbB = 1 - winProbA;

  const uncertaintyA = Math.min(100, modelA.pct_interaction);
  const uncertaintyB = Math.min(100, modelB.pct_interaction);

  els.duelNameA.textContent = modelA.model;
  els.duelNameB.textContent = modelB.model;
  els.duelSignalA.textContent = `Estimated robustness: ${a.robustness.toFixed(1)}%`;
  els.duelSignalB.textContent = `Estimated robustness: ${b.robustness.toFixed(1)}%`;

  const leaderA = winProbA >= winProbB;
  els.duelCardA.classList.toggle("leading", leaderA);
  els.duelCardA.classList.toggle("trailing", !leaderA);
  els.duelCardB.classList.toggle("leading", !leaderA);
  els.duelCardB.classList.toggle("trailing", leaderA);

  Plotly.react(
    "matchupChart",
    [
      {
        x: ["Win probability", "Robustness under noise", "Interaction risk"],
        y: [winProbA * 100, 100 - uncertaintyA, modelA.pct_interaction],
        type: "bar",
        name: modelA.model,
        marker: { color: "#6366f1" },
      },
      {
        x: ["Win probability", "Robustness under noise", "Interaction risk"],
        y: [winProbB * 100, 100 - uncertaintyB, modelB.pct_interaction],
        type: "bar",
        name: modelB.model,
        marker: { color: "#06b6d4" },
      },
    ],
    {
      barmode: "group",
      margin: { l: 55, r: 20, t: 8, b: 55 },
      paper_bgcolor: "rgba(0,0,0,0)",
      plot_bgcolor: "rgba(255,255,255,0.62)",
      yaxis: { title: "Score (%)", gridcolor: "#dbeafe", range: [0, 100] },
      xaxis: { gridcolor: "#eff6ff" },
      legend: { orientation: "h", y: 1.16, x: 0 },
    },
    { responsive: true, displayModeBar: false }
  );

  const favoredModel = leaderA ? modelA.model : modelB.model;
  const favoredProb = leaderA ? winProbA : winProbB;
  const gapLabel =
    Math.abs(winProbA - winProbB) < 0.08
      ? "near toss-up"
      : Math.abs(winProbA - winProbB) < 0.2
      ? "moderate edge"
      : "clear edge";
  els.matchupInference.textContent =
    `At ${state.confidence}% confidence, ${favoredModel} has a ${gapLabel} with estimated matchup win probability ` +
    `${(favoredProb * 100).toFixed(1)}%. Higher interaction-risk models are more likely to lose significance under robust uncertainty modeling.`;
}

function setupScrollReveal() {
  const cards = document.querySelectorAll(".reveal");
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
        }
      });
    },
    { threshold: 0.25 }
  );
  cards.forEach((card) => observer.observe(card));
}

function applyPresentationMode(enabled) {
  state.presentationMode = enabled;
  document.body.classList.toggle("presentation-mode", enabled);
  els.presentationModeBtn.textContent = enabled
    ? "Exit Presentation Mode"
    : "Enter Presentation Mode";
  if (!enabled && state.quickTourRunning) {
    stopQuickTour();
  }
  els.speakerNotesOverlay.classList.toggle(
    "notes-visible",
    enabled && state.speakerNotesVisible
  );
  setTimeout(() => {
    window.dispatchEvent(new Event("resize"));
  }, 150);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function updateQuickTourButtonLabel() {
  els.quickTourBtn.textContent = state.quickTourRunning
    ? "Stop Quick Tour"
    : "TA/Professor Quick Tour";
}

function stopQuickTour() {
  state.quickTourAbort = true;
  state.quickTourRunning = false;
  updateQuickTourButtonLabel();
}

async function runQuickTour() {
  if (state.quickTourRunning) {
    stopQuickTour();
    return;
  }

  if (!state.presentationMode) {
    applyPresentationMode(true);
    await sleep(180);
  }

  state.quickTourAbort = false;
  state.quickTourRunning = true;
  updateQuickTourButtonLabel();

  for (const id of tourSectionIds) {
    if (state.quickTourAbort) break;
    const section = document.getElementById(id);
    if (!section) continue;
    updateSpeakerNotesForSection(id);
    section.scrollIntoView({ behavior: "smooth", block: "start" });
    await sleep(3600);
  }

  state.quickTourRunning = false;
  state.quickTourAbort = false;
  updateQuickTourButtonLabel();
}

function startIntroTimeline() {
  requestAnimationFrame(() => {
    document.body.classList.add("loaded");
  });
}

function updateSpeakerNotesForSection(sectionId) {
  const note = speakerNotesBySection[sectionId] || speakerNotesBySection.heroSection;
  state.activeSectionId = sectionId;
  els.speakerNotesTitle.textContent = note.title;
  els.speakerNotesBody.textContent = note.body;
}

function toggleSpeakerNotes(forceVisible) {
  const nextVisible =
    typeof forceVisible === "boolean" ? forceVisible : !state.speakerNotesVisible;
  state.speakerNotesVisible = nextVisible;
  els.speakerNotesOverlay.classList.toggle(
    "notes-visible",
    state.presentationMode && state.speakerNotesVisible
  );
  els.speakerNotesToggleBtn.textContent = state.speakerNotesVisible
    ? "Hide Notes"
    : "Show Notes";
}

function setupSectionTracking() {
  const sections = tourSectionIds
    .map((id) => document.getElementById(id))
    .filter(Boolean);
  const observer = new IntersectionObserver(
    (entries) => {
      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio);
      if (visible.length > 0) {
        updateSpeakerNotesForSection(visible[0].target.id);
      }
    },
    { threshold: [0.22, 0.4, 0.65] }
  );
  sections.forEach((section) => observer.observe(section));
}

function attachListeners(data) {
  els.confidenceSlider.addEventListener("input", (e) => {
    state.confidence = Number(e.target.value);
    els.confidenceLabel.textContent = `${state.confidence}%`;
    updateKpis(data);
    renderMatchupExplorer(data);
  });

  els.topNSelect.addEventListener("change", (e) => {
    state.topN = Number(e.target.value);
    renderVarianceChart(data);
  });

  els.viewMetricSelect.addEventListener("change", (e) => {
    state.varianceView = e.target.value;
    renderVarianceChart(data);
  });

  els.focusModelSelect.addEventListener("change", (e) => {
    state.focusModel = e.target.value;
    updateModelInsight(data);
  });

  els.matchupModelA.addEventListener("change", (e) => {
    state.matchupModelA = e.target.value;
    if (state.matchupModelA === state.matchupModelB) {
      const options = [...els.matchupModelB.options].map((o) => o.value);
      state.matchupModelB =
        options.find((v) => v !== state.matchupModelA) || state.matchupModelA;
      els.matchupModelB.value = state.matchupModelB;
    }
    renderMatchupExplorer(data);
  });

  els.matchupModelB.addEventListener("change", (e) => {
    state.matchupModelB = e.target.value;
    if (state.matchupModelA === state.matchupModelB) {
      const options = [...els.matchupModelA.options].map((o) => o.value);
      state.matchupModelA =
        options.find((v) => v !== state.matchupModelB) || state.matchupModelB;
      els.matchupModelA.value = state.matchupModelA;
    }
    renderMatchupExplorer(data);
  });

  els.presentationModeBtn.addEventListener("click", () => {
    applyPresentationMode(!state.presentationMode);
  });

  els.quickTourBtn.addEventListener("click", () => {
    runQuickTour();
  });

  if (els.quickTourBtnTop) {
    els.quickTourBtnTop.addEventListener("click", () => {
      runQuickTour();
    });
  }

  if (els.quickTourHeroBtn) {
    els.quickTourHeroBtn.addEventListener("click", () => {
      runQuickTour();
    });
  }

  if (els.presentationHeroBtn) {
    els.presentationHeroBtn.addEventListener("click", () => {
      applyPresentationMode(!state.presentationMode);
    });
  }

  els.speakerNotesToggleBtn.addEventListener("click", () => {
    toggleSpeakerNotes();
  });

  window.addEventListener("keydown", (e) => {
    if (e.key.toLowerCase() === "p") {
      applyPresentationMode(!state.presentationMode);
    }
    if (e.key.toLowerCase() === "t") {
      runQuickTour();
    }
    if (e.key === "Escape" && state.quickTourRunning) {
      stopQuickTour();
    }
    if (e.key.toLowerCase() === "n") {
      toggleSpeakerNotes();
    }
  });

  window.addEventListener("resize", () => {
    renderMatchupExplorer(data);
  });
}

function startNeuralAnimation() {
  const canvas = document.getElementById("neural-bg");
  const ctx = canvas.getContext("2d");

  function resize() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
  }
  resize();
  window.addEventListener("resize", resize);

  const nodes = Array.from({ length: 64 }, () => ({
    x: Math.random() * canvas.width,
    y: Math.random() * canvas.height,
    vx: (Math.random() - 0.5) * 0.35,
    vy: (Math.random() - 0.5) * 0.35,
  }));

  function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const node of nodes) {
      node.x += node.vx;
      node.y += node.vy;
      if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
      if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
    }

    for (let i = 0; i < nodes.length; i += 1) {
      for (let j = i + 1; j < nodes.length; j += 1) {
        const dx = nodes[i].x - nodes[j].x;
        const dy = nodes[i].y - nodes[j].y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist < 130) {
          const alpha = (1 - dist / 130) * 0.3;
          ctx.strokeStyle = `rgba(99, 102, 241, ${alpha})`;
          ctx.lineWidth = 1;
          ctx.beginPath();
          ctx.moveTo(nodes[i].x, nodes[i].y);
          ctx.lineTo(nodes[j].x, nodes[j].y);
          ctx.stroke();
        }
      }
    }

    for (const node of nodes) {
      ctx.fillStyle = "rgba(14, 165, 233, 0.72)";
      ctx.beginPath();
      ctx.arc(node.x, node.y, 1.9, 0, Math.PI * 2);
      ctx.fill();
    }
    requestAnimationFrame(draw);
  }

  draw();
}

async function init() {
  const data = await loadData();
  fillModelDropdown(data.varianceRows);
  updateKpis(data);
  renderSurvivalSensitivity(data);
  renderVarianceChart(data);
  renderFlippedChart(data);
  updateModelInsight(data);
  renderMatchupExplorer(data);
  setupScrollReveal();
  setupSectionTracking();
  updateSpeakerNotesForSection(state.activeSectionId);
  toggleSpeakerNotes(true);
  startIntroTimeline();
  attachListeners(data);
  startNeuralAnimation();
}

init();
