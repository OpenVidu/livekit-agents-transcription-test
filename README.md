# livekit-agents-transcription-test

Minimal setup to test audio transcription using livekit-agents STT node

1. Build the agent container

   ```bash
   docker build -t livekit/transcription-agent-test:latest agent/.
   ```

2. Start the services

   ```bash
   docker compose up -d
   ```

3. Run the webapp

   ```bash
   cd webapp
   npm install
   npm start
   ```

4. Open http://localhost:3000 in your browser and test.
