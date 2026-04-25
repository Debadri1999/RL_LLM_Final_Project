# PDFs folder

This folder holds the downloaded arXiv PDFs for papers cited in the project.

**To populate this folder:** run `../download_papers.sh` from your local terminal (Git Bash, WSL, or any Unix shell). The script uses `curl` to fetch all arXiv PDFs listed in `../bibliography.md`.

Three classical references (Dawid-Skene 1979, Bradley-Terry 1952, Whitehill 2009 GLAD — archive URL may rot) may require alternative sources such as Purdue library, JSTOR, or Google Scholar.

Files expected after successful download:

```
A1_Xu2026_JudgeAwareRanking.pdf
B1_Chiang2024_ChatbotArena.pdf
B2_Zhu2023_JudgeLM.pdf
B3_Gu2024_JudgeSurvey.pdf
C1_Shi2024_PositionBias.pdf
C2_Huang2025_DroppingHandful.pdf
C3_Singh2024_LeaderboardIllusion.pdf
C4_Frick2025_PromptToLeaderboard.pdf
C5_Blackwell2024_BenchmarkUncertainty.pdf
D2_Raykar2010_LearningFromCrowds.pdf
D3_Whitehill2009_GLAD.pdf  (may require manual download)
D4_Chen2013_PairwiseRanking.pdf  (may require manual download)
E1_Ouyang2022_InstructGPT.pdf
E2_Rafailov2023_DPO.pdf
```
