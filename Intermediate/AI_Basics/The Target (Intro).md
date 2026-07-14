Welcome to the Reverse Engineering (RE) Component of this training. 

This section is meant to be compressed and may be a bit confusing to those who have little or no experience. However, you need to ask questions. People who know can recognize when you're faking it. So embrace whatever stage of learning you're at and never stop asking questions and learning.

This section is not a complete encapsulation of the methodology, but a framework designed to help you build a scaffolding that will expedite the development of your own methodology. 

What do I mean by a methodology? What does that term mean? 
``` 
Methodology is the systematic, theoretical analysis of the methods and principles associated with a branch of knowledge, serving as the strategic framework for research, business, or education. It justifies the choice of specific methods (e.g., surveys, experiments) to ensure research validity, reproducibility, and alignment with project goals
	- Merriam-Webster
```

That definition clearly states what I mean and what you need to develop in your endeavor to continually find critical vulnerabilities. 

### Monologue 

Why is it important to develop a methodology and not simply a suite of tools and walkthroughs? 
Using a haphazard method of research may net a few bugs, but maintaining a continual flow of discovery will hinge on the fact that you adhere to the components of your system that have netted success in the past. You should have a basic flow of research, of which we will discuss later, that leads into potential bug identification, and further research.

When you make a discovery, annotate how you discovered it. Keep an understanding of what was your mindset when you chose to look where you did and why you came to a specific decision at key points that resulted in your progression. Success is not limited to bug identification, but extends to any skill or experience that refines your ability to research, detect, and exploit a binary. 

If you don't know how something works, research it and write a small narrative for yourself on how the target binary or software interacts with that specific topic. At first it's going to be a flood of unknowns, but over time you will prune away those unknowns and recognize what you can breeze by and what you need to stop and look at. As you will see in this training, you should understand the target functionality at a level where you can at least partially implement it in your test harness. it may also be extremely wise to display data in different forms, ie. hex, bytearray, big endian, little endian, ascii, etc. Over time you will learn to recognize data that is in a different form. 

In this training you will see what I'm calling a "test harness". This is my either whole or partial implementation of the functionality in the client, server, or both. You will gain immense insight into protocols, encryption, data structuring, and more due to the fact that you will have implemented components of it. Once you're able to get the targeted software to accept your data as legitimate 'enough' to be accepted as valid communications from a client, you can begin to really dive deep into the Vulnerability Research (VR).

Why do I choose to pattern my work like this?
1. My hypothesis is either validated or invalidated by live testing of the data against the target.
2. As my understanding of the target increases so does the refinement of my active testing can progress. 
3. I am positioned to target both binary and logical exploits with my continually refined test harness. 
4. I have exceptionally granular control over my testing and the ability to bootstrap interaction components, making testing extremely fast. 
5. As my test harness increases in functional sophistication along with my understanding, I can reach extremely deep into the target's code and potentially target vulnerabilities in functionality rather distant from my initial access vector. 



### Before getting started

What is a **memory bug** vs a **logic bug**? 

A memory bug or binary exploit targets a failure in the target binary to properly perform memory bounds checking and/or input validations on data provided from a source outside of the binary.
	These types of bugs are synonymous with exploitation, stack overflow, heap overflow, use-after-free, etc. However, on modern systems and with languages that have a managed memory construct, they're less harder exploit due to the likely need for a multi-bug chain.

A logic bug is a bug or failure in the logic of a target software that allows an attacker to abuse legitimate functionality to obtain a malicious outcome. This can be caused by poor API segmentation, failure to validate data after first check, poor permissions implementation, etc.
	These types of bugs are usually harder to find and may potentially require more time and understanding to identify. This is because you have to understanding the various components, their functionality, and their behavior. Once you understand how the features are designed to be used you can determine if they can be used against the target in an illegitimate way. 


Most start their journey looking for memory bugs and quickly drown in ocean of subjects they must be proficient in, skills they need to master, and the never ending tools designed to make things "easier". Just realize that there is no "easy" way through this process. You must pay your dues to yourself to see any return on investment. No tool, script, class, or tutorial will usher you to a life of passive success. Only through your frustration and overcoming will you attain your goals. 


Next: [The Target (White box)](The%20Target%20%28White%20box%29.md)
