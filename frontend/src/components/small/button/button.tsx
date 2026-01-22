import { type PropsWithChildren } from "react";
export type ButtonVariant = "primary" | "gradient" | "secondary" | "tertiary" | "info" | "success" | "error" | "warning";
type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
type ButtonWidth = "full" | "auto" | "responsive";
type ButtonShape = "default" | "rounded" | "text" | "outline";
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: ButtonVariant;
  size?: ButtonSize;
  width?: ButtonWidth;
  disabled?: boolean;
  isLoading?: boolean;
  shape?: ButtonShape;
  className?: string;
  children?: React.ReactNode;
}
const Button = ({
  label,
  children,
  onClick = () => { },
  size = "xs",
  width = "auto",
  variant = "primary",
  disabled = false,
  isLoading = false,
  shape = "default",
}: PropsWithChildren<ButtonProps>): React.ReactElement => {
  const baseStyles =
    "font-semibold transition-all duration-200 focus:outline-none";
  const variants: Record<ButtonVariant, string> = {
    primary: "btn-primary",
    tertiary: "btn-tertiary",
    info: "btn-info",
    success: "btn-success",
    error: "btn-error",
    warning: "btn-warning",
    gradient: "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 border-none text-white hover:opacity-90",
    secondary: "btn-secondary",
  };
  const shapes = {
    default: "rounded-lg",
    rounded: "btn-circle",
    text: "btn-text",
    outline: "btn-outline",
  }
  const widths = {
    full: "btn-block",
    auto: "btn-wide",
    responsive: "w-auto pl-3 pr-3",
  };
  const sizes = {
    xs: "btn-xs",
    sm: "btn-sm",
    md: "", //default
    lg: "btn-lg",
    xl: "btn-xl",
  };
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`btn ${baseStyles} ${variants[variant]} ${sizes[size]} ${shapes[shape]}${isLoading ? "opacity-70 cursor-not-allowed" : ""
        } ${widths[width]}`}
    >
      {isLoading ? "Loading..." : children || label}
    </button>
  );
};

export default Button;
