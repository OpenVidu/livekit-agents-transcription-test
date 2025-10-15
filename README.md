# livekit-agents-transcription-test

Minimal setup to test audio transcription using livekit-agents STT node (with Amazon Transcribe)

1. Build the agent container

   ```bash
   docker build -t livekit/transcription-agent-test:latest agent/.
   ```

2. Export AWS credentials env vars in the shell and start the services

   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key_id
   export AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export AWS_DEFAULT_REGION=your_aws_region
   
   docker compose up -d
   ```

3. Run the webapp

   ```bash
   cd webapp
   npm install
   npm start
   ```

4. Open http://localhost:3000 in your browser and test.
