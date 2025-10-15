# livekit-agents-transcription-test

Minimal setup to test audio transcription using livekit-agents STT node (with Amazon Transcribe)

1. Build the agent container

   ```bash
   docker build -t livekit/transcription-agent-test:latest agent/.
   ```

2. Export requried env vars and start the agent

   ```bash
   # Export your LiveKit Cloud credentials
   export LIVEKIT_URL=wss://xxxxxxxx.livekit.cloud
   export LIVEKIT_API_KEY=your_livekit_cloud_api_key
   export LIVEKIT_API_SECRET=your_livekit_cloud_api_secret

   # Export your AWS credentials
   export AWS_ACCESS_KEY_ID=your_access_key_id
   export AWS_SECRET_ACCESS_KEY=your_secret_access_key
   export AWS_DEFAULT_REGION=your_aws_region
   
   # Start the agent
   docker compose up -d
   ```

3. Set up your LiveKit Cloud credentials in the webapp HTML [right here](https://github.com/OpenVidu/livekit-agents-transcription-test/blob/87c0ea4d1872ee6de645e5642a2135ebaa0cb190/webapp/index.html#L97-L99):

   ```html
   const LIVEKIT_URL = "wss://xxxxxxxx.livekit.cloud";
   const LIVEKIT_API_KEY = "your_livekit_cloud_api_key";
   const LIVEKIT_API_SECRET = "your_livekit_cloud_api_secret";
   ```

4. Run the webapp

   ```bash
   cd webapp
   npm install
   npm start
   ```

5. Open http://localhost:3000 in your browser and test.
