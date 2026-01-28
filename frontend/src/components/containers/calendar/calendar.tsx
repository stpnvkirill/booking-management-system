// import { selectedDate, setSelectedDate, setSelectedResource, setActiveTab } from '../../../App.tsx'
import { useBookingContext } from '../../../types/bookingContext.tsx';
import Button from '../../small/button/button.tsx';
import { BookingCardCalendar } from '../booking-card/booking-card-calendar.tsx';
import { motion, AnimatePresence } from 'framer-motion';

export const Calendar = () => {
  const {
    selectedDate,
    setSelectedDate,
    bookings,
    viewDate,
    setViewDate,
    getDaysInMonth,
  } = useBookingContext();

  const monthNames = [
    'Январь',
    'Февраль',
    'Март',
    'Апрель',
    'Май',
    'Июнь',
    'Июль',
    'Август',
    'Сентябрь',
    'Октябрь',
    'Ноябрь',
    'Декабрь',
  ];
  const currentMonth = viewDate.getMonth();
  const currentYear = viewDate.getFullYear();

  const handlePrevMonth = () => {
    const newDate = new Date(currentYear, currentMonth - 1, 1);
    setViewDate(newDate);

    setSelectedDate(
      `1 ${monthNames[newDate.getMonth()].slice(0, 3).toLowerCase()}`
    );
  };

  const handleNextMonth = () => {
    // setViewDate(new Date(currentYear, currentMonth + 1, 1));
    const newDate = new Date(currentYear, currentMonth + 1, 1);
    setViewDate(newDate);
    setSelectedDate(
      `1 ${monthNames[newDate.getMonth()].slice(0, 3).toLowerCase()}`
    );
  };
  const days = getDaysInMonth(currentYear, currentMonth);

  const getSelectedDayNumber = () => {
    const match = selectedDate.match(/\d+/);
    return match ? match[0] : null;
  };

  const selectedDayNumber = getSelectedDayNumber();
  // console.log(bookings);
  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4 h-screen overflow-auto">
        {/* Заголовок */}
        <div className="mb-6">
          <h1 className="text-3xl font-semibold mb-2">Календарь</h1>
          <p className="text-accent-content text-sm">Расписание бронирований</p>
        </div>
        {/* Текущий месяц */}
        <div className="bg-base-100 rounded-2xl p-5 mb-6">
          <div className="flex justify-between items-center mb-5">
            <Button
              variant="primary"
              size="lg"
              width="responsive"
              shape="text"
              onClick={handlePrevMonth}
              label="←"
            />
            <h2 className="text-lg font-semibold">
              {monthNames[currentMonth]} {currentYear}
            </h2>
            <Button
              variant="primary"
              size="lg"
              width="responsive"
              shape="text"
              onClick={handleNextMonth}
              label="→"
            />
          </div>
          {/* Дни недели */}
          <div className="grid grid-cols-7 gap-2 mb-4 text-center">
            {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
              <div key={day} className="text-sm text-accent-content w-auto">
                {day}
              </div>
            ))}
          </div>
          {/* Числа месяца с бронированиями */}
          <div className="grid grid-cols-7 gap-2 text-center">
            {days.map((day, index) => {
              if (!day) return <div key={`empty-${index}`} />; // Пустая ячейка для отступа
              const dayString = `${day} ${monthNames[currentMonth].slice(0, 3).toLowerCase()}`;
              const isSelected = day.toString() === selectedDayNumber;
              const hasBooking = bookings.some((b) => b.date === dayString);
              return (
                <Button
                  key={index}
                  label={day.toString()}
                  size="md"
                  width="auto"
                  variant="primary"
                  onClick={() => {
                    if (day && !isSelected) {
                      setSelectedDate(dayString);
                    }
                  }}
                  shape="default"
                  className={`relative ${hasBooking ? 'btn-active' : ''} ${isSelected ? '' : 'bg-base-100! border-none! shadow-none! hover:bg-[#374151]!'}`} //
                >
                  {hasBooking && (
                    <div className="absolute bottom-1 left-[50%] transform -translate-x-1/2 w-1 h-1 bg-accent-content rounded-full"></div>
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
            initial={{ opacity: 0, y: 0 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 0 }}
            transition={{ duration: 0.2 }}
          >
            <BookingCardCalendar
              bookings={bookings}
              selectedDate={selectedDate}
            />
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
};
