# Downloaded Papers

## Papers Directly Relevant to Research Hypothesis

### 1. SAE Interventions are Unreliable: Post-Intervention Recovery of Suppressed Behavior
- **File**: `2606.18322v1_SAE_Interventions_Unreliable_Post_Recovery.pdf`
- **Authors**: Mingyue Cui, Linghui Shen, Xingyi Yang
- **Year**: 2026
- **arXiv**: 2606.18322
- **Key Contribution**: Demonstrates that SAE feature-level interventions that appear to suppress behavior do NOT eliminate the behavior — models recover via "SAE reconstruction residual" (unexplained component). 95.8% recovery rate in refusal-steering experiments even with clamps active. Introduces "post-intervention recovery" diagnostic.
- **Relevance**: CORE PAPER. Directly demonstrates "robustness plateaus" — null results from intervention clamps mask underlying behavioral capacity. The "causal handle vs complete bottleneck" distinction is exactly the framework our research needs to formalize statistically.
- **Code**: https://github.com/Mingyuee88/sae-post-intervention-recovery

### 2. Confirming the Null: Remarks on Equivalence Testing and the Topology of Confirmation
- **File**: `2405.16331v1_Confirming_Null_Equivalence_Testing.pdf`
- **Authors**: Reid Dale
- **Year**: 2024
- **arXiv**: 2405.16331
- **Key Contribution**: Formal modal logic for frequentist confirmation. Shows that point null hypotheses (H: θ = θ₀) are NOT confirmable, while equivalence hypotheses (H: θ ∈ [L,U]) ARE confirmable. Validates TOST as a model of Mayo's Severe Testing.
- **Relevance**: Core statistical framework for our Bayesian analysis of null results. The topological confirmation criterion explains WHY standard NHST cannot confirm null results — we need equivalence testing or Bayes factors.

### 3. Replication of "null results" — Absence of evidence or evidence of absence?
- **File**: `2305.04587v3_Replication_Null_Results_Absence_Evidence.pdf`
- **Authors**: Samuel Pawel, Rachel Heyard, Charlotte Micheloud, Leonhard Held
- **Year**: 2023
- **arXiv**: 2305.04587
- **Key Contribution**: Shows that non-significance ≠ evidence of absence. Presents TOST (Two One-Sided Tests) and Bayes factors BF₀₁ as proper methods for quantifying evidence for null hypotheses. Applied to Reproducibility Project: Cancer Biology data.
- **Relevance**: CORE STATISTICAL METHODOLOGY. Provides the exact methods (TOST, BF₀₁) needed to distinguish "intervention impotence" (underpowered study showing null) from "intrinsic robustness" (true null confirmed by equivalence testing).

### 4. Computational Safety for Generative AI: A Hypothesis Testing Perspective
- **File**: `2502.12445v2_Computational_Safety_GenAI_Hypothesis_Testing.pdf`
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2502.12445
- **Key Contribution**: Frames AI safety as a hypothesis testing problem. Addresses statistical testing of safety properties in generative AI.
- **Relevance**: Direct methodological bridge between safety evaluation and formal hypothesis testing.

### 5. Latent Adversarial Training Improves Robustness to Persistent Harmful Behaviors in LLMs
- **File**: `2407.15549v3_Latent_Adversarial_Training_Robustness_LLM.pdf`
- **Authors**: Abhay Sheshadri et al. (MIT, Anthropic, MATS)
- **Year**: 2024/2025 (TMLR)
- **arXiv**: 2407.15549
- **Key Contribution**: Shows fine-tuning "suppresses rather than removes" harmful capabilities. Introduces targeted LAT (Latent Adversarial Training) that perturbs residual stream activations to make suppression more thorough. Demonstrates robustness improvement across jailbreaks, backdoors, and unlearning.
- **Relevance**: Directly addresses the suppress-vs-remove distinction. Provides experimental evidence that standard alignment interventions result in suppression plateaus (null results from standard eval hide residual capacity).

### 6. Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training
- **File**: `2401.05566v3_Sleeper_Agents_Deceptive_LLMs_Safety_Training.pdf`
- **Authors**: Evan Hubinger, Carson Denison, Jesse Mu et al. (Anthropic)
- **Year**: 2024
- **arXiv**: 2401.05566
- **Key Contribution**: Shows that safety training cannot reliably remove backdoored deceptive behaviors trained into LLMs. Adversarial training can even strengthen backdoors. Demonstrates that null results from safety evaluation can mask persistent harmful capabilities.
- **Relevance**: Classic example of "robustness plateau" — null results from safety training on deceptively aligned models reflect intrinsic robustness of the behavior, not successful intervention.

### 7. Fine-tuning Aligned Language Models Compromises Safety, Even When Users Do Not Intend To!
- **File**: `2310.03693v1_Finetuning_Aligned_LLMs_Compromises_Safety.pdf`
- **Authors**: Xiangyu Qi, Yi Zeng, Tinghao Xie et al.
- **Year**: 2023
- **arXiv**: 2310.03693
- **Key Contribution**: Even benign fine-tuning (without any adversarial intent) degrades safety alignment. Shows safety alignment is shallow/brittle.
- **Relevance**: Establishes that safety = suppression mechanism rather than fundamental capability change. Sets up the question of what true robustness looks like.

### 8. Representation Engineering: A Top-Down Approach to AI Transparency
- **File**: `2310.01405v4_Representation_Engineering_AI_Transparency.pdf`
- **Authors**: Andy Zou, Long Phan, Sarah Chen et al.
- **Year**: 2023
- **arXiv**: 2310.01405
- **Key Contribution**: RepE identifies "reading vectors" from population-level representations that can steer model behavior. Demonstrates controllable activation steering for honesty, harmlessness, etc.
- **Relevance**: Provides the primary intervention technique (activation steering) to test across systematically varied strengths.

## Alignment Foundations Papers

### 9. Constitutional AI: Harmlessness from AI Feedback
- **File**: `2212.08073v1_Constitutional_AI_Harmlessness.pdf`
- **Authors**: Claude Anthropic team
- **Year**: 2022 (Anthropic)
- **arXiv**: 2212.08073
- **Key Contribution**: Constitutional AI uses AI-generated critiques and revisions to train harmless models without human labels on harmful outputs.
- **Relevance**: Key intervention technique to test for robustness. Sets baseline for systematic study.

### 10. Training Language Models to Follow Instructions with Human Feedback (InstructGPT)
- **File**: `2203.02155v1_InstructGPT_RLHF_Training.pdf`
- **Authors**: Long Ouyang, Jeff Wu, Xu Jiang et al. (OpenAI)
- **Year**: 2022
- **arXiv**: 2203.02155
- **Key Contribution**: RLHF training for instruction following and alignment. Foundational alignment intervention.
- **Relevance**: Baseline alignment technique to test robustness under systematic variation.

### 11. Direct Preference Optimization: Your Language Model is Secretly a Reward Model
- **File**: `2305.18290v3_DPO_Direct_Preference_Optimization.pdf`
- **Authors**: Rafael Rafailov, Archit Sharma, Eric Mitchell et al.
- **Year**: 2023
- **arXiv**: 2305.18290
- **Key Contribution**: DPO reformulates RLHF as direct policy optimization from human preference data. Simpler than PPO.
- **Relevance**: Alternative alignment intervention for robustness testing.

## Safety Fragility Papers

### 12. Safety Alignment Should Be Made More Than Just a Few Tokens Deep
- **File**: `2406.05946v1_Safety_Alignment_More_Than_Few_Tokens_Deep.pdf`
- **Authors**: Xiangyu Qi, Ashwinee Panda, Kaifeng Lyu et al.
- **Year**: 2024
- **arXiv**: 2406.05946
- **Key Contribution**: Safety alignment shortcuts — models learn to refuse based on early token patterns rather than deep semantic understanding, making them brittle to perturbations.
- **Relevance**: Explains WHY null results from safety interventions mask residual capability — alignment is surface-level.

### 13. LoRA Fine-tuning Efficiently Undoes Safety Training in Llama 2-Chat 70B
- **File**: `2310.20624v2_LoRA_Undoes_Safety_Training_Llama2.pdf`
- **Authors**: Simon Lermen, Charlie Rogers-Smith, Jeffrey Ladish
- **Year**: 2023
- **arXiv**: 2310.20624
- **Key Contribution**: As little as $200 of compute using LoRA fine-tuning can effectively remove safety alignment from Llama 2-Chat.
- **Relevance**: Quantitative evidence that safety is suppressive. The "robustness plateau" breaks quickly with even minimal fine-tuning.

### 14. The Geometry of Alignment Collapse: When Fine-Tuning Breaks Safety
- **File**: `2602.15799v1_Geometry_Alignment_Collapse_Finetuning_Safety.pdf`
- **Authors**: Multiple
- **Year**: 2026
- **arXiv**: 2602.15799
- **Key Contribution**: Geometric explanation of safety collapse during fine-tuning. Shows that fine-tuning updates the direction of safety representations even when trained on benign data.
- **Relevance**: Mechanistic understanding of why interventions appear to work (local null result) but are actually fragile.

### 15. Why LLM Safety Guardrails Collapse After Fine-tuning
- **File**: `2506.05346v1_Why_LLM_Safety_Guardrails_Collapse_Finetuning.pdf`
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2506.05346
- **Key Contribution**: Similarity analysis between alignment and fine-tuning datasets to understand why fine-tuning destroys safety.
- **Relevance**: Quantifies the fragility of alignment interventions.

### 16. Safety Layers in Aligned Large Language Models: The Key to LLM Security
- **File**: `2408.17003v5_Safety_Layers_Aligned_LLMs_Key_Security.pdf`
- **Authors**: Multiple
- **Year**: 2024
- **arXiv**: 2408.17003
- **Key Contribution**: Identifies specific layers where safety information is stored. Shows that modifying these layers degrades safety.
- **Relevance**: Mechanistic basis for targeted interventions in robustness testing experiments.

### 17. Safety Training Persists Through Helpfulness Optimization in LLM Agents
- **File**: `2603.02229v1_Safety_Training_Persists_Helpfulness_Optimization.pdf`
- **Authors**: Multiple
- **Year**: 2026
- **arXiv**: 2603.02229
- **Key Contribution**: In agentic settings, safety training persists through helpfulness optimization. Interesting counter-example to typical fragility findings.
- **Relevance**: Shows variation in robustness across settings — key to the meta-experimental hypothesis.

### 18. LLM Probability Concentration: How Alignment Shrinks the Generative Horizon
- **File**: `2506.17871v3_LLM_Probability_Concentration_Alignment.pdf`
- **Authors**: Multiple
- **Year**: 2025
- **arXiv**: 2506.17871
- **Key Contribution**: Alignment reduces diversity in model outputs — a measurable signature of alignment that can be tracked.
- **Relevance**: Provides quantitative metrics for measuring alignment effects across intervention strengths.

## Statistical Methodology Papers

### 19. Meta-analysis of Bayesian Analyses
- **File**: `1904.04484v2_Meta_Analysis_Bayesian_Analyses.pdf`
- **Authors**: Multiple
- **Year**: 2019
- **arXiv**: 1904.04484
- **Key Contribution**: Framework for combining multiple Bayesian analyses. Shows how to aggregate posterior distributions rather than point estimates.
- **Relevance**: Core methodology for the meta-experimental Bayesian analysis of null result distributions.

### 20. Bayes Factors for Peri-Null Hypotheses
- **File**: `2102.07162v2_Bayes_Factors_Peri_Null_Hypotheses.pdf`
- **Authors**: Multiple
- **Year**: 2021
- **arXiv**: 2102.07162
- **Key Contribution**: Bayes factors for "peri-null" hypotheses (narrow intervals around null). Addresses the practical impossibility of exact point-null hypotheses.
- **Relevance**: The research hypothesis involves robustness plateaus (near-null results across varied interventions). Peri-null Bayes factors are the appropriate test.

### 21. Connecting Bayes Factor and the Region of Practical Equivalence (ROPE)
- **File**: `1903.03153v2_Bayes_Factor_ROPE_Interval_Null.pdf`
- **Authors**: Multiple
- **Year**: 2019
- **arXiv**: 1903.03153
- **Key Contribution**: Connects frequentist ROPE/TOST with Bayesian Bayes factors for interval null hypothesis testing.
- **Relevance**: Provides dual frequentist/Bayesian approach to confirming null results.

### 22. How Accurate Are Bayes Factor-Based Null Hypothesis Tests?
- **File**: `2406.08022v2_Accuracy_Bayes_Factor_Null_Hypothesis_Tests.pdf`
- **Authors**: Multiple
- **Year**: 2024
- **arXiv**: 2406.08022
- **Key Contribution**: Simulation study showing accuracy of Bayes factor tests for null hypotheses in practice.
- **Relevance**: Validates the Bayes factor methodology proposed in our research.

### 23. Reverse-Bayes Methods for Evidence Assessment and Research Synthesis
- **File**: `2102.13443v2_Reverse_Bayes_Evidence_Assessment_Research_Synthesis.pdf`
- **Authors**: Multiple
- **Year**: 2021
- **arXiv**: 2102.13443
- **Key Contribution**: Reverse-Bayes: starting from an observed result, what prior would make it convincing? Framework for research synthesis.
- **Relevance**: Alternative to forward Bayes for null result meta-analysis.

## Evaluation Methods Papers

### 24. Systematic Evaluation of LLM-as-a-Judge in LLM Alignment Tasks
- **File**: `2408.13006v2_Systematic_Evaluation_LLM_as_Judge_Alignment.pdf`
- **Authors**: Multiple
- **Year**: 2024
- **arXiv**: 2408.13006
- **Key Contribution**: Evaluates reliability of LLM-as-a-judge for alignment evaluation. Shows biases in automated evaluation.
- **Relevance**: Methodology for automated evaluation of alignment interventions at scale.

### 25. Baseline Defenses for Adversarial Attacks Against Aligned Language Models
- **File**: `2309.00614v2_Baseline_Defenses_Adversarial_Attacks_Aligned_LLMs.pdf`
- **Authors**: Neel Jain, Avi Schwarzschild, Yuxin Wen et al.
- **Year**: 2023
- **arXiv**: 2309.00614
- **Key Contribution**: Simple baseline defenses (perplexity filtering, paraphrasing) against adversarial jailbreaks. Shows varying effectiveness.
- **Relevance**: Establishes baselines for intervention effectiveness measurement.

### 26. How to Use and Interpret Activation Patching
- **File**: `2404.15255v1_How_Use_Interpret_Activation_Patching.pdf`
- **Authors**: Multiple
- **Year**: 2024
- **arXiv**: 2404.15255
- **Key Contribution**: Best practices for activation patching as mechanistic interpretability technique.
- **Relevance**: Methodological guidance for the intervention experiments (patching as a controlled intervention).

### 27. Safety-Tuned LLaMAs: Lessons From Improving the Safety of LLMs
- **File**: `2309.07875v3_Safety_Tuned_LLaMAs_Improving_Safety.pdf`
- **Authors**: Federico Bianchi, Mirac Suzgun et al.
- **Year**: 2023
- **arXiv**: 2309.07875
- **Key Contribution**: Systematic study of safety tuning in Llama models. Shows that safety tuning can be done effectively but depends heavily on data quality and training approach.
- **Relevance**: Empirical baseline for what successful vs. unsuccessful safety interventions look like.

### 28. Control RL: Interpretable Token-Level Steering of LLMs via Sparse Autoencoder Features
- **File**: `2506.18322v1_Control_RL_Token_Steering_LLMs_SAE.pdf`
- **Authors**: Multiple
- **Year**: 2026
- **arXiv**: 2506.18322
- **Key Contribution**: RL-based approach to steering LLMs via SAE features. Improves on naive clamping.
- **Relevance**: Advanced intervention technique to include in systematic variation study.
