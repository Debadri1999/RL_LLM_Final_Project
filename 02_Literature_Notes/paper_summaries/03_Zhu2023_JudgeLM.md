# Zhu, Wang, Wang (2023) — JudgeLM

**Full title:** *JudgeLM: Fine-tuned Large Language Models are Scalable Judges*
**arXiv:** 2310.17631
**URL:** https://arxiv.org/abs/2310.17631
**Role in our project:** Background foundational paper (required per course brief). Establishes LLM-as-a-Judge as a legitimate evaluator class.

---

## Problem

Human evaluation of open-ended LLM outputs is expensive and slow. Automated evaluation is desirable but prior judge models (GPT-4 prompting, NLG metrics) suffer from biases and inconsistency.

## Methodology

- Fine-tune open-source LLMs (7B, 13B, 33B) on a curated dataset of (task, LLM-generated answers, GPT-4 judgment) triples.
- Training data augmentation to combat known biases:
  - **Swap augmentation** (position bias)
  - **Reference support** (knowledge bias)
  - **Reference drop** (format bias)

## Key findings

- JudgeLM-7B achieves >90% agreement with GPT-4 judgments — exceeding human-to-human agreement.
- Scales to 5K samples in ~3 min on 8 A100 GPUs.
- Three-bias taxonomy: position, knowledge, format.

## Relevance to our project

1. Establishes that LLM judges have structured, identifiable biases. This motivates modeling judge noise rather than treating judges as interchangeable.
2. The three-bias taxonomy (position, knowledge, format) is a direct antecedent to our "pair-heterogeneous noise depends on what's being judged" claim — prompt category affects which biases dominate.
3. Potential usage in our project: we could *use* a small fine-tuned judge model (or API-based judge) to validate our prompt-category heterogeneity hypothesis on arena prompts.

## What they don't do

- No statistical model of judge noise (they treat bias as something to *remove* rather than to *model*).
- No Bradley-Terry framework.
- No uncertainty quantification for the resulting scores.
