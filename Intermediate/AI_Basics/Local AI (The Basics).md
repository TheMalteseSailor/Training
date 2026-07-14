### Quick Overview

Running a local Large Language Model (LLM) is a complex orchestration of math and memory. Here is the pipeline of how a prompt transforms into a response, step-by-step. 

First, lets cover what an LLM, neural network, and a transformer actually is and some basic components. 

It helps to think of them as a hierarchy. 
	- Neural Networks are the broad Foundation
	- Transformers are the specific blueprint for building the neural networks
	- Large Language Models are the finished products built using those blueprints.

###### 1. Neural Networks:
A neural network is a type of AI modeled loosely after the human brain. Data enters through an input layer, passes through one or more hidden layers where it is transformed, and emerges from an output layer as a prediction

![Pasted image 20260316120240.png](Pasted%20image%2020260316120240.png)
(ganked from the internet)

###### 2. Transformers:
The Transformer is a specialized type of neural network designed to handle sequences of data, such as sentences. The `secret sauce` of transformers is self-attention. This allows the model to look at every word in a sentence at once and decide which other words are most relevant to its meaning. 
Wait?! How can it see all of your tokens at once, but it's only predicting one token at a time?!? Using the self-attention mechanism, every token, in your prompt is relationed to every other token simultaneously. A massive map of relationships is created using every token of your prompt to discern relation between the tokens. An easy example of this is,  "The pig ate the slop because it was a pig." The word "it" refers to the pig, not the slop. This is recognized using this giant mathematical snapshot that captures the context.

###### 3. Large Language Models:
An LLM is a powerful AI application that uses transformer architecture and has been trained on an astronomical amount of text. "**Large**" refers to both the training data and the number of parameters.


#### The Beginning: Your Prompt

1. **The Input: Tokenization & The Context Window**
When you hit enter, your text is broken into Tokens (chunks of characters or words). 
Context Window: The maximum number of tokens the model can "keep in mind" at once (e.g., 8k, 32k, or 128k).

- **Context Overflow**: This occurs when your prompt plus the generated history exceeds the window. The model must then "forget" the earliest parts of the conversation to make room for new data. 

2. **Processing: The Prefill Phase**
The model reads your entire prompt to understand the relationships between words, recall the subject of self-attention just discussed. 

- **CPU Threads**: If you aren't using a dedicated GPU (VRAM), the workload is split across your processor's cores. Optimizing thread count (usually matching your physical core count) ensures the fastest "Time to First Token."
- **KV Cache (Key-Value Cache)**: This is the "short-term memory" of the model. Every word in your current session is converted into a mathematical vector and stored here so the model doesn't have to re-process the entire chat for every new token.

3. **Generation: The Autoregressive Loop**
LLMs predict the next single token based on the ones before it. It assigns a probability score to every word in its vocabulary. To keep the output from being robotic or repetitive, several "samplers" filter these probabilities: 
Temperature: Controls randomness. High temperature (e.g., 1.2) flattens the probabilities, making "wilder" choices more likely. Low temperature (e.g., 0.2) makes the model confident and predictable.

- **Top K Sampling**: The model only considers the top K most likely next words (e.g., top 40) and ignores the rest.

- **Top P Sampling (Nucleus)**: The model looks at the smallest set of words whose cumulative probability adds up to P (e.g., 0.90).

- **Min P Sampling**: A modern alternative that discards tokens with a probability lower than a percentage of the top token's probability (e.g., 0.05). This is often smoother than Top P.
**Repeat Penalty**: Artificially lowers the probability of tokens that have already appeared recently, preventing the model from getting stuck in a loop. 

4. **Acceleration: Speculative Decoding**
To speed things up, some setups use Speculative Decoding. A tiny, fast "draft" model guesses the next few tokens, and the large "oracle" model checks them all at once. If the draft is right, you get 3–5 tokens in the time it usually takes to generate one. 

5. **The Output: Detokenization**
Once a token is selected, it is converted back into human-readable text and streamed to your screen. The loop repeats until the model hits an "End of Sentence" token. 



```
          [ USER PROMPT ]
                 |
      1. TOKENIZATION & CONTEXT CHECK
      (Text -> Tokens | Check for OVERFLOW)
                 |
      2. PREFILL PHASE (Compute-Bound)
      (Uses CPU THREADS/GPU to build KV CACHE)
                 |
                 v
+-------------------------------------------------------+
|  3. THE DECODING LOOP (Autoregressive Generation)     |
+-------------------------------------------------------+
|                                                       |
|  A. LOGIT GENERATION                                  |
|     (Model assigns scores to ~32,000+ words)          |
|                                                       |
|  B. THE SAMPLING REFINERY                             |
|     |-- TEMPERATURE    (Randomness vs. Logic)         |
|     |-- REPEAT PENALTY (Prevents "the the the...")    |
|     |-- TOP K / TOP P  (Culls low-probability junk)   |
|     `-- MIN P          (Scalpels the tail based on %) |
|                                                       |
|  C. TOKEN SELECTION                                   |
|     (The "Winner" is picked from the refined list)    |
|                                                       |
|  D. SPECULATIVE DECODING (Optional)                   |
|     (Fast draft model guesses +3-5 tokens ahead)      |
|                                                       |
+------------------+------------------------------------+
                   |
         (Append token to history)
                   |
        4. STOP CONDITION REACHED?
         /                 \
      [ NO ]             [ YES ]
         |                  |
    (Loop back)       5. DETOKENIZATION
    to Step 3        (Tokens -> Human Text)
                            |
                    [ FINAL RESPONSE ]
```


### Decoding Loop

Key Concepts in the Distribution:
- **Logits**: These are the "raw" numerical values the model spits out before they are turned into percentages.
- **Softmax**: The mathematical function that turns those raw scores into a Probability Distribution that adds up to 100%.
- The "Long Tail": A model might have 32,000+ words in its vocabulary. Most of them (like "potato" in the example above) have near-zero probability. Top-K and Top-P are designed to "cut the tail" so the model doesn't pick a nonsensical word by accident.
- **Temperature (The Shaker)**: It doesn't change which word is #1, but it changes the gap between #1 and #2.
	- High Temp makes the probabilities more equal (chaotic/creative).
	- Low Temp makes the leader much more dominant (boring/logical).
- **Min-P**: This is currently considered the "gold standard" for local LLMs because it scales based on how confident the model is. If the model is 90% sure, Min-P cuts almost everything else. If the model is confused, it keeps more options open.


```
          [ PREVIOUS CONTEXT ] 
        "The quick brown fox..."
                  |
        1. LOGIT GENERATION (Raw Scores)
 [ jumps: 15.2 | leaps: 14.8 | runs: 12.1 | potato: -4.2 ]
                  |
        2. SOFTMAX (Conversion to %)
 [ jumps: 60%  | leaps: 30%  | runs: 8%   | potato: 0.001% ]
                  |
/-----------------V---------------------------------------\
|         3. THE PROBABILITY REFINERY (Samplers)          |
\---------------------------------------------------------/
|                                                         |
| A. TEMPERATURE                                          |
|    - Low (0.1): [ jumps: 98% | leaps: 2%  ] (Sharper)   |
|    - High (1.5): [ jumps: 35% | leaps: 30% ] (Flatter)  |
|                                                         |
| B. TOP-K SAMPLING                                       |
|    - Keep only the top 'K' highest bars; delete rest.   |
|                                                         |
| C. TOP-P (NUCLEUS)                                      |
|    - Keep the top 'X' words that sum up to P%.          |
|                                                         |
| D. MIN-P (Dynamic)                                      |
|    - Delete any word < 5% of the lead word's score.     |
|                                                         |
\-------------------------+-------------------------------/
                          |
                4. STOCHASTIC SELECTION 
          (A random "dice roll" based on the 
           final refined % percentages)
                          |
                [ WINNING TOKEN: "jumps" ]
```


### Quantization 

Quantization is the process of compressing an LLM's "weights" (the trillions of numbers that represent its knowledge) from high-precision decimals into smaller, rounded-off integers.
Most local models are 4-bit or 8-bit, down from the original 16-bit (FP16). This allows a 70B model that originally required 140GB of VRAM to fit into 40GB with minimal loss in "intelligence".

#### The Quantization "Shrink-Wrap"
```
      [ 16-BIT (FP16) ]                 [ 4-BIT (GGUF/EXL2) ]
      (The Original)                    (The Compressed)
      +---------------+                 +---------------+
      |  3.14159265   |                 |      3.1      |
      | -0.00234812   |                 |     -0.0      |
      |  0.98765432   |  == SHRINK ==>  |      1.0      |
      |  1.55678901   |                 |      1.6      |
      +---------------+                 +---------------+
      [ SIZE: 100GB ]                   [ SIZE: 25GB ]
      [ RAM: HUGE ]                     [ RAM: SMALL ]
```

#### How It Works (The Math)
- **Weight Reduction**: Think of it like resizing a 4K image to 1080p. You lose some fine detail, but the picture is still perfectly recognizable.
- **The "Grid" (Scaling)**: To keep the model smart, we don't just round numbers. We find the Min/Max of a group of numbers (a "block") and create a small scale to map them to the 4-bit range (0 to 15).
- **Inference Speed**: Because the model is smaller, your GPU can "read" the entire brain much faster. This increases your Tokens Per Second (TPS) significantly.

#### LMStudio Model Configuration


![Pasted image 20260313201541.png](Pasted%20image%2020260313201541.png)

Next: [Local AI (Experts)](Local%20AI%20%28Experts%29.md)

