import { AnimatePresence, motion } from 'framer-motion';
import { useEffect, useState } from 'react';
import { CalendarBookingCard } from './components/booking-card';
import { type BookingItem } from '@/shared/types/types';
import BlockMiniCalendar from '../../shared/components/calendar/mini-calendar';
import axios from 'axios';
import { Spinner } from '@/shared/components/spinner/spinner';
import ErrMessage from '../../shared/components/messages/error-message';
import dayjs from 'dayjs';

export default function CalendarScreen() {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [data, setData] = useState<BookingItem[] | undefined>();

  const [currentMonth, setCurrentMonth] = useState(() => {
    return dayjs().startOf('month')
  });
  const [selectedDate, setSelectedDate] = useState(() => {
    return dayjs().startOf("day")
  });
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<BookingItem[]>(
          `${import.meta.env.VITE_SERVER_IP}/api/bookings/all`,
          {
            headers: {
              Accept: 'application/json',
              Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
            },
          }
        );
        const ResourcesFilteredByDate = response?.data.filter((booking: BookingItem) => {
          return (
            dayjs(booking?.start_time).format("YYYY-MM-DD") === dayjs(selectedDate).format("YYYY-MM-DD")
          );
        });
        setData(ResourcesFilteredByDate)
      } catch (err) {
        setError('Error fetching data. Please try again later.');
        console.error(err)
      } finally {
        setLoading(false);
      }
    };
    fetchData()
  }, [selectedDate])
  return (
    <div className="flex flex-col gap-4 max-h-[calc(100vh-150px)] overflow-y-scroll">
      {/* Текущий месяц */}
      <BlockMiniCalendar
        data={undefined}
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
          {
            error ? (<ErrMessage error={error} />) :
              loading ? (<Spinner />) :
                !loading && !error ?
                  (
                    <CalendarBookingCard
                      selectedDate={selectedDate}
                      setSelectedDate={setSelectedDate}
                      currentMonth={currentMonth}
                      setCurrentMonth={setCurrentMonth}
                      bookings={data}
                    />
                  ) : ""
          }

        </motion.div>
      </AnimatePresence>
    </div>
  );
}
