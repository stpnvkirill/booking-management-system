import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';
import type { ResourceItem } from '@/shared/types/types';
import BlockMiniCalendar from '../../shared/components/calendar/mini-calendar';
import axios from 'axios';
// import ErrMessage from '../resources/components/resource-error';
import { Spinner } from '@/shared/components/spinner/spinner';
import ErrMessage from '../../shared/components/messages/error-message';
import Message from '@/shared/components/messages/message';
// interface CalendarScreenProps {
//   data: ResourceItem | undefined;
// }
export default function CalendarScreen() {
  const currentDateUTC = new Date();
  const utcDatetimeString = currentDateUTC.toISOString();
  console.log(utcDatetimeString);
  // const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  const [selectedDate, setSelectedDate] = useState<string>(utcDatetimeString);

  // useEffect для получения данных с бд
  // const [activeFilter, setActiveFilter] = useState<Filters | undefined>('Все');
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<ResourceItem[] | undefined>([]);
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<ResourceItem[]>(
          `${import.meta.env.VITE_SERVER_IP}/api/resources/all`,
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
    <>
      {/* Текущий месяц */}
      <BlockMiniCalendar
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        data={data}
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
          ) : data?.length == 0 && !loading ? (
            <Message message="Нет доступных бронирований" />
          ) : (
            ''
          )}
          {loading ? (
            <Spinner />
          ) : data?.length != 0 ? (
            <CalendarBookingCard
              bookings={[]} // #TODO переделать получение данных
              selectedDate={selectedDate}
            />
          ) : (
            ''
          )}
        </motion.div>
      </AnimatePresence>
    </>
  );
}
