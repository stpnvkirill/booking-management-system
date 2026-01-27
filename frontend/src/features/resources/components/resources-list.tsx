interface ListProps {
  count: number;
}
export default function List({ count }: ListProps) {
  return (
    <div className="mb-4 text-sm text-secondary">
      Список ({count}{' '}
      {count == 1 || count == 21
        ? 'ресурс'
        : (count >= 2 && count <= 4) || (count >= 22 && count <= 24)
          ? 'ресурса'
          : 'ресурсов'}
      )
    </div>
  );
}
