# PlantAI — AI Plant Disease Detection Frontend

A polished React + TypeScript + Tailwind prototype for an AI-powered plant disease detection/classification product.

## Run locally

```bash
npm install
npm run dev
```

Then open the Vite URL shown in the terminal.

## Product flow

Dashboard → Analyze Plant → Upload → Choose YOLO/CNN → Mock analysis → Results → Compare → AI Assistant → History.

## Backend integration

All mock inference calls are isolated in `src/services/api.ts`.

Replace these functions with real `fetch` calls:

- `predictYolo()` → `POST /predict/yolo`
- `predictCnn()` → `POST /predict/cnn`
- `askPlantAI()` → `POST /chat`

The UI consumes typed result shapes from `src/types/index.ts`, so backend changes can be handled at the service boundary instead of throughout the UI.

## Design notes

The visual direction is inspired by the supplied Dribbble reference: soft botanical greens, warm neutrals, rounded cards, calm whitespace, and plant-care imagery. It is an original product interface rather than a copy. The reference emphasizes nature-inspired aesthetics, minimalism, clear hierarchy and accessible interactions. 

Demo metrics are explicitly labeled as mock/demo values. Accuracy, precision, recall, F1 and mAP are not fabricated.

## Key components

- `Sidebar`, `Topbar`
- `UploadZone`
- `ModelSelector`
- `LoadingScanner`
- `ResultImage`
- `Confidence`
- Dashboard/stat cards
- YOLO/CNN results
- Comparison dashboard with chart
- PlantAI chatbot
- Analysis history and filters
- Responsive mobile navigation
