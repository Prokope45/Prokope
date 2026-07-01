#!/bin/sh

# Authors:
#	- Jared Paubel

# ln ~/.local/share/opencode/auth.json

# Create .opencode directory in project root
mkdir -p .opencode

# Create opencode.json
cat > .opencode/opencode.json << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": "ask",
    "webfetch": "allow"
  },  
  "provider": {
    "lmstudio": {
      "name": "LM Studio (local)",
      "npm": "@ai-sdk/openai-compatible",
      "options": {
        "baseURL": "http://host.docker.internal:1234/v1"
      },
      "models": {
        "openai/gpt-oss-20b": {
          "name": "gpt-oss-20b",
          "thinking": true
        }
      }
    }
  }
}
EOF

# Create auth.json
cat > .opencode/auth.json << 'EOF'
{
  "google": {
    "type": "api",
    "key": ""
  }
}
EOF

# Create AGENTS.md
cat > .opencode/AGENTS.md << 'EOF'
You are a helpful coding agent that can create boilerplate code, debug problems, and optimize existing systems. However, you must cite yourself when writing any significant portion of code. The only exception is if the file already exists and you are editing it to fix a bug or improve it under the user's guidance, especially if user tweaks what you wrote. Otherwise, if you create a new file or otherwise change well over 75% of the files contents, cite yourself at the top of the file using a docstring:

```
<Some description about what the file does>

Authors:
    - <User's name - use Github username if not provided>
        - <Line segments that were edited by user or you wrote after user critiqued your code (i.e. "Lines 25-54 written by human")>
    - <Your agent and model name, and whether you are a local or propriety model such as  "OpenCode agent - local qwen/qwen3.5-9b">
        - <Line segments that you actually wrote with no user input (i.e. "Lines 1-24 written")>
Percentage written by Agent: <Using above lines-of-code for human and agent, give best percentage guess of how much was written by you or another AI>
```
EOF

echo "Setup complete! .opencode folder created with configuration files."