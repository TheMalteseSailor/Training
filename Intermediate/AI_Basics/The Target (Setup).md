This section will discuss and utilize a test server, client, and web UI.

### Bundle Components:
1. Server source file - Server.cpp
2. Test harness - test_client.py
3. Web UI - webui.py and templates\index.html
### Requirements:
1. python3
2. python3 flask
3. (optional) Windows VS C compiler if building server from source.

### Setup (using bundled binaries)

1. Open 3 terminals or cmd.exe windows
2. unzip bundle 
``` cmd
cd TrainingMaterial\
```
3. In the window you want to run your local webserver in.
``` cmd
python -m venv webui
```
4. install the python module flash. You'll need internet because it's not bundled
``` cmd
...> webui\Scripts\activate
(webui) ...> pip install flask
```
5. Leave this window open to run your local webserver later
6. In another window locate your server binary 
7. (if needed) open the webui.py file and make the following change:
	``` python
	-FILE_PATH = "..\\x64\\Debug\\decrypted_output.txt"
	+FILE_PATH = "PUT\\REAL\\PATH\\decrypted_output.txt"
	```



Next: [The Target (Intro)](The%20Target%20%28Intro%29.md)

