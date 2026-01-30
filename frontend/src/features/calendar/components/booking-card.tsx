import { type PropsWithChildren } from 'react';
import type { BookingItem } from '@/shared/types/types';
import { AnimatePresence, motion } from 'framer-motion';
import { monthNames } from '@/shared/types/constants';
import type dayjs from 'dayjs';
import { GetDD_MM_YYYY } from '@/shared/types/functions';
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
  // setSelectedDate,
  // currentMonth,
  // setCurrentMonth
}: PropsWithChildren<CalendarCardProps>): React.ReactElement => {
  console.log(bookings);
  // const { setSelectedResource, setActiveTab } = useBookingContext();
  // карточка бронирования на странице с календарем
  //фильтр списка
  const filteredBookings =
    bookings?.filter(
      (booking: BookingItem) =>
        GetDD_MM_YYYY(booking.start_time) ===
          selectedDate.format('YYYY-MM-DD').toString() && booking.end_time
    ) || [];
  console.log('booking-card', bookings);

  const getDDMMDateFromUTCString = (utcString: string | undefined): string => {
    if (!utcString) {
      return 'Дата не указана';
    }
    const dateObject = new Date(utcString);
    const day = dateObject.getDate();
    const year = dateObject.getFullYear();

    const month = monthNames[dateObject.getMonth()];
    return `${day} ${month} ${year} г.`;
  };
  console.log(selectedDate.format('DD-MM-YYYY').toString());
  return (
    <AnimatePresence mode="popLayout">
      <h2 className="text-[16px] font-semibold mb-4">
        Бронирования на {selectedDate.format('DD-MM-YYYY').toString()}
      </h2>
      <div className="mb-8">
        <div className="flex flex-col justify-start overflow-y-scroll max-h-[calc(100vh-450px)] pb-6">
          {filteredBookings.map((booking) => (
            <motion.div
              key={booking.id}
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
                    {booking?.id}
                  </h3>
                  <div className="flex items-center gap-2 mb-2">
                    <span className="bg-accent text-accent-content pt-0.5 pb-0.5 pr-2 pl-2 rounded-xl text-xs font-medium">
                      {booking?.resource_name}
                    </span>
                    <span className="text-accent-content text-sm">•</span>
                    <span className="text-accent-content text-sm">
                      {booking?.resource_name}
                    </span>
                  </div>
                  {booking?.start_time && (
                    <div className="text-info text-sm font-medium">
                      ⏰ {getDDMMDateFromUTCString(booking?.start_time)}
                    </div>
                  )}
                  {/* ⏰ */}
                </div>
                <div className="text-right">
                  <div className="text-xl text-accent-content font-bold mb-2">
                    {/* {(booking?.price ?? 0).toLocaleString()} ₽ */} {'Цена'}
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
          {filteredBookings.length === 0 && (
            <motion.p
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-gray-500 italic"
            >
              На этот день бронирований нет.
            </motion.p>
          )}
        </div>
      </div>
    </AnimatePresence>
  );
};
