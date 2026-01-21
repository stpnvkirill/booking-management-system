import {  type PropsWithChildren } from "react";

export type ButtonVariant = // Варианты стиля
  | "primary"
  |"gradient"
  | "secondary"
  | "tertiary"
  | "info"
  | "success"
  | "error"
  | "warning";
type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: ButtonVariant;
  size?: ButtonSize; // Варианты размера
  disabled?: boolean; // Состояние блокировки
  isLoading?: boolean; // Состояние загрузки
  isCircle?: boolean;
  className?: string;
  children?: React.ReactNode; 
}
const Button = ({
  label,
  children,
  onClick = () => {},
  size = "xs",
  variant = "primary",
  disabled = false,
  isLoading = false,
  isCircle = false
}: PropsWithChildren<ButtonProps>): React.ReactElement => {
  const baseStyles =
    "btn-block font-semibold transition-all duration-200 focus:outline-none";
    
    const shape = isCircle ? "btn-circle" : "rounded-lg";
  const variants: Record<ButtonVariant, string> = {
    primary: "btn-primary",
    gradient: "bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 border-none text-white hover:opacity-90",
    secondary: "btn-secondary",
    tertiary: "btn-tertiary",
    info: "btn-info",
    success: "btn-success",
    error: "btn-error",
    warning: "btn-warning",
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
      }`}
    >
      {isLoading ? "Loading..." : (children || label)}
    </button>
  );
};

export default Button;
