In the context of AI architecture, "models of experts" refers to Mixture of Experts (MoE). This is a design where a large model is split into many smaller, specialized sub-networks (experts) rather than being one single, massive block. 

Internally, an MoE model is "sparse," meaning it only uses a small fraction of its total "brain power" for any given task. While a model might have 1 trillion total parameters, it might only activate 50 billion of them to process a single piece of information, making it faster and more efficient than "dense" models. 

The architecture consists of three core internal components: 
- **Experts**: Independent neural networks (typically Feed-Forward Networks) that specialize in specific types of data, such as math, coding, or linguistic nuances.
- **The Router** (Gating Network): A lightweight "traffic controller" that decides which experts are best suited to handle the incoming data.
- **The Combiner**: A mechanism that takes the specialized outputs from the chosen experts and merges them into a final answer.

##### MoE Information Flow
```
       [ INPUT TOKEN ]

              |
      ________V________
     |                 |
     |  Self-Attention | (Global Context: How words relate)
     |_________________|
              |
      ________V________

     |                 |
     |     ROUTER      | (The Traffic Controller)
     | (Gating Network)| 
     |_________________|
        /     |     \
       /      |      \  <-- Token is sent ONLY to Top-K Experts
      /       |       \      (Others remain inactive/zeroed)
     V        V        V
 [Exp 1]   [Exp 2]  [Exp 8]
 (Math)    (Code)   (Logic)
    \         |        /
     \________|_______/

              |
      ________V________
     |                 |
     |    COMBINER     | (Weighted sum of expert outputs)
     |_________________|
              |
      ________V________

     |                 |
     |  Layer Norm/Res | (Stability & Cleanup)
     |_________________|
              |
       [ NEXT LAYER ]

```


##### Path Summary
1. **Attention**: The token first looks at the surrounding text to understand the general vibe (e.g., "Is this a math problem?").
2. **Routing**: The Router calculates which experts are best for that specific token. In a "Top-2" system, it might pick the Math and Logic experts.
3. **Specialization**: The data passes through those specific experts. If the token is "index," it might go to the Coding expert; if it's "apple," it might go to the Linguistic expert.
4. **Integration**: The Combiner takes the specialized answers, weighs them (e.g., 80% Math Expert, 20% Logic Expert), and passes the result to the next layer in the model.

This is exceptionally important and valuable when running AI on local hardware. 

Next: [Local AI (Thinking)](Local%20AI%20%28Thinking%29.md)
