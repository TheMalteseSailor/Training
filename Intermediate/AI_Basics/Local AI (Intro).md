
This section was originally meant to only be a small introduction section to AI as a lead-in for how to develop malware using local AI. However, the demand for understanding how the AI inference process works at a fundamental level was higher than that of the original content. 

This section is not all inclusive, it's not easily digestible, and it's not completely reflective of frontier AI models. What this section is is a springboard for your future research and self-learning. As with anything you self-teach, you should ensure that you integrate this information within your existing contextual understanding. Memorizing factoids is good for tests, but not great for true understanding. 

### Firstly

- What is local AI?
	- This is simply an AI model that you run on your local hardware. It does not mean that it does not interact with external resources, but simply that you're hosting the runtime and model on your locally owned hardware. 

- Why would you bother with Local AI?
	- Do you care about privacy? 
	- Are you doing stuff with AI you don't want to be transmitted to someone else's servers?
	- Do you want to generate content that is not married to some online service?


### Secondly

Online AI services will often provide better out-of-the-box quality than what most people can achieve locally. That is for many reasons. 
	1. hardware limiting factors. 
		1. Your hardware cannot compete with enterprise grade GPUs being managed by engineers that actually know how to tune the models, hardware, and workflow.
		2. You may have a good GPU, but your CPU and RAM are not sufficient to survive any spillage onto the CPU and system RAM.
	2. You have to understand what all the settings mean to obtain optimal performance and response quality.
	3. The models you're using are not even in the same universe with regards to parameter count to the models being ran on enterprise grade GPUs with hundreds of billions of parameters and context windows of 1 million tokens.
	4. Local models often require more prompt massaging to get the response you were looking for. 

Even with all of these downsides there are ways to compensate for this and obtain good quality responses at a good speed. 

First you must determine what are you looking to obtain from using AI in general. If you're simply trying to slap AI onto something that can be done with a python script, you're wrong and you're wasting a lot of time and money. Using AI is expensive and often significantly slower than deterministically executed code. AI shines when you're not able to calculate for each outcome, but you need whatever it is to flow into a set number of code flows you've established. 

	From a non-technical vantage point, you can use AI for many tasks like cleaning up short stories, modifying text to remove repetition or change the vibe, understanding complex processes in subjects like math, engineering, or programming, processing and/or generating images, and much more. 


This doesn't mean that you cannot use AI to generate workflows that you use to structure your hand-written code with. It also doesn't mean that you can't use it to generate unit tests for the code you write. **My main point is that AI shouldn't be doing the thinking for you, it should be supplementing the thinking you're already doing.**


### Lastly 

Where should you go to learn more?
	1. Youtube
		1. Watch videos of how software developers are integrating AI into their workflows or products
		2. Learn from other's mistakes. This includes which hardware to buy, software to run, models to use, etc.
		3. Watch tutorials
			1. Skip the cyber videos and aim at the engineering topics. All of the cool cyber stuff sits on top of the **boring** yet fundamental engineering concepts.
	2. blog posts.
		1. Read through how different people implement their workflows. 
			1. After you understand the basics stick with more programming focused posts. The Graphical Interface of most tools abstracts what's really happening and you become a user.
			2. Understanding why people choose different implementations for different projects.
				1. A GUI interface may be exactly what you need early on, but it also may not scale as hoped for when your project is deployed.
	3. Read company websites
		1. Especially, earlier on in your learning in the higher level topics, many companies will offer basic free information that is extremely well written.
			1. [[Detailed LLM Parameter Guide]]


### Let's get started!

[[Local AI (The Basics)]]