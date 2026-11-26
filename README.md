# Headscale Integration

A standalone Headscale integration and deployment repository supporting VPN functionality within the **Swarmchestrate Cluster Builder** ecosystem.

This repository contains the API integration, automation scripts, tests and deployment configuration required to interact with and manage a Headscale VPN control plane.

The primary goal is to provide reusable Headscale functionality that can be consumed by the separate `cluster-builder` project during cluster provisioning and orchestration.

## 1. Purpose

Headscale provides the VPN control plane used by Swarmchestrate to establish and manage connectivity between infrastructure components.

This repository maintains the integration layer responsible for communicating with Headscale through its REST API.

The integration is designed to allow Cluster Builder to automate VPN-related operations without having to implement Headscale API communication directly inside its core provisioning logic.

## 2. Architecture and API Functionality

The architecture consists of three main components:

| Component | Responsibility |
|---|---|
| Headscale server | Provides the VPN control plane |
| Headscale integration | Implements API communication and management functionality |
| Cluster Builder | Consumes the integration as part of cluster provisioning and orchestration |

### Python API Client

The main API client is implemented in:

`cluster_builder/infrastructure/headscale.py`

It currently supports:

- Creating Headscale users.
- Listing users.
- Deleting users.
- Generating pre-authentication keys.
- Listing nodes.
- Deleting nodes.
- API authentication and error handling.

The client is designed to be reusable by the Cluster Builder project.

### Integration with Cluster Builder

The Headscale API client is intended to provide the Headscale management functionality used by the separate `cluster-builder` project. The two repositories are maintained independently, with the integration providing the Headscale-specific API implementation and deployment tooling.

This allows Cluster Builder to perform operations such as:

- Creating Headscale users for cluster infrastructure.
- Generating pre-authentication keys for node registration.
- Managing Headscale nodes.
- Supporting VPN connectivity for K3s cluster components.

The Headscale API functionality is maintained independently from Cluster Builder's core provisioning logic.

## 3. Installation and Configuration

The Python integration requires its API connection details to be configured through environment variables.

Refer to `.env_example` for the required configuration variables.

Required configuration includes:

- Headscale server URL.
- Headscale API authentication key.
- API request timeout.

Never commit real API keys or credentials.

## 4. Docker Compose Deployment

The repository also maintains the Docker Compose configuration for the Headscale server.

Deployment files are located in:

`deployment/headscale/`

The deployment is designed around the existing Headscale installation and preserves its persistent configuration and data.

It includes:

- Docker Compose service definition.
- Pinned Headscale image.
- Example server configuration.
- Persistent configuration and database mounts.
- Health checks and restart policy.
- Deployment documentation.

See [`deployment/headscale/README.md`](deployment/headscale/README.md) for operational instructions.

## 5. Existing Server Migration

The deployment configuration is being prepared to manage the existing Headscale server installation rather than provision a new server.

The migration process is designed to preserve:

- Existing Headscale database.
- Server configuration.
- Noise private key.
- Let's Encrypt certificate cache.
- Existing ACL policy.
- Current Headscale server identity.

A verified backup and rollback procedure must be prepared before replacing the existing Docker container.

**Do not run the Compose deployment against the existing server until the migration procedure has been reviewed and approved.**

## 6. Repository Structure

```text
headscale-integration/
├── cluster_builder/
│   └── infrastructure/
│       └── headscale.py
├── scripts/
│   └── api.sh
├── tests/
│   ├── test_headscale.py
│   └── test_headscale_integration.py
├── deployment/
│   └── headscale/
│       ├── docker-compose.yml
│       ├── config.yaml.example
│       ├── .env.example
│       ├── .gitignore
│       └── README.md
├── .env_example
├── pyproject.toml
└── README.md
```

## 7. Testing

The API integration includes unit and live integration tests.

Run unit tests:

```bash
pytest tests/test_headscale.py -v
```

Run integration tests:

```bash
pytest tests/test_headscale_integration.py -v
```

Integration tests require a reachable Headscale server and valid API credentials.

## 8. Security

- Never commit API keys or private credentials.
- Keep live server configuration and database files outside the repository.
- Protect the Headscale Noise private key.
- Back up persistent data before deployment changes.
- Review ACL policies and access permissions.

## 9. Project Status

The Python Headscale API client has been implemented and tested against the existing Headscale server.

The integration is intended to support VPN management functionality within Cluster Builder.

The Docker Compose deployment configuration is being prepared for a controlled migration of the existing Headscale server.

## 10. Related Project

**[Swarmchestrate Cluster Builder](https://github.com/Swarmchestrate/cluster-builder)**

The Cluster Builder project consumes this integration to incorporate Headscale VPN management into its cluster provisioning and orchestration workflows.

This repository maintains the Headscale-specific API client, automation scripts and server deployment configuration.

The two repositories are maintained separately, with this repository responsible for Headscale-specific API integration and server deployment.
