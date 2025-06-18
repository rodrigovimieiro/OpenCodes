# Continue Configuration for VSCode

This guide explains how to install and use the [Continue](https://continue.dev) extension in Visual Studio Code with a custom model configuration using [Ollama](https://ollama.com).

## 📦 What is Continue?

[Continue](https://continue.dev) is an open-source AI-powered coding assistant for Visual Studio Code that helps you complete, refactor, and understand code using Large Language Models (LLMs).


## ⚙️ Prerequisites

- [Visual Studio Code](https://code.visualstudio.com/) installed
- [Continue Extension](https://marketplace.visualstudio.com/items?itemName=Continue.continue) installed in VSCode
- [Ollama](https://ollama.com/) installed and running with the required models:
  - `gemma3:27b-it-qat`
  - `qwen2.5-coder:1.5b-base`

- You can install these models using:
    ```bash
    ollama pull gemma3:27b-it-qat
    ollama pull qwen2.5-coder:1.5b-base
    ```

## ⚙️ Remote server (SSH)

- Ensure the remote server has Ollama running:
    ```bash
    ollama serve
    ```
- On your local machine, tunnel the Ollama default port (11434) with:
    ```bash
    ssh -N -L 11434:localhost:11434 user@remote-host
    ```

## 🧠 Notes

- You can customize or add more models by editing the _.continue/config.json_ file. See the example in the current folder.