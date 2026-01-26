import React, { useState } from 'react';

type InputVariant = 'default' | 'success' | 'error';

type InputSize = 'xs' | 'sm' | 'md' | 'lg' | 'xl';
interface InputProps {
  value?: string;
  onChange?: ((e: React.ChangeEvent<HTMLInputElement>) => void) | undefined;
  placeholder?: string;
  variant?: InputVariant;
  size?: InputSize;
  disabled?: boolean;
  type?: React.HTMLInputTypeAttribute;
  label?: string;
  id?: string;
  isFloating?: boolean;
  span?: string;
  className?: string;
}
const Input = ({
  label,
  id,
  placeholder,
  variant = 'default',
  size = 'md',
  disabled = false,
  isFloating = false,
  span,
  onChange,
  value,
  // type = 'text',
  className = '',
  ...props
}: InputProps): React.ReactElement => {
  const [internalValue, setInternalValue] = useState('');
  const controlledValue = value !== undefined ? value : internalValue;
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    // Обновляем внутренний стейт
    setInternalValue(e.target.value);
    // Вызываем внешний onChange, если он был передан
    if (onChange) {
      onChange(e);
    }
  };

  const baseStyles =
    'input font-medium transition-all duration-200 focus:outline-none';
  const variants: Record<InputVariant, string> = {
    default: '',
    success: 'is-valid',
    error: 'is-invalid',
  };
  const sizes: Record<InputSize, string> = {
    xs: 'input-xs',
    sm: 'input-sm',
    md: '', //default
    lg: 'input-lg',
    xl: 'input-xl',
  };

  const combinedClasses = `${baseStyles} ${variants[variant]} ${sizes[size]} ${className}`;

  const floatingInputClasses = `${combinedClasses} bg-base-100 p-3 rounded-xl border border-white/5 focus:outline-accent`;

  if (isFloating) {
    return (
      <>
        <div className="input-floating max-w-sm">
          <input
            id={id}
            value={controlledValue}
            placeholder={`${placeholder}`}
            disabled={disabled}
            onChange={handleChange}
            {...props}
            className={floatingInputClasses}
          />
          <label className="input-floating-label" htmlFor={`${id}`}>
            {label}
          </label>
          <span className="helper-text ps-3">{span}</span>
        </div>
      </>
    );
  }
  return (
    <>
      <div className="max-w-sm">
        <label className="label-text" htmlFor={`${id}`}>
          {label}
        </label>
        <input
          id={id}
          value={controlledValue}
          type="text"
          className={combinedClasses}
          placeholder={`${placeholder}`}
          disabled={disabled}
          onChange={handleChange}
          {...props}
        />
        <span className="helper-text">{span}</span>
      </div>
    </>
  );
};

export default Input;
