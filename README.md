# 🏎️ F1 Race Replay 🏎️
![example workflow](https://github.com/jamie005/f1-race-replay/actions/workflows/ci.yml/badge.svg)

A full-stack application for visualising and replaying Formula 1 race telemetry data. It features a real-time 3D race viewer built with React, Cesium and Resium, allowing users to spectate races from any angle. The Dockerised backend Python service ingests F1 session data using the FastF1 library, before serialising it using Protobuf and 
streaming it using Kafka.

## Utilised Technologies

![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Poetry](https://img.shields.io/badge/Poetry-%233B82F6.svg?style=for-the-badge&logo=poetry&logoColor=0B3D8D)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Apache Kafka](https://img.shields.io/badge/Apache%20Kafka-000?style=for-the-badge&logo=apachekafka)
![Nx](https://img.shields.io/badge/nx-143055?style=for-the-badge&logo=nx&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Docker Compose](https://img.shields.io/badge/Docker%20Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)

## Screenshots
![Screenshot](./img/screenshot2.png)
![Screenshot](./img/screenshot1.png)
![Screenshot](./img/screenshot3.png)

## Project Setup

### Prerequisites
- VS Code
- [VS Code Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

### Steps

1. Within VSCode, open the command pallette then run "Dev Containers: Reopen in Container"

2. Lint, test, and build each project:
   ```sh
   nx run-many -t lint test e2e build container
   ```
3. Run the F1 Race Replay stack:
   ```sh
   docker compose up -d
   ```
4. Access the F1 Race Viewer from: http://localhost:80

## Disclaimer

This repository is not associated in any way with the Formula 1 companies. F1, FORMULA ONE, FORMULA 1, FIA FORMULA ONE WORLD CHAMPIONSHIP, GRAND PRIX and related marks are trade marks of Formula One Licensing B.V.
