import { AnimatePresence, motion } from 'framer-motion';
import CalendarBlock from './components/calendar-block';
import { useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';

export default function CalendarScreen() {
  const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  const [bookings, setBookings] = useState<BookingItem[]>([
    {
      id: '0',
      title: 'Loft Noir',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 2900,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '1',
      title: 'Loft Noir2',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 3000,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '2',
      title: 'Cowork Pulse',
      type: 'Работа',
      capacity: 'Дневной доступ',
      location: 'Центр',
      rating: 4.7,
      timeLeft: '8ч',
      price: 1200,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '3',
      title: 'Hall Obsidian',
      type: 'Площадка',
      capacity: '80–120 гостей',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '6ч',
      price: 5400,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '4',
      title: 'Noir Suites',
      type: 'Жильё',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '5',
      title: 'Noir 222 Suites',
      type: 'Работа',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '',
      time: '',
      active: false,
    },
  ]);
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4 h-screen overflow-auto">
        {/* Заголовок */}
        <div className="mb-6">
          <h1 className="text-3xl font-semibold mb-2">Календарь</h1>
          <p className="text-accent-content text-sm">Расписание бронирований</p>
        </div>
        {/* Текущий месяц */}
        <CalendarBlock />
        <AnimatePresence mode="wait">
          <motion.div
            key={selectedDate}
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            <CalendarBookingCard
              bookings={bookings}
              selectedDate={selectedDate}
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
