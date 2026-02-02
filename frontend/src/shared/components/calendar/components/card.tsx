type CardVariant = 'default' | 'primary' | 'secondary' | 'accent';
type CardShape = 'rounded-lg' | 'rounded-xl' | 'rounded-2xl' | 'rounded-none';

interface CardProps {
  children: React.ReactNode;
  title?: string;
  extra?: React.ReactNode;
  variant?: CardVariant;
  shape?: CardShape;
  className?: string; // Для добавления любых кастомных классов извне
}
export default function Card({
  children,
  title,
  extra,
  variant = 'default', // По умолчанию - стандартный фон
  shape = 'rounded-xl', // По умолчанию - среднее скругление
  className = '',
}: CardProps) {
  const variantClasses: Record<CardVariant, string> = {
    default: 'bg-base-100 border-base-200', // Стандартный светлый/темный фон темы
    primary: 'bg-primary text-primary-content', // Основной цвет с контрастным текстом
    secondary: 'bg-secondary text-secondary-content', // Вторичный цвет
    accent: 'bg-accent text-accent-content', // Акцентный цвет
  };
  const cardClasses = `card shadow-sm border ${variantClasses[variant]} ${shape} ${className}`;
  return (
    <div className={`${cardClasses}`}>
      <div className="card-body p-5">
        {(title || extra) && (
          <div className="flex justify-between items-center mb-4 text-neutral">
            {title && <h2 className="card-title font-semibold">{title}</h2>}
            {extra && <div className="text-primary font-medium">{extra}</div>}
          </div>
        )}
        {children}
      </div>
    </div>
  );
}
