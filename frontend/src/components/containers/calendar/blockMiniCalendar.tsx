import Card from '../../small/card/card.tsx';
import Button from '../../small/button/button.tsx';
import { useBookingContext } from '../../../types/bookingContext.tsx';

export const BlockMiniCalendar = () => {
  const {
    setSelectedDate,
    selectedDate,
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
    const newDate = new Date(currentYear, currentMonth + 1, 1);
    setViewDate(newDate);
    setSelectedDate(
      `1 ${monthNames[newDate.getMonth()].slice(0, 3).toLowerCase()}`
    );
  };
  const days = getDaysInMonth(currentYear, currentMonth);

  const selectedDayNumber = selectedDate.match(/\d+/)?.[0];

  // const [activeButtonId, setActiveButtonId] = useState<number | null>(null);

  return (
    <Card>
      <div className="flex justify-between items-center mb-5">
        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={handlePrevMonth}
          label="←"
        />
        <h2 className="text-lg text-neutral font-semibold">
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
      <div className="grid grid-cols-7 gap-2 mb-2">
        {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
          <div
            key={day}
            className="text-center text-xs text-base-content/50 uppercase font-bold"
          >
            {day}
          </div>
        ))}
      </div>
      {/* Сетка чисел */}
      <div className="grid grid-cols-7 gap-2">
        {days.map((day, index) => {
          if (!day) return <div key={`empty-${index}`} />; // Пустая ячейка для отступа

          const dayString = `${day} ${monthNames[currentMonth].slice(0, 3).toLowerCase()}`;
          const isSelected = day.toString() === selectedDayNumber;
          const hasBooking = bookings.some((b) => b.date === dayString);
          return (
            <Button
              label={day.toString()}
              onClick={() => {
                if (day && !isSelected) {
                  setSelectedDate(dayString);
                }
              }}
              size="md"
              width="auto"
              shape="default"
              className={`relative ${isSelected ? '' : 'bg-base-100! border-none! shadow-none! hover:bg-[#374151]!'} ${hasBooking ? 'btn-active' : ''}`}
            >
              {hasBooking && (
                <div className="absolute bottom-1 left-[50%] transform -translate-x-1/2 w-1 h-1 bg-accent-content rounded-full"></div>
              )}
            </Button>
          );
        })}
      </div>
    </Card>
  );
};
