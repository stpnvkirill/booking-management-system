// import reactLogo from './assets/react.svg'
// import reactLogo from '../../assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import {
  ResourceDetails,
  ResourcesScreen,
} from "../../components/containers/resource/resource.tsx";
import { Calendar } from "../../components/containers/calendar/calendar.tsx";
import { renderProfileScreen } from "../../components/containers/profile/profile.tsx";
import { BottomNav } from "../../components/containers/bottomNav/bottomNav.tsx";
//import {BottomNav} from '../../components/containers/bottomNav/bottomNav.tsx'
// import {type  FilterType,  type BookingItem , type TimeSlot} from '../../App.tsx'
// import {activeTab, setSelectedResource,  selectedTimeSlot, selectedResource} from '../../App.tsx'
import { useBookingContext } from "../../components/containers/bookingContext/bookingContext.tsx";

export interface BookingItem {
  id: string;
  title: string;
  type: "Площадка" | "Работа" | "Жильё";
  capacity?: string;
  location: string;
  rating: number;
  timeLeft?: string;
  price: number;
  date?: string;
  time?: string;
  active?: boolean;
}

export interface TimeSlot {
  time: string;
  available: boolean;
}

export type FilterType =
  | "Все"
  | "Площадки"
  | "Работа"
  | "Здоровье"
  | "Авто"
  | "Жильё";

export function MainPage() {
  // Основной стиль приложения
  const appStyle: React.CSSProperties = {
    backgroundColor: "#0a0a0a",
    color: "#ffffff",
    minHeight: "100vh",
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  };
  const { activeTab, selectedResource } = useBookingContext();
  return (
    <div style={appStyle}>
      {/* Контент в зависимости от выбранного таба */}
      <div style={{ paddingBottom: "80px" }}>
        {selectedResource
          ? ResourceDetails()
          : activeTab === "Ресурсы"
            ? ResourcesScreen()
            : activeTab === "Календарь"
              ? Calendar()
              : renderProfileScreen()}
      </div>
      {/* Нижняя навигация */}
      {!selectedResource && BottomNav()}
    </div>
  );
}
