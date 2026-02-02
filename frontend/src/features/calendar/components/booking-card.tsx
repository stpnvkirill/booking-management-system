import { useEffect, useState, type PropsWithChildren } from 'react';
import type { BookingItem, ResourceItem } from '@/shared/types/types';
import { AnimatePresence, motion } from 'framer-motion';
import dayjs from 'dayjs';
import axios from 'axios';
import { Spinner } from '@/shared/components/spinner/spinner';
import ErrMessage from '@/shared/components/messages/error-message';
import { firstBigLetter } from '@/shared/types/functions';
export interface CalendarCardProps {
  bookings: BookingItem[] | undefined;
  selectedDate: dayjs.Dayjs;
  setSelectedDate: React.Dispatch<React.SetStateAction<dayjs.Dayjs>>;
  currentMonth: dayjs.Dayjs;
  setCurrentMonth: React.Dispatch<React.SetStateAction<dayjs.Dayjs>>;
}
export const CalendarBookingCard = ({
  bookings,
  selectedDate,
}: PropsWithChildren<CalendarCardProps>) => {
  const [resources, setResources] = useState<ResourceItem[]>()
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    setResources(undefined)
    setLoading(true)
    setError(null)
    // console.log("Дата выбрана:", selectedDate.format('DD-MM-YYYY').toString())
    const fetchAllResources = async () => {
      if (!bookings || bookings.length === 0) {
        setLoading(false);
        return;
      }
      try {
        const requests = bookings.map(booking =>
          axios.get<ResourceItem>(
            `${import.meta.env.VITE_SERVER_IP}/api/resources/${booking.resource_id}`,
            {
              headers: {
                Accept: 'application/json',
                Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
              },
            }
          )
        )
        const responses = await Promise.all(requests);
        const resourceData = responses.map(res => res.data);
        setResources(resourceData)
      } catch (err) {
        console.error(err);
        setError(String(err));
      } finally {
        setLoading(false);
      }
    }
    fetchAllResources()
  }, [selectedDate, bookings])
  return (
    <AnimatePresence mode="popLayout">
      <h2 className="text-[16px] font-semibold mb-4">
        Бронирования на {selectedDate.format('DD-MM-YYYY').toString()}
      </h2>
      <div className="flex flex-col justify-start overflow-y-scroll max-h-[calc(100vh-250px)]">
        <div className="">
          {
            loading ? <Spinner /> :
              error ? <ErrMessage error={error} /> :
                typeof resources == 'undefined' ? (
                  <motion.p
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-gray-500 italic"
                  >
                    Ha этот день бронирований нет.
                  </motion.p>
                ) :
                  resources != undefined && resources.length != 0 && !loading && !error ?
                    (
                      resources.map((res, i) => {
                        return (
                          <motion.div
                            key={res.id}
                            layout
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, scale: 1 }}
                            transition={{ duration: 0.2 }}
                            className="bg-base-200 rounded-2xl p-5 mb-4 hover:bg-base-100 duration-200"
                          >
                            <div className="flex justify-between items-start mb-3">
                              <div className="text-left">
                                <h3 className="text-lg font-semibold mb-1 text-accent-content">
                                  {firstBigLetter(res.name)}
                                </h3>
                                <div className="flex items-center gap-2 mb-2">
                                  <span className="bg-accent text-accent-content pt-0.5 pb-0.5 pr-2 pl-2 rounded-xl text-xs font-medium">{firstBigLetter(res.resource_type)}</span>
                                  <span className="text-accent-content text-sm">•</span>
                                  <span className="text-accent-content text-sm">{firstBigLetter(res.description)}</span>
                                </div>
                                <div className="text-info text-sm font-medium">
                                  ⏰ {dayjs(bookings![i].start_time).format("HH:mm")}-{dayjs(bookings![i].end_time).format("HH:mm")}
                                </div>
                              </div>
                              <div className="text-right">
                                <div className="text-xl text-accent-content font-bold mb-2">
                                  {(res.price_per_hour ?? 0).toLocaleString()} ₽
                                </div>
                              </div>
                            </div>
                          </motion.div>
                        )
                      })
                    ) : ""
          }
        </div>
      </div >
    </AnimatePresence >
  );
};

