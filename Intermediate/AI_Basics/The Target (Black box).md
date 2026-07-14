
Back: [[The Target (White box)]]

Though you're likely coming from the White box code, we're going to temporarily forget that for a short period and take a look at what the server.exe binary looks like in ghidra. 

When you compile a binary, you can make it a Debug or Release build. A debug build will posses a massive amount of additional data to assist you in debugging issues in a development or prerelease environment. Bug hunting on a debug build makes like significantly easier. In a Release build, all of that additional context is removed and the compilers optimizer will likely restructure your code to increase execution efficiency without modifying the actual code functionality. 

This may seem inconsequential, but it could mean that multiple functions are compressed into a single inline function in the final binary, exposing data and context that didn't exist in your source code. In the debug build below you this will not be the case as this build is meant to simplify debugging not be released to production. However, it's easier to track the logic and ghidra does a better job at the decompilation. 

#### ============================
#### Pause for some basic Ghidra familiarization 
#### ============================


The first thing you need to do when you get a binary into ghidra is to ensure you've gotten the correct architecture and your best guess at the compiler. This will help the ghdira decompiler and analysis functionality to output the best results. 

#### Locate Main

The first thing I do when I am looking at a binary for the first time is to determine the main function or entry point, ie. main, entry, WINMAIN, DLLMAIN, etc. This includes any functions that are seen in procmon being called like in the event of a DLL having specific exports/ordinals called by another program. This can also be seen if the binary is imported by another binary and the function is seen being called. 

![[Pasted image 20260228205557.png]]

In this window you can see that I've located main. Since this is the Debug build, all of the function symbols (names) are present along with source file line annotations. You can see that the variable types in the decompilation window are descriptive and not what you'd normally see ie. int, char, undefined0. 

Make your way through some of the basics of the startup process for the server and try to get a basic understanding of how the server handles client callbacks.


#### Locate socket handlers

It is extremely easy to get lost down rabbit holes during this part of the analysis. This is because the handler logic can be extremely complex and number of supported communications protocols can be numerous. If you're lucky the data structure will be relatively basic, but for more complicated targets you may have to deal with complicated handshakes, session state handling, and potential services that utilize multiple streams for C2 and tasking.

The easiest way to prevent getting lost in the potential mess is to try and ascertain the most basic TCP protocol supported and locate it's socket accept function. If you're lucky the socket receive function will not be obfuscated, and you can look in the "Symbol Tree" window for that function.

![[Pasted image 20260228211416.png]]

Here we can see that this external reference has 2 cross-references (XREFs). This is an instance where the binary is importing a function from a DLL, in this instance that DLL is ws2_32.dll located in the Windows\System32 directory. 

Note: Inside the source code when I used \#include <winsock2.h> this imported the header file that imported the needed windows socket DLLs in my binary. When I programmatically called the accept() function that the ws2_32.dll library exposed, the linker made the connection between my code and the system's DLL and added the needed code (and added the library into the Import Address Table (IAT)) so that the Windows Loader could modify the location of that function call at program initialization/start time. This process is not complex, but it is outside the scope of this training. Review the [[Building A Binary (Primer)]] for more information. 

Since this program is written in C the execution flow is extremely simplistic and easy to follow. We can see that one of the XREFs is inside the main function. Double clicking the address beside main, in this instance it would be **1400121c8** in the main:1400121c8 seen.

![[Pasted image 20260228212616.png]]

We can now see in the decompilation window the call to accept. The local_1d10 is the pointer to socket and later we can see it's stored in an array. My goal is not to completely dissect the execution flow to write a report, academic paper, or professional blog post. I only need to know enough to understand the basic flow of data so I can start to build my testing harness. At this point, the execution flow and the expected data structure is straight forward. However, in a more complex environment, you may need to utilize dynamic analysist and bounce back and forth between static and dynamic to ascertain the state of data at a given point.

#### \<Tangent>

Due to Address Space Layout Randomization (ASLR) the base address of the dynamic instance will change every time you reboot the system. But in nearly all modern cases the Image Base Address of the running instance will not be the same as the static instance. You could rebase your static instance when needed, but I tend to use a converter function in an interactive python terminal to do address conversions between the two.

I had google generate this sample code that performs that task.
``` python
def translate_address(target_addr, source_base, destination_base):
    """
    Translates an address from one image base to another.
    
    :param target_addr: The specific address you want to convert
    :param source_base: The base address of the current environment (Static or Dynamic)
    :param destination_base: The base address of the environment you are moving to
    :return: The translated address in the destination space
    """
    # 1. Calculate the RVA (Relative Virtual Address) 
    # This is the offset from the start of the module
    rva = target_addr - source_base
    
    # 2. Apply that offset to the new base
    return destination_base + rva

# --- Example Usage ---

# Static Base (from IDA Pro / Ghidra / PE Header)
STATIC_BASE = 0x140000000 

# Dynamic Base (The 'Actual' load address found in x64dbg / Cheat Engine)
DYNAMIC_BASE = 0x7ff76e8a0000 

# Example: A function found at 0x140001234 in IDA
static_func_addr = 0x140001234

# Convert Static -> Dynamic
runtime_addr = translate_address(static_func_addr, STATIC_BASE, DYNAMIC_BASE)

# Convert Dynamic -> Static
back_to_static = translate_address(runtime_addr, DYNAMIC_BASE, STATIC_BASE)

print(f"Static Address:  {hex(static_func_addr)}")
print(f"Dynamic Address: {hex(runtime_addr)}")
print(f"Verified Static: {hex(back_to_static)}")
```
#### \<\Tangent>

#### Client data handler(s)

Now that we have found the code that manages the connection from the client we can begin to start to ascertain the code flow looks like. The accept() function is a phenomenal starting point in blackbox RE due to the simple context around the function's usage. It's used for accepting connections. Sometimes you may find yourself digging into the wrong socket hander, but it's best to start looking at the TCP communications functionality if your targeted binary has that method of communications. 

To dig a bit deeper into value of targeting the accept() function, let's keep in mind where in the connection chain the accept occurs. It occurs before any decryption, but after most of the system boilerplate code. This reduces the amount of time you're sifting through non-applicable code. 

In this binary there are clear indications of application layer encryption and the fact that RC4 is what's being used. That's usually not the case. You'll have to follow the execution right after the connection to ascertain which encryption algorithm and variant is being used. 

The decryption process will result in several function calls being made. In the past you would have to parse through the algorithm's ASM mnemonics and/or decompilation code to  ascertain which one is being used. The easy answer now is to ask AI what algorithm is being used.  Be mindful that AI is imperfect and has in the past come to the wrong conclusion about which algorithm variant was being used. 

Below we can see the RC4 decrypt function being called on some data. Here it's easier to ascertain what's occurring because the debug symbols are present in the binary and the function is labeled. 

![[Pasted image 20260314203148.png]]

If programming is not your strong suit and reading the ghidra assigned variables is making tracing the code difficult, you can `Show Call Trees for accept`. This will show you a list of function call chains into and out from the targeted address. 

![[Pasted image 20260314203026.png]]

![[Pasted image 20260314203821.png]]


As you can see here, there are no outgoing calls made from within the accept function. You need to go to the function containing the accept call that you're interested in and `Show Call Trees for 0x*******`. Below I go back to the function that contains the targeted accept function and right click on the first address of the containing function.

![[Pasted image 20260314204224.png]]

As you can now see, we can see all of the outgoing function calls within this function. We can see our accept function half way down the list. We can see a short ways down the recv() function being used to receive data from the client. 

![[Pasted image 20260314204407.png]]

If you read through the primer for RC4 you'll recognize what's occurring here. If not you're going to miss out in that I will simply say that we can see the hardcoded RC4 decryption string being used in the initialization of the decryption functionality. 

![[Pasted image 20260314204618.png]]

Now that we've nailed down the encryption method used and the static key used in the encryption, we need to ascertain what the server is doing with the data it has received and is now decrypted. 

First, we can see that it prints to a terminal window and it then writes to a file. This is important because one of your goals is to determine where possible contaminated data is handled and where its final resting place is. In this instance it's in a file on disk. However, it can remain in memory, be transformed, stored on the stack, added to a larger structure, etc. 

Unfortunately, there is nothing I see right now that results in something I'm going to be able exploit, beyond a DOS. 

### Data Handlers

Now that we know how the data is handled we need to determine what handles the data. What I mean by that, what is the programmatic customer of my data; what function handles my data during internal usage? That can take many forms, native GUI code, web frontends, databases, data transformation and processing code, etc. 

In this instance we encounter a web UI. It's a python based web service that's using the flask module to handle the web components. We know this at this point because we have the server side components.

You should be attempting to set up the entire setup so you're testing against a true-enough running version of targeted software. The web UI below simply displays the decrypted data to the web page. This is great news. This opens up a whole additional world of potential exploit vectors.

![[Pasted image 20260314210502.png]]


taking a peek at the root webpage of the site, we see it's index.html. Let's take a look at it. 

**STOP!**  At this point I would normally have started constructing my test harness. Most often I will need to test the hypothesis' I've generated while looking at the static binary against what I'm seeing in a running instance of the code. However, I will address that after I discuss the web UI code.

``` javascript
        async function updateLog() {
            try {
                const response = await fetch('/api/data');
                const result = await response.json();
                const logContent = document.getElementById('log-content');

                // Clear and repopulate the log
                logContent.innerHTML = '';
                result.data.forEach(line => {
                    //const div = document.createElement('div');
                    //div.className = 'entry';
                    //div.textContent = line;
                    //logContent.appendChild(div);
                    const logContainer = document.getElementById('log');
                    const fragment = document.createRange().createContextualFragment(line);
                    //logContainer.innerHTML = line
                    logContent.appendChild(fragment);
```

Above is a snippet from the index.html. Pay attention to any comments or commented out code. I'm not a web developer so I'm not going to pontificate on any specific strategy of identifying bugs. However, I do know there is some data handling here and recognize that the developer placed it in a try/catch block. AI is good at identifying potentially dangerous code and is useful when deal with a language or another topic you're not familiar with. If you're using an abliterated model, you can simply say, "find a potentially exploitable bug in this code." With a normal model with all of the security guardrails intact, you may have to play word games with it, but the overall request idea should be similar. 

AI tells me that the way the data is being written to the page is dangerous and that data passed in. So naturally, that's where I want my data to go. 

#### Getting my data to the dangerous code

Not all bugs are equal. Most bugs are technical bugs in the software, but are not reachable by user controlled data. Exploitation can require several specific events occur around your dangerous code to result in an exploitable scenario. This usually means that you have to be able to push your malicious code to the target software, have it accept the data and place it in some buffer, do something with the data while handling it in a way that does not properly maintain data integrity.

Regardless of what type of exploit you're going to attempt, you're trying to submit data that is not properly handled by the targeted by software. In this instance I am pretending to be a client. I have the encryption details, I can pass the initial check(s), and can submit tainted data into the target buffer. Without getting to deep into the mechanical requirements of various binary exploit vectors, I'll say that most memory based exploits targeting code that implements modern memory protections and randomizations, you're going to need an accompanying memory/data leak bug along with your overflow. There are instances where a single exploit, slightly changed can meet both requirements, but that requires some poor programming decisions on behalf of the socket handler developer. 

As in the white box we'll need to write some code to help us get our malicious testing data deeper into the targeted binary's code in an effort to trigger the bug that may be exploitable. 

``` python 
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
STATIC_KEY = b"STATIC_RC4_KEY_123"

def rc4_crypt(key, data):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = j = 0
    res = []
    for char in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        res.append(char ^ S[(S[i] + S[j]) % 256])
    return bytes(res)

def main():
    message = "Secret data from Python client!\n"
    encrypted = rc4_crypt(STATIC_KEY, message.encode())
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            s.sendall(encrypted)
            print(f"Sent: {message}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

This vibe coded harness spells out pretty clearly where your malicious data should go, `message`. 

We can see the same message from the web UI here in the message. So now we can see and understand the flow of our data.

```
+----------+          +----------+          +----------+
|          |          |          |          |          |
|  Client  |--------->|  Server  |--------->|   File   |
|          | (1) Send |          | (2) Save |          |
+----------+          +----------+          +----------+

                                                 |
                                                 | (3) Read
                                                 v
+----------+          +----------+          +----------+
|          |          |          |          |          |
| Browser  |<---------| Web Svc  |<---------|  System  |
|          | (5) View |          | (4) Pull |          |
+----------+          +----------+          +----------+
```


#### Testing 

Now that I can get my malicious data into the inner processing of the server and a completely different client component of another aspect of the server binary, I need to take stock of what I can have an impact on. Of course there are DOSs present, but this isn't a bug bounty, I want RCE or some other data disclosure bug. 

My testing will quickly maneuver away from basic crashes via massive payloads to determining any additional complex structures required to get my payload to the targeted function, minimum and maximum payload lengths possible, etc. I'm going to skip this step due to the simple nature of the targeted binary. 


#### Exploitation

This part of the process really starts at the beginning... Whenever you identify a function that handles external data, you should be contemplating how you could break it. This becomes more effective with experience and the broadening of your exploitation method repertoire. The learning and identification process can be expedited and illuminated by submitting the function decompilation into an AI prompt and ask for inline comments and a list of vulnerabilities in the  decompiled code. 

In this binary there may be other vulnerabilities, but the focus of the training is illuminate the life cycle of your malicious data as it transits various components of our targeted binary. Understanding the path of your data and what form it's taking as it traverses this path is very important. 






## THE END...
		for now...