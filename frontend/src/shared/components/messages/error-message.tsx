interface ErrMessageProps {
  error: string | undefined;
}
export default function ErrMessage({ error = '' }: ErrMessageProps) {
  return (
    <div className="text-red-500 text-center">
      Ошибка загрузки данных! <br />
      {error ? error : ''}
    </div>
  );
}
