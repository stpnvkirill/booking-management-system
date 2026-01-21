import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

 import "./styles/App.css";
// import App from "./App.tsx";
import {App4} from './views/main-page/main-page.tsx'

import {BookingProvider} from './components/containers/bookingContext/bookingContext.tsx'
import { plugin } from "postcss";




createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <BookingProvider>
    { <App4 /> }
    
    </BookingProvider>
  </StrictMode>
);
