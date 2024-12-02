
# Ollama + Gemma2:27B Setup with Ngrok Exposure

This guide outlines the steps to set up Ollama serving the `gemma2:27b` model locally and expose the service to the world using Ngrok.

---

## Prerequisites

- **Operating System**: macOS (M2 chip)
- **Software**:
  - [Homebrew](https://brew.sh) (to install dependencies)
  - [Ollama](https://ollama.ai) (via Homebrew)
  - [Ngrok](https://ngrok.com) (via Homebrew)

---

## Setup Steps

### 1. Install Ollama
Use Homebrew to install Ollama:
```bash
brew install ollama
```

### 2. Run `gemma2:27b` Locally
Start the `gemma2:27b` model in serving mode:
1. Launch Ollama's serve mode:
   ```bash
   ollama serve
   ```
2. In a separate terminal, run the `gemma2:27b` model:
   ```bash
   ollama run gemma2:27b
   ```

By default, Ollama will serve the model on `localhost:11434`.

---

### 3. Install Ngrok
Install Ngrok via Homebrew:
```bash
brew install ngrok
```

Authenticate Ngrok with your account token:
```bash
ngrok config add-authtoken <YOUR_AUTH_TOKEN>
```

---

### 4. Expose Localhost to the World
Use Ngrok to expose the port `11434`:
```bash
ngrok http 11434 --host-header="localhost:11434" --url=merry-publicly-reptile.ngrok-free.app
```

This will create a public-facing URL (e.g., `https://merry-publicly-reptile.ngrok-free.app`) that maps to your local `localhost:11434`.

> **Note:** If you encounter a `404` error, ensure you include the `--host-header` parameter.

---

### 5. Test the Setup
You can verify the setup using a `curl` command:
```bash
curl https://merry-publicly-reptile.ngrok-free.app/api/generate -H "Content-Type: application/json" -d '{
  "model": "gemma2:27b",
  "prompt": "who are you",
  "stream": false
}'
```

If successful, the response from `gemma2:27b` should appear in the terminal.

---

## Troubleshooting

- **404 Errors with Ngrok**: Ensure the `--host-header="localhost:11434"` parameter is included when starting Ngrok.
- **Ollama Issues**: Confirm Ollama is properly installed and running by checking its logs or restarting the service.
- **Connection Problems**: Verify that your firewall settings allow external access via the Ngrok URL.

---


Enjoy using Ollama with the `gemma2:27b` model and Ngrok!
