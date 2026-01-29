import Button from '@/shared/components/button/button';
import type { BookingItem } from '@/shared/types/types';
import { useState } from 'react';
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
export default function CalendarBlock() {
  const getDaysInMonth = (year: number, month: number) => {
    const date = new Date(year, month, 1);
    const days = [];

    const firstDayOfWeek = date.getDay();

    const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

    for (let i = 0; i < offset; i++) {
      days.push(null);
    }

    while (date.getMonth() === month) {
      days.push(date.getDate());
      date.setDate(date.getDate() + 1);
    }
    return days;
  };
  const selectedDayNumber = '13 янв';
  const bookings: BookingItem[] = [];
  const [viewDate, setViewDate] = useState(new Date(2026, 0, 1));
  // const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  const currentDateUTC = new Date().toISOString();
  const [selectedDate, setSelectedDate] = useState<Date | string>(currentDateUTC);
  console.log(selectedDate)
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

  // eslint-disable-next-line @typescript-eslint/no-unused-vars
  // const getSelectedDayNumber = () => {
  //   const match = selectedDate.match(/\d+/);
  //   return match ? match[0] : null;
  // };
  return (
    <div className="bg-base-100 rounded-2xl p-5 mb-6">
      <div className="flex justify-between items-center mb-5">
        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={() => handlePrevMonth}
          label="←"
        />
        <h2 className="text-lg font-semibold">
          Январь 2026
          {/* {monthNames[currentMonth]} {currentYear} */}
        </h2>
        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={() => handleNextMonth}
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
          const hasBooking = bookings.some((b) => b.start_time === dayString);
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
              className={`relative ${hasBooking ? 'btn-active' : ''} ${isSelected ? '' : 'bg-base-100! border-none! shadow-none! hover:bg-[#374151]!'}`}
            >
              {hasBooking && (
                <div className="absolute bottom-1 left-[50%] transform -translate-x-1/2 w-1 h-1 bg-accent-content rounded-full"></div>
              )}
            </Button>
          );
        })}
      </div>
    </div>
  );
}
