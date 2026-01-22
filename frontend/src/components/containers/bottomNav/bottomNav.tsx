// import { activeTab, setActiveTab } from '../../../App.tsx'
import Button from "../../small/button/button.tsx";
import { useBookingContext } from "../bookingContext/bookingContext.tsx";

export const BottomNav = () => {
  const { activeTab, setActiveTab } = useBookingContext();
  return (
    <div className="fixed bottom-0 left-0 right-0 flex justify-around p-3 border-t border-base-300 bg-base-200">
      {(["Ресурсы", "Календарь", "Профиль"] as const).map((tab) => (
        <Button
          variant="info"
          key={tab}
          onClick={() => setActiveTab(tab)}
          label={`${tab}`}
          disabled={activeTab == tab}
          shape="text"
          width="responsive"
        />
      ))}
    </div>
  );
};
