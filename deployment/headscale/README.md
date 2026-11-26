# Headscale Server Deployment

Docker Compose deployment configuration for the existing Swarmchestrate Headscale server.

## 1. Overview

This directory contains the Docker Compose configuration and example settings for managing the existing Headscale server.

The deployment is designed to preserve the current server installation, including its configuration, database, encryption keys and TLS certificate cache.

**This deployment configuration is designed to support automated Headscale installation and deployment on a Linux server. It is initially being developed and validated against the existing Swarmchestrate Headscale instance. The deployment process must preserve existing data and configuration when migrating that instance.**

## 2. Deployment Files

| File | Purpose |
|---|---|
| `docker-compose.yml` | Defines the Headscale Docker service |
| `.env.example` | Example deployment environment variables |
| `config.yaml.example` | Reference Headscale server configuration |
| `.gitignore` | Excludes local secrets and backup files |

## 3. Existing Server Configuration

The current server uses:

- Headscale version: `v0.27.1`
- Docker image: `headscale/headscale:0.27.1`
- Database: SQLite
- Configuration directory: `/etc/headscale`
- Data directory: `/var/lib/headscale`
- HTTPS: Let's Encrypt
- HTTP-01 certificate challenge
- Ports: `80` and `443`

The Compose deployment pins the existing image by digest to avoid unintended image changes.

## 4. Persistent Data

The deployment reuses the existing server directories:

| Host path | Container path | Purpose |
|---|---|---|
| `/etc/headscale` | `/etc/headscale` | Configuration and ACL policy |
| `/var/lib/headscale` | `/var/lib/headscale` | Database, Noise key and certificate cache |

These directories must not be deleted or overwritten during deployment.

## 5. Configuration

The deployment environment template is provided in `.env.example`.

Before validating the deployment, create a local `.env` file based on that template.

The example Headscale configuration is provided in `config.yaml.example`.

Do not overwrite the existing server configuration with the example file.

## 6. Validation

From the repository root on the Ubuntu server, validate the Compose configuration:

```bash
docker compose \
  --env-file deployment/headscale/.env \
  -f deployment/headscale/docker-compose.yml \
  config
```

This validates the Compose configuration without replacing the running container.

## 7. Migration Procedure

The existing Headscale service currently runs in a manually created Docker container.

Docker Compose cannot directly adopt that container. A controlled migration is therefore required.

Before migration:

1. Inspect the existing container and configuration.
2. Create a backup of `/etc/headscale` and `/var/lib/headscale`.
3. Verify the backup.
4. Prepare rollback commands.
5. Schedule a maintenance window.
6. Obtain approval before stopping or replacing the existing container.

The existing database, Noise private key, TLS cache and ACL policy must be preserved.

**Do not run `docker compose up` against the existing server before completing the backup and migration preparation.**

## 8. Deployment Status

<badge color="warning">Migration pending</badge>

- [x] Existing Headscale server inspected.
- [x] Docker image and persistent directories identified.
- [x] Compose configuration prepared.
- [ ] Compose configuration validated on the Ubuntu server.
- [ ] Existing server backup created and verified.
- [ ] Rollback procedure prepared.
- [ ] Controlled migration completed.
- [ ] Post-migration verification completed.

## 9. Operational Commands

Check service status:

```bash
docker compose -f deployment/headscale/docker-compose.yml ps
```

View logs:

```bash
docker compose -f deployment/headscale/docker-compose.yml logs -f
```

Check Headscale health:

```bash
docker exec headscale headscale health
```

Check the HTTPS endpoint:

```bash
curl -I https://headscale-test.swarmchestrate.sztaki.hu
```

Refer to the main repository README for information about the Headscale API integration.
