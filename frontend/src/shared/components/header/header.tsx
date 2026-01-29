interface HeaderProps {
  title: string;
  subtitle: string;
}
export default function Header({ title, subtitle }: HeaderProps) {
  return (
    <div className="mb-6">
      <h1 className="text-3xl text-neutral font-bold mb-2">{title}</h1>
      <p className="text-base-300 text-sm">{subtitle}</p>
    </div>
  );
}
