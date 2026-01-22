import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./styles/App.css";
import App from "./App.tsx";
// import { plugin } from "postcss";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App></App>
  </StrictMode>,
);
