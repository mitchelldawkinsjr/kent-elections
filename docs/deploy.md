# Deploy

Push to `main` runs `.github/workflows/deploy-vps.yml`. Markdown-only pushes do not deploy. **Run workflow** on the Actions tab rebuilds the current `main`.

Public site: https://ballot.360web.cloud
Container: kent-ballot-app
Loopback on the VPS: 127.0.0.1:8033
VPS directory: /opt/360ws/clients/docker-app/kent-ballot/
Proxy forwards to http://kent-ballot-app:80 on Docker network `360ws-network`.

After `up`: none.

Secrets (GitHub Actions, same values as little-sprouts): `VPS_HOST`, `VPS_USER`, `VPS_SSH_KEY`. Optional: `VPS_SSH_PORT`, `SLACK_WEBHOOK`.
