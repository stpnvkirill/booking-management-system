import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';
import type { BookingItem } from '@/shared/types/types';
import BlockMiniCalendar from '../../shared/components/calendar/mini-calendar';
import axios from 'axios';
// import ErrMessage from '../resources/components/resource-error';
import { Spinner } from '@/shared/components/spinner/spinner';
import ErrMessage from '../../shared/components/messages/error-message';
import dayjs from 'dayjs';
// interface CalendarScreenProps {
//   data: BookingItem | undefined;
// }
export default function CalendarScreen() {
  const currentDateUTC = new Date();
  const utcDatetimeString = currentDateUTC.toISOString();
  console.log(utcDatetimeString);

  // useEffect для получения данных с бд
  // const [activeFilter, setActiveFilter] = useState<Filters | undefined>('Все');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BookingItem | undefined>();

  const [currentMonth, setCurrentMonth] = useState(() => {
    return data?.start_time
      ? dayjs(data.end_time).startOf('month')
      : dayjs().startOf('month');
  });
  const [selectedDate, setSelectedDate] = useState(() => {
    return data?.start_time
      ? dayjs(data.end_time).startOf('day')
      : dayjs().startOf('day');
  });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<BookingItem>(
          `${import.meta.env.VITE_SERVER_IP}/api/bookings/all`,
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

  console.log('CalendarScreen', data);
  return (
    <div className='min-h-[calc(100vh-190px)]'>
      {/* Текущий месяц */}
      <BlockMiniCalendar
        data={data}
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        currentMonth={currentMonth}
        setCurrentMonth={setCurrentMonth}
      />
      <AnimatePresence mode="wait">
        <motion.div
          key={selectedDate.toLocaleString()}
          initial={{ opacity: 0, y: 0 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 0 }}
          transition={{ duration: 0.2 }}
        >
          {error ? (
            <ErrMessage error={error} />
          ) : !data?.id && !loading ? (
            ' '
          ) : (
            ''
          )}
          {loading ? (
            <Spinner />
          ) : !data?.id ? (
            <CalendarBookingCard
              // bookings={} // #TODO переделать получение данных
              selectedDate={selectedDate}
              setSelectedDate={setSelectedDate}
              currentMonth={currentMonth}
              setCurrentMonth={setCurrentMonth}
              bookings={undefined}
            />
          ) : (
            ''
          )}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
