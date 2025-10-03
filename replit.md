# EVA: Evolutionary Virtual Android

## Overview
EVA (Evolutionary Virtual Android) is a self-evolving intelligent system designed to observe, learn, adapt, and evolve autonomously. This is a living digital entity built with modular cognition, ethical safeguards, and embodiment-ready architecture.

**GitHub Repository**: https://github.com/evaofo001/E.V.A

## Core Philosophy
- **Evolution over Instruction**: EVA learns through experimentation, mutation, and selection
- **Ethics-First Intelligence**: Every decision passes through a Policy Engine
- **Modular Cognition**: Distributed architecture across multiple languages
- **Synthetic Personality**: Tunable parameters (curiosity, empathy, technicality)
- **Embodiment-Ready**: Designed for future integration with physical robotics

## Project Architecture

### Frontend (React + TypeScript)
- **Framework**: Vite + React + TypeScript
- **Port**: 5000
- **Components**:
  - Chat Interface with EVA
  - Real-time messaging system
  - Status monitoring
- **Location**: `/frontend`

### Backend (Python)
- **Framework**: FastAPI
- **Port**: 8000 (localhost)
- **Components**:
  - EVA Core Orchestrator
  - Policy Engine (Ethics & Safety)
  - REST API for chat interactions
- **Location**: `/backend`

### Evolution Cycle
EVA operates on a continuous 5-phase loop:
1. **Perception** 👁️ - Collects data from user input
2. **Memory** 🧠 - Stores and integrates data
3. **Learning** 📚 - Discovers patterns and insights
4. **Experimentation** 🧪 - Tests new behaviors safely
5. **Output** 📤 - Communicates and takes action

## Project Structure
```
.
├── frontend/               # React + TypeScript frontend
│   ├── src/
│   │   ├── App.tsx        # Main EVA chat interface
│   │   └── App.css        # EVA styling
│   ├── vite.config.ts     # Vite configuration (port 5000)
│   └── package.json
├── backend/               # Python backend
│   ├── eva_core/
│   │   ├── orchestrator.py    # EVA Core Orchestrator
│   │   └── policy_engine.py   # Ethics & Safety Engine
│   ├── api/
│   │   └── main.py           # FastAPI server
│   └── requirements.txt
├── README.md
└── .replit
```

## Setup Status
- ✅ **Frontend**: React + TypeScript with Vite (running on port 5000)
- ✅ **Backend**: Python FastAPI with EVA Core (port 8000)
- ✅ **Workflow**: Frontend development server configured
- ⏳ **Database**: PostgreSQL setup required (manual configuration in Replit UI)

## Database Setup (Manual Required)
EVA requires a PostgreSQL database for knowledge storage. To set up:
1. Open the Replit Database tool
2. Click "Create a database"
3. Connection credentials will be automatically saved as environment variables:
   - `DATABASE_URL`
   - `PGHOST`, `PGUSER`, `PGPASSWORD`, `PGDATABASE`, `PGPORT`

## Running EVA

### Development Mode
The frontend is already running via the configured workflow on port 5000.

### Backend API (Optional)
To run the backend API separately:
```bash
cd backend
python -m api.main
```

## Foundational Knowledge Modules
EVA is seeded with core "digital instincts":
- **Learning Framework**: Reinforcement logic, pattern recognition
- **Understanding Engine**: Natural language processing
- **Ethics & Safety Core**: Policy Engine, emergency protocols
- **Response Generator**: Personality parameters and tone modulation
- **Decision-Making Engine**: Rule-based logic with ethical filters
- **Memory Structure**: Knowledge graph with semantic tagging

## Current Features
- ✅ Chat interface with EVA
- ✅ Synthetic personality system
- ✅ Ethics and Policy Engine
- ✅ Real-time messaging
- ✅ Status monitoring
- ✅ Multi-language architecture (Rust, C++, Python, TypeScript)
- ✅ Training/Learning pipeline - EVA learns from conversations
- ✅ C++ Perception module for performance
- 🚧 Rust Policy Engine (compiled, integration pending)
- 🚧 Knowledge graph integration (pending database)
- 🚧 Full multi-language integration (in progress)

## Future Roadmap
- **Short-Term**: Finalize ethical ruleset and decision tree
- **Mid-Term**: Deploy in virtual environments (games, simulations)
- **Long-Term**: Integrate with physical robotics for embodiment

## Recent Changes
- **2025-10-03**: Multi-language architecture and learning systems
  - **Phase 1: Initial Setup**
    - Created React + TypeScript frontend with Vite
    - Built Python FastAPI backend with EVA Core Orchestrator
    - Configured Vite for Replit proxy (port 5000, host 0.0.0.0)
    - Implemented basic chat interface with EVA
    - Set up Policy Engine for ethical decision-making
  
  - **Phase 2: OpenAI Integration**
    - Added workflows for frontend and backend servers
    - Integrated OpenAI API (gpt-4o-mini) for intelligent responses
    - Added openai package to backend requirements
    - Fixed API response schema to match FastAPI validation
    - Fixed network binding for Replit environment (0.0.0.0)
    - Verified end-to-end chat functionality
  
  - **Phase 3: Multi-Language Architecture**
    - Installed Rust (1.88.0), C++ (GCC 14.2.1), C (Clang 19.1.7) toolchains
    - Created project structure: rust_modules/, cpp_modules/, proto/
    - Defined Protobuf schemas for cross-language communication
    - Built Rust-based Policy Engine with PyO3 bindings
    - Created C++ Perception module with sentiment analysis
    - Implemented Python Training Pipeline for continual learning
    - EVA now learns patterns from conversations autonomously
    - Added API endpoints for learning insights (/learning/insights, /learning/patterns)
