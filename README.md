# DrugClip Platform

> AI-Powered Virtual Screening Platform for Drug Discovery

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com)

## Overview

DrugClip Platform is a production-grade virtual screening system that combines **DrugCLIP** (a contrastive learning model for protein-ligand binding) with **Morgan Fingerprint pre-screening** to rapidly evaluate millions of compounds against target proteins.

### Key Features

- **Two-Stage Screening Pipeline**: Morgan FP pre-screening → DrugCLIP re-ranking
- **High Performance**: 250+ molecules/second on Apple MPS, 1000+ on CUDA GPU
- **REST API**: FastAPI backend with async job processing
- **Web Dashboard**: React-based UI for job management and result visualization
- **Enterprise Ready**: Multi-tenant architecture, audit logging, SSO support
- **Cloud Native**: Docker + Kubernetes deployment, auto-scaling

### Performance

| Hardware | Speed | 1M Compounds | 10M Compounds |
|----------|-------|--------------|---------------|
| Apple M4 MPS | 250 mol/s | ~67 min | ~11 hrs |
| NVIDIA A100 | 1,200 mol/s | ~14 min | ~2.3 hrs |
| CPU (32-core) | 80 mol/s | ~3.5 hrs | ~35 hrs |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Dashboard (React)                 │
├─────────────────────────────────────────────────────────┤
│                    API Gateway (FastAPI)                  │
├──────────────┬──────────────┬───────────────────────────┤
│  Job Queue   │  Auth/SSO    │  Billing/Metering         │
│  (Celery)    │  (OAuth2)    │  (Stripe)                 │
├──────────────┴──────────────┴───────────────────────────┤
│              Screening Engine (DrugCLIP)                 │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐ │
│  │ FP Pre-screen│  │DrugCLIP Rank│  │ Result Assembly │ │
│  └─────────────┘  └─────────────┘  └─────────────────┘ │
├─────────────────────────────────────────────────────────┤
│  Storage: S3/MinIO │ DB: PostgreSQL │ Cache: Redis      │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for web dashboard)
- Docker (optional, for containerized deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/MoKangMedical/drugclip-platform.git
cd drugclip-platform

# Install Python dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Download DrugCLIP model
python scripts/download_model.py

# Start API server
uvicorn api.main:app --reload --port 8000

# Start web dashboard (in another terminal)
cd web && npm install && npm run dev
```

### Docker Deployment

```bash
docker-compose up -d
```

Access:
- Web Dashboard: http://localhost:3000
- API Docs: http://localhost:8000/docs
- Monitoring: http://localhost:9090 (Prometheus)

## API Usage

### Submit Screening Job

```bash
curl -X POST http://localhost:8000/api/v1/jobs \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -F "protein_file=@target.pdb" \
  -F "ligand_library=@compounds.sdf" \
  -F "config={\"top_k\": 100, \"stage1_threshold\": 0.3}"
```

### Check Job Status

```bash
curl http://localhost:8000/api/v1/jobs/{job_id} \
  -H "Authorization: Bearer YOUR_API_KEY"
```

### Get Results

```bash
curl http://localhost:8000/api/v1/jobs/{job_id}/results \
  -H "Authorization: Bearer YOUR_API_KEY"
```

## Commercial Editions

| Feature | Community | Professional | Enterprise |
|---------|-----------|--------------|------------|
| Core Screening | ✓ | ✓ | ✓ |
| API Access | 100 jobs/mo | Unlimited | Unlimited |
| Web Dashboard | Basic | Full | Full + Custom |
| Batch Processing | 1K compounds | 1M compounds | Unlimited |
| Priority Queue | ✗ | ✓ | ✓ |
| SSO/SAML | ✗ | ✗ | ✓ |
| On-Premise Deploy | ✗ | ✗ | ✓ |
| SLA | Community | 99.9% | 99.99% |
| **Price** | **Free** | **$499/mo** | **Contact Us** |

## Documentation

- [Architecture Guide](docs/architecture/overview.md)
- [API Reference](docs/api/reference.md)
- [Deployment Guide](docs/deployment/docker.md)
- [Contributing Guide](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Citation

If you use this platform in your research, please cite:

```bibtex
@software{drugclip_platform,
  title={DrugClip Platform: AI-Powered Virtual Screening},
  author={MoKangMedical},
  year={2026},
  url={https://github.com/MoKangMedical/drugclip-platform}
}
```
