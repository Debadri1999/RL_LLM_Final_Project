#!/usr/bin/env bash
# download_papers.sh
# Bulk-download all arXiv PDFs referenced in the project into pdfs/
#
# USAGE (from your local machine — not inside the Cowork sandbox):
#   cd "C:\Users\DOUBLEDO_GAMING\OneDrive\Desktop\PURDUE SPRING'25\MOD-4\MGMT-59000-RL&LLM\Final_Project\02_Literature_Notes"
#   bash download_papers.sh
#
# Requires: curl (Git Bash / WSL / macOS / Linux all have it by default)
# Classical references (Dawid-Skene, Bradley-Terry) must be obtained via Purdue
# library / JSTOR — they are not on arXiv.

set -euo pipefail

mkdir -p pdfs
cd pdfs

echo "Downloading arXiv papers..."

# ============================================================
# A. Primary anchor
# ============================================================
curl -L -o "A1_Xu2026_JudgeAwareRanking.pdf"        "https://arxiv.org/pdf/2601.21817.pdf"

# ============================================================
# B. Required background
# ============================================================
curl -L -o "B1_Chiang2024_ChatbotArena.pdf"         "https://arxiv.org/pdf/2403.04132.pdf"
curl -L -o "B2_Zhu2023_JudgeLM.pdf"                 "https://arxiv.org/pdf/2310.17631.pdf"
curl -L -o "B3_Gu2024_JudgeSurvey.pdf"              "https://arxiv.org/pdf/2411.15594.pdf"

# ============================================================
# C. Track 2 advanced topics we cite
# ============================================================
curl -L -o "C1_Shi2024_PositionBias.pdf"            "https://arxiv.org/pdf/2406.07791.pdf"
curl -L -o "C2_Huang2025_DroppingHandful.pdf"       "https://arxiv.org/pdf/2508.11847.pdf"
curl -L -o "C3_Singh2024_LeaderboardIllusion.pdf"   "https://arxiv.org/pdf/2504.20879.pdf"
curl -L -o "C4_Frick2025_PromptToLeaderboard.pdf"   "https://arxiv.org/pdf/2502.14855.pdf"
curl -L -o "C5_Blackwell2024_BenchmarkUncertainty.pdf" "https://arxiv.org/pdf/2410.03492.pdf"

# ============================================================
# D. Classical crowdsourcing (arXiv / open copies only)
# ============================================================
curl -L -o "D2_Raykar2010_LearningFromCrowds.pdf"   "https://jmlr.org/papers/volume11/raykar10a/raykar10a.pdf"
curl -L -o "D3_Whitehill2009_GLAD.pdf"              "https://papers.nips.cc/paper/3644-whose-vote-should-count-more-optimal-integration-of-labels-from-labelers-of-unknown-expertise.pdf" || echo "D3 GLAD PDF: NeurIPS archive URL may have changed; search Google Scholar."

# D1 (Dawid-Skene 1979) and D5 (Bradley-Terry 1952) require JSTOR / Purdue library access.
# D4 (Chen 2013) ACM DL or Microsoft Research:
curl -L -o "D4_Chen2013_PairwiseRanking.pdf"        "https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/wsdm2013.pdf" || echo "D4 URL may have changed; search the title on Google Scholar."

# ============================================================
# E. RLHF / alignment background
# ============================================================
curl -L -o "E1_Ouyang2022_InstructGPT.pdf"          "https://arxiv.org/pdf/2203.02155.pdf"
curl -L -o "E2_Rafailov2023_DPO.pdf"                "https://arxiv.org/pdf/2305.18290.pdf"

echo ""
echo "Download complete. Files in: $(pwd)"
ls -lh | awk 'NR==1 || /\.pdf$/'
