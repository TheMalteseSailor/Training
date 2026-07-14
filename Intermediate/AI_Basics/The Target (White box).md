Back: [[The Target (Setup)]]
## Looking At The Code

We're going to start looking at the Server component. 

You aren't always going to be able to see the source code for a binary you're looking to exploit. If you are you're engaged in "White box" research because you are looking at the source code and details that may ultimately be removed during the compilation and/or productization process. Since we have the source code let's see what the C looks like before diving into an analysis tool.

Let's start this off by taking a look at each chunk of source code we have at our disposal. 
### Server

Real malware controllers will contain a large amount of code that's not relevant to this training, so I've constructed a simulation that represents a realistic cross-section of the core client handling functionality. Let's look at the source code for this server cross-section functionality.

``` C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h>
#include <windows.h> 

#pragma comment(lib, "ws2_32.lib")

#define PORT 8080
#define BUFFER_SIZE 4096
#define MAX_CLIENTS 10
#define KEY "STATIC_RC4_KEY_123"

typedef struct {
    unsigned char s[256];
    int i, j;
} RC4_CTX;

void rc4_init(RC4_CTX* ctx, const unsigned char* key, int key_len) {
    for (int i = 0; i < 256; i++) ctx->s[i] = (unsigned char)i;
    for (int i = 0, j = 0; i < 256; i++) {
        j = (j + ctx->s[i] + key[i % key_len]) % 256;
        unsigned char temp = ctx->s[i];
        ctx->s[i] = ctx->s[j];
        ctx->s[j] = temp;
    }
    ctx->i = ctx->j = 0;
}

void rc4_crypt(RC4_CTX* ctx, unsigned char* data, int len) {
    int i = ctx->i, j = ctx->j;
    unsigned char* s = ctx->s;
    for (int k = 0; k < len; k++) {
        i = (i + 1) % 256;
        j = (j + s[i]) % 256;
        unsigned char temp = s[i];
        s[i] = s[j];
        s[j] = temp;
        data[k] ^= s[(s[i] + s[j]) % 256];
    }
    ctx->i = i; ctx->j = j;
}

int main() {
    WSADATA wsa;
    SOCKET master, new_socket, client_socket[MAX_CLIENTS];
    struct sockaddr_in server, address;
    int addrlen = sizeof(struct sockaddr_in);
    char buffer[BUFFER_SIZE];
    fd_set readfds;

    // Resolve full path for the file in the EXE directory
    char path[MAX_PATH];
    GetModuleFileNameA(NULL, path, MAX_PATH);
    char* last_slash = strrchr(path, '\\');
    if (last_slash) *(last_slash + 1) = '\0';
    strcat(path, "decrypted_output.txt");

    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0) return 1;

    for (int i = 0; i < MAX_CLIENTS; i++) client_socket[i] = 0;

    master = socket(AF_INET, SOCK_STREAM, 0);
    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(PORT);

    if (bind(master, (struct sockaddr*)&server, sizeof(server)) == SOCKET_ERROR) return 1;
    listen(master, 3);

    printf("Server Listening on Port %d\n", PORT);
    printf("Writing to: %s\n", path);

    // Open file for appending
    FILE* fptr = fopen(path, "ab");
    // Check to see if the file pointer is valid
    if (!fptr) {
        printf("Error: Could not open file for writing.\n");
        return 1;
    }
	
    while (1) {
        FD_ZERO(&readfds);
        FD_SET(master, &readfds);
        for (int i = 0; i < MAX_CLIENTS; i++) {
            if (client_socket[i] > 0) FD_SET(client_socket[i], &readfds);
        }

        select(0, &readfds, NULL, NULL, NULL);

        if (FD_ISSET(master, &readfds)) {
            new_socket = accept(master, (struct sockaddr*)&address, &addrlen);
            for (int i = 0; i < MAX_CLIENTS; i++) {
                if (client_socket[i] == 0) {
                    client_socket[i] = new_socket;
                    printf("New client connected.\n");
                    break;
                }
            }
        }

        for (int i = 0; i < MAX_CLIENTS; i++) {
            SOCKET s = client_socket[i];
            if (FD_ISSET(s, &readfds)) {
                memset(buffer, 0, BUFFER_SIZE);
                int valread = recv(s, buffer, BUFFER_SIZE - 1, 0);

                if (valread <= 0) {
                    closesocket(s);
                    client_socket[i] = 0;
                    printf("Client disconnected.\n");
                }
                else {
                    // Decrypt
                    RC4_CTX ctx;
                    rc4_init(&ctx, (const unsigned char*)KEY, (int)strlen(KEY));
                    rc4_crypt(&ctx, (unsigned char*)buffer, valread);

                    // 1. Write to Terminal
                    printf("Decrypted: %s\n", buffer);

                    // 2. Write to File
                    fwrite(buffer, 1, valread, fptr);
                    fprintf(fptr, "\n"); // Add newline for readability in file
                    fflush(fptr);
                }
            }
        }
    }

    fclose(fptr);
    WSACleanup();
    return 0;
}
```


We can now see how the basic mechanics of how the server both handles client callbacks and how it handles the data sent to it by clients. This can seem overly simplistic, and it is. However, the core concepts are remain, despite the extreme simplicity of the example. 

In a real world vulnerability research environment, I want to determine where the target binary, software, or service handles external data when I'm mapping out the target's attack surface. In this instance, my target is the functionality that manages the client data handler(s), to simulate the hunting for an Remote Code/Command Execution (RCE). 

Most software developers know that this will be a prime target for a vulnerability researcher and will spend considerable effort to ensure this specific functionality is securely written. In the instances like we have here, where we're using an language that's unmanaged, the compiler can make considerable changes to the final binary's actual structure. This can and has in the past functionally broken safe programming practices. This is less likely now, but still persists at some level. 

### Test Harness (Fake Client)

Now that we understand my target, some context of how the code flow works, and have some understanding as to what the expected data will look like from a real client, I can build my test harness. A test harness is custom program, usually written in python, that allows you to quickly perform extremely granular targeted testing. This can be extremely difficult to implement in practice because the code you're looking to target may be far down the execution chain and you must understand the all of the intermediate data state to a level that any intermediate data checks or validations will pass. 

The first hurtle is usually encompasses 2 things: encryption and data structure. In the test harness below, there is no data structure. That's because the server facsimile does not handle complex communications. In a real targeted binary, it's extremely likely that the data will need to be in some form of structured format. However, for this training, the handler will be straightforward so that you don't get lost in the vast milieu of non-relevant context in a real piece of malware.

``` python
import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 8080
STATIC_KEY = b"STATIC_RC4_KEY_123"

# This function encrypts our test data.
# In a real test harness, you want to run your data through a decryption check.
# This will ensure check to ensure your encryption and final pre-encryption data is in a state you think it's in.
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
	# message is the variable that will contain our test data.
    message = "Secret data from Python client!\n"
    encrypted = rc4_crypt(STATIC_KEY, message.encode())
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))
            # Sends your payload to the target.
            s.sendall(encrypted)
            print(f"Sent: {message}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
```


### WebUI

If you're like me you probably looked at the webUI prior to this point and have some ideas as to what data I want to start trying to send to the server.

``` 
webui.py
templates
	|___ index.html
```

You have to ask yourself, "What am I try to accomplish?" The answer is to obtain code or command execution. In this section we're going to tale a look at the user's web interface. You may not be able to reach the web interface from your existing access, but you may be able to poison the data stored by the server so that when the legitimate user accesses the data, they trigger a trap that you've staged in the form of an exploit. 

Since we are operating on the fact that you have the server components, We'll take a look at the management interface too. This web management UI purposefully lacks many basic functionality. This was so that you could simply parse the code and understand the basic flow of data.

``` python
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Ensure this path matches the directory where your C server is writing the file
FILE_PATH = "decrypted_output.txt"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'r') as f:
            # Read all lines and return them as a list
            content = f.readlines()
        return jsonify({"data": content})
    return jsonify({"data": ["File not found yet..."]})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

From a quick look what can we ascertain from this python script? 
	1. The name of the file is hardcoded
	2. Though jsonify() is used, it looks like data is read without filtering from the decrypted_output.txt file.

Now let's take a look at the code that displays the management console data to the browser. I'm not a web developer, so I'll try to locate the code that actually does the displaying of the data to the user. 

``` html ln:true
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Live Decrypted Traffic</title>
    <style>
        body {
            font-family: sans-serif;
            background: #121212;
            color: #00ff00;
            padding: 20px;
        }

        #log-container {
            background: #000;
            border: 1px solid #333;
            padding: 15px;
            height: 400px;
            overflow-y: auto;
        }

        .entry {
            border-bottom: 1px solid #222;
            padding: 5px 0;
            font-family: monospace;
        }
    </style>
</head>
<body>
    <h1>Real-Time Decrypted Traffic</h1>
    <div id="log-container">
        <div id="log-content">Waiting for data...</div>
    </div>

    <script>
        async function updateLog() {
            try {
                const response = await fetch('/api/data');
                const result = await response.json();
                const logContent = document.getElementById('log-content');

                // Clear and repopulate the log display
                logContent.innerHTML = '';
                result.data.forEach(line => {
                    const logContainer = document.getElementById('log');
                    const fragment = document.createRange().createContextualFragment(line);
                    logContent.appendChild(fragment);
                });

                // Auto-scroll to bottom
                const container = document.getElementById('log-container');
                container.scrollTop = container.scrollHeight;
            } catch (err) {
                console.error("Error fetching data:", err);
            }
        }

        // Refresh every 2 seconds
        setInterval(updateLog, 2000);
        updateLog(); // Initial call
    </script>
</body>
</html>
```

The updatLog() function looks important. Notice that the developer has wrapped that code block in an exception handler. A developer should do that when the code is processing, manipulating, or performing some task that may result in a state that's either not intended or is recognized as not a condition that's acceptable to continued execution. Just because a code block is wrapped in a try/catch block does not mean it's not susceptible to exploitation. It just means you're likely going to have to ride a very fine line between legitimate enough data and still malicious enough to trigger the desired vulnerable code. 

Like I said, I'm not a web developer, but excuses don't find bugs... Doing some research on the internet I can tell there are several potential vulnerabilities. However, you must keep then entire data life-cycle in mind as you assess it at different points in its life-cycle. The data will have different meaning and context depending on where it resides at the point in which you're viewing it and how it's being accessed. Even if you have to write narrative style notes as to the context you see at different points where you see the data, you need to capture what you're seeing in a manner that's you're going to understand when you come back to it.

An example of this in this instance would look something like this.
```
The network traffic is RC4 encrypted with a static key that's hardcoded into the client and the binary. The network data structure is basic in that the RC4 stream resets with every message. This means that I don't have to worry about stream desynchronization. You can see this in the server where it recreates the RC4 decryption context with every decrypt. This means it starts back at the beginning of the stream.

In my fake client script, I've implemented in a similar manner and it'll handle that for me. 
#TODO: I need to implement a decrypt check/validation for the data so that I can visually check the validity of the data as the complexity of the data begins to increase. 
```

If you're lost as to what any of that means, go back and review the RC4 encryption primer.

If we had all of this information, we might be able to skip a large portion of the dynamic testing component of our testing, but since you're going to have to stand up an instance of the targeted binary to test your exploitation attempts via your fake client script, you might as well throw your binaries into ghidra or Ida. Since the compilation process can affect the end state of the binary you need to see how the actual released binary looks at the system level. 

Since the white box and black box sections overlap at this point, I'll break here and integrate it into the black box section.

Next: [[The Target (Black box)]]



