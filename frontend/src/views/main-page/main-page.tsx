// import reactLogo from './assets/react.svg'
// import reactLogo from '../../assets/react.svg'
// import viteLogo from '/vite.svg'
// import './App.css'
import {
  ResourceDetails,
  ResourcesScreen,
} from '../../components/containers/resource/resource.tsx';
import { Calendar } from '../../components/containers/calendar/calendar.tsx';
import { RenderProfileScreen } from '../../components/containers/profile/profile.tsx';
import { BottomNav } from '../../components/containers/bottomNav/bottomNav.tsx';
//import {BottomNav} from '../../components/containers/bottomNav/bottomNav.tsx'
// import {type  FilterType,  type BookingItem , type TimeSlot} from '../../App.tsx'
// import {activeTab, setSelectedResource,  selectedTimeSlot, selectedResource} from '../../App.tsx'
import { useBookingContext } from '../../types/bookingContext.tsx';
import { motion, AnimatePresence } from 'framer-motion';
import { AuthContainer } from '../../types/auth/auth.tsx';

const pageVariants = {
  initial: { opacity: 0, x: 0 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 0 },
};

export interface BookingItem {
  id: string;
  title: string;
  type: 'Площадка' | 'Работа' | 'Жильё';
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
  | 'Все'
  | 'Площадка'
  | 'Работа'
  | 'Здоровье'
  | 'Авто'
  | 'Жильё';

export function MainPage() {
  const { isAuthenticated } = useBookingContext();
  console.log('Status Auth:', isAuthenticated);

  const { activeTab, selectedResource } = useBookingContext();

  if (!isAuthenticated) {
    return (
      <div className="fixed inset-0 z-9999 flex items-center justify-center bg-neutral-content">
        <AuthContainer />
      </div>
    );
  }
  return (
    <div className="bg-neutral-content text-neutral min-h-screen font-sans">
      {/* Контент в зависимости от выбранного таба */}
      <div className="pb-20">
        <AnimatePresence mode="wait">
          <motion.div
            key={selectedResource ? 'details' : activeTab} // Ключ для анимки, без него не ворк
            initial="initial"
            animate="animate"
            exit="exit"
            variants={pageVariants}
            transition={{ duration: 0.2 }}
          >
            {selectedResource ? (
              <ResourceDetails />
            ) : activeTab === 'Ресурсы' ? (
              <ResourcesScreen />
            ) : activeTab === 'Календарь' ? (
              <Calendar />
            ) : (
              <RenderProfileScreen />
            )}
          </motion.div>
        </AnimatePresence>
      </div>
      {/* Нижняя навигация */}
      {!selectedResource && <BottomNav />}
    </div>
  );
}
