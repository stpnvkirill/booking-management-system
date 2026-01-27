import Button from '@/shared/components/button/button';
const TABS = ['resources', 'calendar', 'profile'] as const;
type TabName = (typeof TABS)[number];
interface NavbarProps {
  activeTab: TabName;
  setActiveTab: React.Dispatch<React.SetStateAction<TabName>>;
}
export default function Navbar({ activeTab, setActiveTab }: NavbarProps) {
  return (
    <div className="fixed bottom-0 left-0 right-0 flex justify-around p-3 border-t border-base-300 bg-base-200">
      {TABS.map((tab) => (
        <Button
          variant="info"
          key={tab}
          onClick={() => {
            setActiveTab(tab);
          }}
          label={`${tab == 'resources' ? 'Ресурсы' : tab == 'calendar' ? 'Календарь' : tab == 'profile' ? 'Профиль' : ''}`}
          disabled={activeTab == tab}
          shape="text"
          width="responsive"
        />
      ))}
    </div>
  );
}
