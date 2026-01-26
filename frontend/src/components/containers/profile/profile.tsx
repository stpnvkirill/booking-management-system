import Button from '../../small/button/button';
import { ActiveBookingCard } from '../booking-card/booking-card-active';
import { useBookingContext } from '../../../types/bookingContext';
import { motion, AnimatePresence } from 'framer-motion';
import { AUTH_CREDENTIALS } from '../../../types/auth/authConfig.tsx';
import { useState } from 'react';

export const RenderProfileScreen = () => {
  window.Telegram?.WebApp?.ready();
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;

  const { bookings, handleCancelBooking, setIsAuthenticated } =
    useBookingContext();
  const activeBookings = bookings.filter((b) => b.active);
  const [isChecked, setIsChecked] = useState(true);
  const handleChange = () => {
    setIsChecked((prev) => !prev);
  };
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="fixed inset-0 p-4 flex flex-col overflow-hidden bg-neutral-content">
        {/* Заголовок */}

        <div className="flex-none">
          <div className="flex justify-between mb-8">
            <div className="mb-2 mt-2">
              <h1 className="text-3xl font-bold mb-2">Профиль</h1>
              <p className="text-sm text-base-300">Личный кабинет</p>
            </div>
            <div className="mb-2 mt-2">
              <Button
                label={'Выйти'}
                shape="outline"
                variant="error"
                size="lg"
                width="full"
                onClick={() => setIsAuthenticated(false)}
              ></Button>
            </div>
          </div>
          {/* Настройки */}
          <div className="mb-8">
            <div className="bg-base-200 rounded-2xl p-5 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center font-semibold">
                  {user?.photo_url ? (
                    <img
                      className="rounded-full"
                      src={user?.photo_url}
                      alt={user?.photo_url || '404'}
                    />
                  ) : user?.first_name && user?.last_name ? (
                    `${user?.first_name?.charAt(0) || ''} ${user?.last_name?.charAt(0) || ''}`
                  ) : (
                    `404`
                  )}
                </div>
                <div>
                  <div className="text-base font-semibold mb-1">
                    {user?.username || AUTH_CREDENTIALS.login}
                  </div>
                  <div className="flex items-center text-sm">
                    <input
                      type="checkbox"
                      className="checkbox checkbox-primary mr-2"
                      onChange={handleChange}
                      checked={isChecked}
                    />
                    <span className="text-base">
                      {isChecked
                        ? 'Уведомления включены'
                        : 'Уведомления выключены'}
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        {/* Список активных карточек */}
        {activeBookings.length === 0 ? (
          <div className="skeleton-striped flex w-full items-center justify-center min-h-[calc(100vh-350px)] border-none rounded-box border p-4 overflow-y-auto">
            <p className="text-center text-neutral mt-1 mb-1">
              У вас нет активных бронирований.
            </p>
          </div>
        ) : (
          ''
        )}
        <div className="flex-1 overflow-y-auto pb-24 touch-pan-y scrollbar-hide">
          <div className="flex flex-col gap-4">
            <AnimatePresence>
              {activeBookings.map((booking) => (
                <motion.div
                  key={booking.id}
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
                    onCancel={() => handleCancelBooking(booking.id!)}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
};
