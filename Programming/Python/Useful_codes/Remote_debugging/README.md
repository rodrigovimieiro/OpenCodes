# How to remote debug (VScode): 

-- You can leave your codes local and synchronize them remotely:
1. Download and Install the SFTP extension (@Natizyskunk);
2. Setup the SFTP configs for your project (see example `sftp.json`);
3. Press `F1` and type:
    -  `SFTP: Sync:Local->Remote`;
4. Install debugpy on the remote server
    - `pip install debugpy`
5. Add the following to your Python code to the beginning of the .py file:
    - ```python
      import debugpy
      debugpy.listen(("0.0.0.0", 5678))  # Replace 5678 with your debug port
      debugpy.wait_for_client()  # Pause execution until VS Code connects
      print("Debugger connected. Ready to execute.")
      ```
6. In VSCode, add debugger with a `launch.json` file (see example `launch.json`);

* Make sure to edit the JSON files correctly first

-- Alternatively, you can use remote SSH to connect to the server and debug there. This is placing your codes remotely;


Reference: [SFTP](https://toptechtips.github.io/2023-04-19-vscode-sync-local-to-remote/)
