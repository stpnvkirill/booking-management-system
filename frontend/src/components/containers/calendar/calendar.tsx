// import { selectedDate, setSelectedDate, setSelectedResource, setActiveTab } from '../../../App.tsx'
import { useBookingContext } from '../../../types/bookingContext.tsx';
import Button from '../../small/button/button.tsx';
import { BookingCardCalendar } from '../booking-card/booking-card-calendar.tsx';
import { motion, AnimatePresence } from 'framer-motion';

export const Calendar = () => {
  const {
    selectedDate,
    setSelectedDate,
    // setSelectedResource,
    // setActiveTab,
    calendarDays,
    bookings,
  } = useBookingContext();

  const getSelectedDayNumber = () => {
    const match = selectedDate.match(/\d+/);
    return match ? match[0] : null;
  };

  const selectedDayNumber = getSelectedDayNumber();
  // console.log(bookings);
  return (
    <div style={{ padding: '16px' }}>
      {/* Заголовок */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold mb-2 text-base-content">
          Календарь
        </h1>
        <p className="text-sm text-base-content/60">
          Расписание бронирований
        </p>
      </div>

      <div className="mb-6 rounded-2xl p-5 bg-base-200">
      </div>
      
      {/* Текущий месяц */}
      <div
        style={{
          backgroundColor: '#1f2937',
          borderRadius: '16px',
          padding: '20px',
          marginBottom: '24px',
        }}
      >
        <div  
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '20px',
          }}
        >
          <Button
            variant="primary"
            size="lg"
            width="responsive"
            shape="text"
            onClick={() => {}}
            label="←"
          />
          <h2 style={{ fontSize: '18px', fontWeight: '600' }}>Январь 2024</h2>
          <Button
            variant="primary"
            size="lg"
            width="responsive"
            shape="text"
            onClick={() => {}}
            label="→"
          />
        </div>
        {/* Дни недели */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: '2px',
            marginBottom: '16px',
            textAlign: 'center',
          }}
        >
          {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
            <div key={day} style={{ color: '#6b7280', fontSize: '14px' }}>
              {day}
            </div>
          ))}
        </div>
        {/* Числа месяца с бронированиями */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(7, 1fr)',
            gap: '8px',
            textAlign: 'center',
          }}
        >
          {calendarDays.map((day, index) => {
            const dayString = day ? `${day} янв` : '';
            const hasBooking =
              dayString &&
              bookings.some((booking) => booking.date === dayString);
            if (!day) return null;
            const isSelected = day === selectedDayNumber;
            return (
              <Button
                key={index}
                disabled={isSelected}
                label={day}
                size="md"
                width="auto"
                onClick={() => {
                  if (day) {
                    setSelectedDate(`${day} янв`);
                  }
                }}
                shape="rounded"
                className={`relative ${hasBooking ? 'btn-active' : ''}`}
              >
                {hasBooking && (
                  <div
                    style={{
                      position: 'absolute',
                      bottom: '4px',
                      left: '50%',
                      transform: 'translateX(-50%)',
                      width: '4px',
                      height: '4px',
                      backgroundColor: '#000000',
                      borderRadius: '50%',
                    }}
                  ></div>
                )}
              </Button>
            );
          })}
        </div>
      </div>
      {/* Предстоящие бронирования на выбранную дату */}

      <AnimatePresence mode="wait">
        <motion.div
          key={selectedDate}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          transition={{ duration: 0.2 }}
        >
          <BookingCardCalendar
            bookings={bookings}
            selectedDate={selectedDate}
          />
        </motion.div>
      </AnimatePresence>

      {/* <BookingCardCalendar
        key={selectedDate}
        bookings={bookings}
        selectedDate={selectedDate}
      ></BookingCardCalendar> */}
    </div>
  );
};
