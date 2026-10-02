# Frontend Agent Guidelines: Portfolio Copilot

## Project Overview
Next.js 14+ (App Router) frontend interface for the Kensington Manor Property Management Copilot. Communicates with a FastAPI backend running on `http://127.0.0.1:8000`.

## Architecture & Tech Stack
* **Framework**: Next.js with App Router (`app/page.tsx`)
* **Styling**: Tailwind CSS
* **Icons**: `lucide-react`
* **State Management**: React `useState`, `useEffect`, `useRef` for auto-scrolling chat history.

## API Integration Specs
* **Endpoint**: `http://127.0.0.1:8000/api/chat`
* **Method**: `POST`
* **Request Payload**:
  ```json
  {
    "message": "string"
  }