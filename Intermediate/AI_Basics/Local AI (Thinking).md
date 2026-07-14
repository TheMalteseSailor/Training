
"Thinking" models (like OpenAI’s o1 or DeepSeek R1) add a reasoning loop on top of the standard inference pipeline. Instead of going straight from prompt to answer, they generate a hidden Chain of Thought (CoT), checking their own work as they go.

#### The "Thinking" Inference Pipeline
```
       [ USER PROMPT ]
              |
      1. TOKENIZATION & PREFILL
      (Builds initial KV CACHE)
              |
              v
+------------------------------------------+
|  2. THE REASONING LOOP (Test-Time)       | <----------+
+------------------------------------------+            |
|                                          |            |
|  A. LOGIT GEN (Thinking Tokens)          |            |
|     (Predicts logic, not the answer)     |            |
|                                          |            |
|  B. THE SAMPLING REFINERY                |      [ RECURSION ]
|     (Temp / Top-P / Min-P filters)       |     (The model reads
|                                          |      its own thoughts
|  C. THE INNER MONOLOGUE                  |      to decide the
|     |-- DECOMPOSITION (Task breakdown)   |      next logical
|     |-- SIMULATION    (Testing ideas)    |      inference)
|     |-- VERIFICATION  (Self-checking)    |            |
|     `-- PIVOTING      (Fixing errors)    |            |
|                                          |            |
|  D. STOP CHECK (Reasoning Complete?)     |            |
|     |-- [ NO ]  -------------------------+------------+
|     `-- [ YES ] (Reaches "End of Thought" token)
|                                          |
+------------------+-----------------------+
                   |
                   v
+------------------------------------------+
|  3. FINAL ANSWER GENERATION              |
+------------------------------------------+
|                                          |
|  The model uses the "Thinking History"   |
|  to produce a concise final response.    |
|                                          |
+------------------+-----------------------+
                   |
          4. DETOKENIZATION
          (Tokens -> Human Text)
                   |
           [ FINAL RESPONSE ]
```


In reasoning models (like o1 or DeepSeek-R1), the "inner monologue" isn't just a separate text block; it is an emergent behavior driven by a shift in how the model uses its context window to solve problems. 

1. **The "Think" Loop Mechanism**
Instead of predicting the final answer immediately, the model is trained to generate a sequence of reasoning tokens first. 

**Sequential Dependency**: Each word in the inner monologue becomes part of the KV Cache (the model's short-term memory). The model "reads" its own previous thoughts to decide the next step, much like a human writing on a scratchpad.
Test-Time Compute: By generating more tokens before reaching the final answer, the model effectively spends more "computational effort" on the problem. Accuracy scales with the number of these thinking tokens. 

2. **How the Monologue is Trained (RL vs. SFT)**
The "voice" in the monologue comes from two distinct training styles:
- **Supervised Fine-Tuning (SFT)**: The model is fed thousands of examples of "correct" thinking patterns (e.g., "First, I will define X... then I will calculate Y").
- **Reinforcement Learning (RL)**: Models like DeepSeek-R1-Zero were trained without examples. Instead, they were given rewards for correct answers and correct formatting. Over thousands of iterations, complex behaviors like self-correction and backtracking (e.g., "Wait, that doesn't seem right, let me try another way") appeared spontaneously. 

2. **Anatomical Breakdown of a Thought**
A typical inner monologue follows a structured cognitive flow often guided by System Prompts or RL Incentives: 

```
+---------------+-------------------------------------+----------------------------
|     STAGE     |       WHAT HAPPENS INTERNALLY       |    KEY INDICATOR TOKENS    
+---------------+-------------------------------------+----------------------------
| DECOMPOSITION | Breaks the prompt into smaller,     | "Let's break this down..." 
|               | solvable sub-tasks.                 | "First, I'll identify..."  
+---------------+-------------------------------------+----------------------------
|  SIMULATION   | Tests a hypothesis or a potential   | "If I assume X, then Y..." 
|               | path of reasoning.                  | "Suppose we try..."        
+---------------+-------------------------------------+----------------------------
| VERIFICATION  | Checks intermediate steps for logic | "Checking my work..."     
|               | or math errors.                     | "Does this hold true?"     
+---------------+-------------------------------------+----------------------------
|   PIVOTING    | Abandons a failed strategy to try   | "Actually, that's wrong..."
|               | a new approach.                     | "Wait, let me restart..."
+---------------+-------------------------------------+----------------------------
|  CONVERGENCE  | Summarizes the findings into the    | "Therefore, the answer..." 
|               | final visible response.             | "In conclusion..."         
+---------------+-------------------------------------+----------------------------
```

4. **Technical Integration**
- **Hidden Tokens**: In many APIs (like OpenAI's o1), these tokens are generated, billed, and stored in the context window, but they are discarded or hidden from the final user output to keep the interface clean. On local models, you can watch the thinking as it's occurring. 
- **Context Pressure**: Because the monologue can be thousands of tokens long, "thinking" models require significantly larger Context Windows to avoid Context Overflow before they even reach the final answer. 


**Example of thinking loop displayed**
![[Pasted image 20260303200427.png]]

Next: [[Local AI (Hardware Limiting)]]
