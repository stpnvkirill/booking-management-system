interface Theme {
  "color-scheme": string
  "--color-base-100": string
  "--color-base-200": string
  "--color-base-300": string
  "--color-base-content": string
  "--color-primary": string
  "--color-primary-content": string
  "--color-secondary": string
  "--color-secondary-content": string
  "--color-accent": string
  "--color-accent-content": string
  "--color-neutral": string
  "--color-neutral-content": string
  "--color-info": string
  "--color-info-content": string
  "--color-success": string
  "--color-success-content": string
  "--color-warning": string
  "--color-warning-content": string
  "--color-error": string
  "--color-error-content": string
  "--radius-selector": string
  "--radius-field": string
  "--radius-box": string
  "--size-selector": string
  "--size-field": string
  "--border": string
  "--depth": string
  "--noise": string
}


interface Themes {
  black: Theme
  ghibli: Theme
  pastel: Theme
  slack: Theme
  light: Theme
  gourmet: Theme
  marshmallow: Theme
  soft: Theme
  spotify: Theme
  dark: Theme
  luxury: Theme
  valorant: Theme
  shadcn: Theme
  claude: Theme
  vscode: Theme
  mintlify: Theme
  perplexity: Theme
  corporate: Theme
  [key: string]: Theme
}

declare const themes: Themes
export default themes