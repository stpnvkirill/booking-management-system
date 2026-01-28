import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';
import type { BookingItem, Filters } from '@/shared/types/types';
import BlockMiniCalendar from '../mini-calendar/mini-calendar';
import axios from 'axios';
// import ErrMessage from '../resources/components/resource-error';
import { Spinner } from '@/shared/components/spinner/spinner';
// interface CalendarScreenProps {
//   data: BookingItem | undefined;
// }
export default function CalendarScreen() {
  const currentDateUTC = new Date();
  const utcDatetimeString = currentDateUTC.toISOString();
  console.log(utcDatetimeString)
  // const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  const [selectedDate, setSelectedDate] = useState<Date | string>(utcDatetimeString);

  // useEffect для получения данных с бд
  const [activeFilter, setActiveFilter] = useState<Filters | undefined>('Все');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BookingItem[]>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<BookingItem[]>(
          'http://localhost:88/api/bookings/all/',
          {
            headers: {
              Accept: 'application/json',
              Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
            },
          }
        );
        setData(response?.data);
      } catch (err) {
        setError('Error fetching data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  console.log("CalendarScreen", data)
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
            {error ? <div className="text-red-500 text-center">Ошибка загрузки данных!</div> : ''}
            {loading ? (
              <Spinner />
            ) : data.length != 0 ? (<CalendarBookingCard bookings={data} selectedDate={selectedDate} />) : ""}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
