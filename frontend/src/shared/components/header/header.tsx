interface HeaderProps {
  title: string;
  subtitle: string;
  children: React.ReactNode | undefined;
}
export default function Header({
  title,
  subtitle,
  children = '',
}: HeaderProps) {
  return (
    <div className="mb-6 flex-none ">
      <div className="flex flex-row justify-between">
        <div>
          <h1 className="text-3xl text-neutral font-bold mb-2">{title}</h1>
          <p className="text-base-300 text-sm ml-1">{subtitle}</p>
        </div>
        {children ? <div>{children}</div> : ''}
      </div>
    </div>
  );
}
