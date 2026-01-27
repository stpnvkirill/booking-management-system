interface HeaderProps {
  title: string;
}
export default function Header({ title }: HeaderProps) {
  return (
    <div className="mb-6">
      <h1 className="text-3xl text-neutral font-bold mb-2">{title}</h1>
      <p className="text-base-300 text-sm">Ресурсы</p>
    </div>
  );
}
