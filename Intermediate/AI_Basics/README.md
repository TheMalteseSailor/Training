- Primers
	- [Encryption (Primers)](Encryption%20%28Primers%29.md)
		- [RC4](RC4.md)
		- [Salsa20](Salsa20.md)
		- [AES](AES.md)
		- [Network Encryption](Network%20Encryption.md)
	- [Building A Binary (Primer)](Building%20A%20Binary%20%28Primer%29.md)
- Chapter 1: AI Fundamentals
	- [Local AI (Intro)](Local%20AI%20%28Intro%29.md)
	- [Local AI (The Basics)](Local%20AI%20%28The%20Basics%29.md)
	- [Local AI (Experts)](Local%20AI%20%28Experts%29.md)
	- [Local AI (Thinking)](Local%20AI%20%28Thinking%29.md)
	- [Local AI (Hardware Limiting)](Local%20AI%20%28Hardware%20Limiting%29.md)
	- [Writing Basic Malware with Local AI](Writing%20Basic%20Malware%20with%20Local%20AI.md)
		- [Detailed LLM Parameter Guide](Detailed%20LLM%20Parameter%20Guide.md)
- Chapter 2: RE Workflow Fundamentals
	- [The Target (Setup)](The%20Target%20%28Setup%29.md)
	- [The Target (Intro)](The%20Target%20%28Intro%29.md)
	- [The Target (White box)](The%20Target%20%28White%20box%29.md)
	- [The Target (Black box)](The%20Target%20%28Black%20box%29.md)
- Chapter 3: TBD

I am **TheMalteseSailor** and welcome to this basic software reverse engineering and vulnerability research introductory training. This is not designed to be an all inclusive course, but a basic introduction to the concepts, workflows, and thought processes surrounding the process of finding software bugs and determining if they are exploitable. 

This training contains several primers that are partially required for the training, but will largely enhance your understanding of the topic when you go to implement the information yourself. The only real primer you need to read through is the RC4 encryption primer. It is not a deal breaker if you don't, but you might not understand some elements later in the training.

#### What this training is
This training is meant as a high-speed flyby of some fundamentals. With some good foundational knowledge that you can build on as well as some pro-tips discovered from hours of suffering. 
#### What this training isn't
This isn't a zero-to-hero deep-dive that will have you developing purely agentic workflows that will 10x your productivity to the moon overnight. It also isn't a deep-dive into Software Reverse Engineering. However, this information has been proven to be extremely valuable to me functionally and for other's I've already passed this information on to.
#### What you should expect
Though this training is foundational it is not going to be easy or shallow. We will be strategically diving down into topics that will help you actually understand the technology you're using and give you a knowledge set you can build on. 

#### Requirements
For the Local AI portion:
1. Your brain.
2. Maybe caffeine

For the Reverse Engineering portion you'll need to download:
1. Ghidra - Download releases from the ghidra github repository only.
2. JDK - use the link in the ghidra README.md install instructions.
3. Pyghidra --  If you want to run python scripts or run a headless ghidra session from a python script.
