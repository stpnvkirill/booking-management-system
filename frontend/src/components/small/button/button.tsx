import { type PropsWithChildren } from "react";

export type ButtonVariant = // Варианты стиля
  | "primary"
  | "gradient"
  | "secondary"
  | "tertiary"
  | "info"
  | "success"
  | "error"
  | "warning";
type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";
type ButtonWidth = "full" | "auto" | "responsive";
interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: ButtonVariant;
  size?: ButtonSize;
  width?: ButtonWidth;
  disabled?: boolean;
  isLoading?: boolean;
  isCircle?: boolean;
  className?: string;
  children?: React.ReactNode;
}
const Button = ({
  label,
  children,
  onClick = () => {},
  size = "xs",
  width = "auto",
  variant = "primary",
  disabled = false,
  isLoading = false,
  isCircle = false,
}: PropsWithChildren<ButtonProps>): React.ReactElement => {
  const baseStyles =
    "font-semibold transition-all duration-200 focus:outline-none";
  const shape = isCircle ? "btn-circle" : "rounded-lg";
  const variants: Record<ButtonVariant, string> = {
    primary: "btn-primary",
    tertiary: "btn-tertiary",
    info: "btn-info",
    success: "btn-success",
    error: "btn-error",
    warning: "btn-warning",
    gradient:
      "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 border-none text-white hover:opacity-90",
    secondary: "btn-secondary",
  };
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
      className={`btn ${baseStyles} ${variants[variant]} ${sizes[size]} ${shape}${
        isLoading ? "opacity-70 cursor-not-allowed" : ""
      } ${widths[width]}`}
    >
      {isLoading ? "Loading..." : children || label}
    </button>
  );
};

export default Button;
