import { type PropsWithChildren } from 'react';
// import Button from '../../small/button/button';
// import { useBookingContext } from '../../../types/bookingContext.tsx';

import type { BookingItem } from '../../../types/bookingContext.tsx';
import { AnimatePresence, motion } from 'framer-motion';
export interface CalendarCardProps {
  bookings?: BookingItem[];
  selectedDate?: string;
}
export const BookingCardCalendar = ({
  bookings,
  selectedDate,
}: PropsWithChildren<CalendarCardProps>): React.ReactElement => {
  // const { setSelectedResource, setActiveTab } = useBookingContext();
  // карточка бронирования на странице с календарем
  //фильтр списка
  const filteredBookings =
    bookings?.filter(
      (booking: BookingItem) => booking.date === selectedDate && booking.active
    ) || [];

  if (bookings !== undefined) {
    return (
      <AnimatePresence mode="popLayout">
        <div>
          <h2 className="text-[16px] font-semibold mb-4">
            Бронирования на {selectedDate}
          </h2>
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
              <div
                key={booking?.id}
                className="bg-base-200 rounded-2xl p-5 mb-4 hover:bg-base-100 duration-200"
              >
                <div className="flex justify-between items-start mb-3">
                  <div>
                    <h3 className="text-lg font-semibold mb-1 text-accent-content">
                      {booking?.title}
                    </h3>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="bg-accent text-accent-content pt-0.5 pb-0.5 pr-2 pl-2 rounded-xl text-xs font-medium">
                        {booking?.type}
                      </span>
                      <span className="text-accent-content text-sm">•</span>
                      <span className="text-accent-content text-sm">
                        {booking?.capacity}
                      </span>
                    </div>
                    {booking?.time && (
                      <div className="text-info text-sm font-medium">
                        ⏰ {booking?.time}
                      </div>
                    )}
                    {/* ⏰ */}
                  </div>
                  <div className="text-right">
                    <div className="text-xl text-accent-content font-bold mb-2">
                      {(booking?.price ?? 0).toLocaleString()} ₽{' '}
                    </div>
                    {/* <Button
                // Нужна ли эта кнопка?
                  label={'Подробнее'}
                  onClick={() => {
                    if (booking !== null) {
                      setSelectedResource(booking!);
                      setActiveTab('Ресурсы');
                    }
                  }}
                  variant="info"
                  size="md"
                ></Button> */}
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
      </AnimatePresence>
    );
  } else {
    return <>data lost...</>;
  }
};
