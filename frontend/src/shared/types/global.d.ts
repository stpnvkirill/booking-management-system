// global.d.ts
import { IStaticMethods } from 'flyonui/flyonui';

declare global {
  interface Window {
    HSStaticMethods: IStaticMethods;
  }
}

export {};
