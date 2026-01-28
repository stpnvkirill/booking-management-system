import { AnimatePresence, motion } from 'framer-motion';
import { useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';
import type { BookingItem } from '@/shared/types/types';
import BlockMiniCalendar from '../mini-calendar/mini-calendar';
interface CalendarScreenProps {
  data: BookingItem | undefined;
}
export default function CalendarScreen({ data }: CalendarScreenProps) {
  const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  // useEffect для получения данных с бд
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4 h-screen overflow-auto">
        {/* Заголовок */}
        <div className="mb-6">
          <h1 className="text-3xl font-semibold mb-2">Календарь</h1>
          <p className="text-accent-content text-sm">Расписание бронирований</p>
        </div>
        {/* Текущий месяц */}
        <BlockMiniCalendar
          selectedDate={selectedDate}
          setSelectedDate={setSelectedDate}
          data={data}
        />
        <AnimatePresence mode="wait">
          <motion.div
            key={selectedDate}
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            <CalendarBookingCard bookings={data} selectedDate={selectedDate} />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
