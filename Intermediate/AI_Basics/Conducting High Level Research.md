You can choose to start your research from several vantage points. I recommend attempting to obtain a certain minimal level of contextual information surrounding the targeted piece of software.

Before executing/detonating the binary(ies) or diving head first into static analysis start by obtaining some of the following details:
 1. Type of binary including architecture 
	 1. x86, x86_64, PPC, ARM, ARM64
 2. Any programmatic security or obfuscation features. 
	 1. ex. self-extracting, embedded loaders
 3. Any compile-time security features that are either compiled in or not. 
	 1. ex. ASLR, SafeSEH, etc.
 4. Any post-compilation security or obfuscation. 
	 1. ex. Packing, emulation (themida, vmprotect), etc.
5. External dependencies
	1. DLLs, configuration files, registry keys, external systems/services, etc.
6. Try to identify any encrypted segments
	1. This can either be whole segments that are unintelligible or static/constant chunks within the binary that are referenced by a stager, loader, decrypter, or deobfuscator. 


Once you ascertain some of the context of the binary(ies) start attempting to identifying:
1. startup methods
	1. entrypoint, ordinals, exports
	2. obscured alternate start paths:
		1. env variables, command-line arguments, system configurations, etc.
2. methods of system interaction
	1. How it interacts with the system or its components
		1. malware functionality
	2. If it interacts with a management server or staging server
		1. network/remote interaction methods
3. anti-debugging / counter-reverse engineering code
	1. TLS - Thread local Storage: pre-thread execution execution
	2. execution timer: The binary sets a timer for function execution and if longer than a predetermined/hardcoded time, it indicates a debugger has placed a breakpoint within the function and slowed down execution.
	3. debugger attach check in PEB:
	4. debugger running on system at startup, 
	5. environment ID'ing 
	6. Anti-AV technique: attempt to detect emulated execution by executing an obscure processor instruction that an emulated environment wouldn't implement.


Before you execute or detonate the binary:
1. get procmon configured and running
	1. configure more wide open filters, but ensure that erroneous system activities are not flooding the log window.
2. configure and set Wireshark to capture
3. if possible, start debugger and prepare to load binary
4. take a snapshot of the VM you're running

