
When you hit "Build" or run a command like cl.exe (MSVC) or gcc (MinGW) on Windows, your human-readable C code undergoes a four-stage transformation to become a machine-readable .exe.

1. Preprocessing
	The preprocessor handles lines starting with #. It doesn't understand C logic; it just performs text manipulation. 
	Header Inclusion: Replaces #include <stdio.h> with the actual content of that file.
	Macro Expansion: Replaces constants (e.g., #define PI 3.14) with their values.
	Result: A massive "Translation Unit" (pure C code). 

2. Compilation
	The compiler takes the preprocessed code and translates it into Assembly language specific to your processor architecture (like x86 or x64). 
	It checks for syntax errors.
	It optimizes the code for performance.
	Result: Assembly code files. 

3. Assembly
	The Assembler converts the assembly code into Machine Code (binary 1s and 0s). 
	These are stored in Object Files (usually ending in .obj on Windows).
	The Catch: These files aren't runnable yet because they contain "holes" where external functions (like printf) are supposed to be. 

4. Linking
	This is the final step where the Linker (e.g., link.exe) stitches everything together. 
	Resolution: It looks at the "holes" in your .obj files and finds the actual addresses of the functions in Windows libraries (like msvcrt.lib).
	Merging: It combines your object files and any static libraries into a single file.
	Result: The final Executable (.exe). 

Visual Summary
``` text
------------------------------------------------------------------
Stage 	        Input	          Tool	         Output
-------------------------------------------------------------------
Preprocessing	.c source	      Preprocessor	 Expanded source
-------------------------------------------------------------------
Compilation	    Expanded source	  Compiler	     Assembly code
-------------------------------------------------------------------
Assembly	    Assembly code	  Assembler	     .obj (Object file)
-------------------------------------------------------------------
Linking	        .obj + Libraries  Linker	     .exe (Executable)
-------------------------------------------------------------------
```