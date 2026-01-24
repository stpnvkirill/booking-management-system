import Button from '../../small/button/button';
import { ActiveBookingCard } from '../booking-card/booking-card-active';
import { useBookingContext } from '../bookingContext/bookingContext';
import { motion, AnimatePresence } from 'framer-motion';
import { AUTH_CREDENTIALS } from '../auth/authConfig';

export const RenderProfileScreen = () => {
  // eslint-disable-next-line react-hooks/rules-of-hooks
  window.Telegram?.WebApp?.ready();
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;

  const { bookings, handleCancelBooking, setIsAuthenticated } = useBookingContext();
  const activeBookings = bookings.filter(b => b.active);


  return (
    <div className="p-4">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Профиль</h1>
        <p className="text-sm" style={{ color: '#6b7280', fontSize: '14px' }}>
          Личный кабинет
        </p>
      </div>
      {/* Настройки */}
      <div className="mb-8">
        <h2 className="text-base font-semibold mb-4">Настройки</h2>
        <div className="rounded-2xl p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center font-semibold">
              {user?.username || '404'}
            </div>
            <div>
              <div className="text-base font-semibold mb-1">
                {user?.username || AUTH_CREDENTIALS.login}
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full" />
                Уведомления включены
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Активные бронирования */}
      <div className="mb-8">
        <div className="flex gap-3 mb-4">
          <Button
            onClick={() => { }}
            label="Активные"
            variant="primary"
            width="responsive"
            size="md"
            shape="rounded"
          ></Button>
          <Button
            onClick={() => { }}
            label="История"
            variant="secondary"
            width="responsive"
            size="md"
            shape="rounded"
          ></Button>
        </div>
      </div>
      {/* Активное бронирование */}

      {/* Список активных карточек */}
      <div className="flex flex-col gap-4">

        <AnimatePresence>
          {activeBookings.map((booking) => (
            <motion.div
              key={booking.id}
              initial={{ opacity: 1, height: 'auto' }}
              exit={{ opacity: 0, height: 0, marginBottom: 0, overflow: 'hidden' }}
              transition={{ duration: 0.3 }}
            >
              <ActiveBookingCard
                data={booking}
                onCancel={() => handleCancelBooking(booking.id!)}
              />
            </motion.div>
          ))}
        </AnimatePresence>

        {/* {activeBookings.length >= 1 ? (
          
          activeBookings.map((booking) => (
            <ActiveBookingCard
              key={booking.id}
              data={booking}
              onCancel={() => handleCancelBooking(booking.id!)}
            />
          ))
        ) : (
          <p className="text-center text-gray-500">У вас пока нет бронирований</p>
        )} */}
      </div>
      {/* 
      <ActiveBookingCard />
      <ActiveBookingCard />
      <ActiveBookingCard /> */}
      {/* Кнопка выхода */}
      <div className="m-1">
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
  );
};
