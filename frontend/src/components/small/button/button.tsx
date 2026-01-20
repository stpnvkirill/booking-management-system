type ButtonVariant = // Варианты стиля
  | "primary"
  | "secondary"
  | "tertiary"
  | "info"
  | "success"
  | "danger"
  | "warning"; 
type ButtonSize = "xs" | "sm" | "md" | "lg" | "xl";

interface ButtonProps {
  label: string;
  onClick: () => void;
  variant?: ButtonVariant;
  size?: ButtonSize; // Варианты размера
  disabled?: boolean; // Состояние блокировки
  isLoading?: boolean; // Состояние загрузки
}
const Button = ({
  label,
  onClick = ()=>{},
  size = "xs",
  variant = "primary",
  disabled = false,
  isLoading = false,
}: ButtonProps): React.ReactElement => {
  const baseStyles =
    "font-semibold rounded transition-all duration-200 focus:outline-none";
  const variants: Record<ButtonVariant, string> = {
    primary: "btn-primary",
    secondary: "btn-secondary",
    tertiary: "btn-tertiary", 
    info: "btn-info",
    success: "btn-success",
    danger: "btn-error",
    warning: "btn-warning",
  };
  const sizes = {
    xs: "btn-xs",
    sm: "btn-sm",
    md: "btn-md", //default 
    lg: "btn-lg",
    xl: "btn-xl",
  };
  return (
    <button
      onClick={onClick}
      disabled={disabled || isLoading}
      className={`btn ${baseStyles} ${variants[variant]} ${sizes[size]} ${
        isLoading ? "opacity-70 cursor-not-allowed" : ""
      }`}
    >
      {isLoading ? "Loading..." : label}
    </button>
  );
};

export default Button;