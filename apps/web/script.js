const PILLARS = [
  "energy",
  "water",
  "waste",
  "packaging",
  "supply_chain",
  "community",
];

const WEIGHTS = {
  energy: 0.2,
  water: 0.15,
  waste: 0.2,
  packaging: 0.15,
  supply_chain: 0.2,
  community: 0.1,
};

const tierFromScore = (score) => {
  if (score >= 80) return "Leader";
  if (score >= 60) return "Progressing";
  if (score >= 40) return "Emerging";
  return "Starter";
};

const toNumber = (value) => {
  const parsed = Number(value);
  if (Number.isNaN(parsed)) return 0;
  return Math.max(0, Math.min(100, parsed));
};

const computeReport = (scores) => {
  const weightedScore = PILLARS.reduce(
    (sum, pillar) => sum + toNumber(scores[pillar]) * WEIGHTS[pillar],
    0,
  );

  const ordered = [...PILLARS].sort((a, b) => scores[a] - scores[b]).slice(0, 3);

  const priorities = ordered.map(
    (pillar) =>
      `Increase ${pillar.replace("_", " ")} initiatives (current score: ${scores[pillar]})`,
  );

  return {
    weightedScore: Number(weightedScore.toFixed(2)),
    tier: tierFromScore(weightedScore),
    priorities,
  };
};

const scoreNode = document.getElementById("scoreNumber");
const tierNode = document.getElementById("tierBadge");
const progressNode = document.getElementById("progressBar");
const resultNode = document.getElementById("result");
const formNode = document.getElementById("assessmentForm");

document.getElementById("year").textContent = new Date().getFullYear();

const animateScore = (target) => {
  const start = Number(scoreNode.textContent) || 0;
  const durationMs = 700;
  const begin = performance.now();

  const tick = (now) => {
    const progress = Math.min(1, (now - begin) / durationMs);
    const current = start + (target - start) * progress;
    scoreNode.textContent = current.toFixed(1);
    if (progress < 1) requestAnimationFrame(tick);
  };

  requestAnimationFrame(tick);
};

const renderResult = (report) => {
  const list = report.priorities.map((item) => `<li>${item}</li>`).join("");
  resultNode.innerHTML = `
    <h3>Your guidance output</h3>
    <p><strong>Tier:</strong> ${report.tier} &nbsp;|&nbsp; <strong>Score:</strong> ${report.weightedScore}</p>
    <p class="muted">Top 3 sustainability shift priorities:</p>
    <ul>${list}</ul>
  `;

  tierNode.textContent = report.tier;
  progressNode.style.width = `${report.weightedScore}%`;
  animateScore(report.weightedScore);
};

formNode.addEventListener("submit", (event) => {
  event.preventDefault();
  const formData = new FormData(formNode);
  const scores = Object.fromEntries(PILLARS.map((pillar) => [pillar, toNumber(formData.get(pillar))]));
  renderResult(computeReport(scores));
});

window.addEventListener("load", () => {
  const initialData = new FormData(formNode);
  const scores = Object.fromEntries(PILLARS.map((pillar) => [pillar, toNumber(initialData.get(pillar))]));
  renderResult(computeReport(scores));
});
