import { AnimatePresence, motion } from 'framer-motion';
import ActiveBookingCard from './components/profile-card.tsx';
// import Button from '@/shared/components/button/button';

import CardEmpty from './components/profile-bookings-empty.tsx';
import type { BookingItem } from '@/shared/types/types.tsx';
import ProfileSettings from './components/profile-user-settings.tsx';
// import Header from '@/shared/components/header/header.tsx';

export default function ProfileScreen() {
  // const activeBookings = bookings.filter((b) => b.active);
  const activeBookings: BookingItem[] = [];
  return (
    <>
      {/* Настройки */}
      <ProfileSettings />
      {/* Если нет активных бронирований */}
      {activeBookings.length === 0 ? <CardEmpty /> : ''}
      {/* Список активных карточек */}
      <div className="flex-1 overflow-y-auto pb-24 touch-pan-y scrollbar-hide">
        <div className="flex flex-col gap-4">
          <AnimatePresence>
            {activeBookings.map((booking) => (
              <motion.div
                key={booking?.id}
                initial={{ opacity: 1, height: 'auto' }}
                exit={{
                  opacity: 0,
                  height: 0,
                  marginBottom: 0,
                  overflow: 'hidden',
                }}
                transition={{ duration: 0.3 }}
              >
                <ActiveBookingCard
                  data={booking}
                  onCancel={() => {
                    // handleCancelBooking(booking.id!)
                  }}
                />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>
      </div>
    </>
  );
}
