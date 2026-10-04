# VPS deployment

The `Deploy Flaav to VPS` workflow runs manually on `main`. Its GitHub runner
must be registered only for `SonZions/flaav` with labels `my-vps` and `flaav`.
The runner invokes the root-owned `/usr/local/sbin/flaav-vps-deploy` bridge;
it does not need Docker access or read access to `/etc/migrated-containers`.

The bridge fetches `origin/main` in `/opt/vps-deploy/flaav/repo`, requires it to
match the workflow commit, builds the image into local Docker, and replaces
`flaav-vps`. It keeps the former container until `/healthz` is ready. On a
failed start it restores the former container. The existing VPN-only port,
memory limit, log rotation and root-owned env file remain in use.

The bridge is installed separately from the Git checkout. Changes to
`deploy/vps-deploy.sh` require review and a root-owned reinstall on the VPS.
