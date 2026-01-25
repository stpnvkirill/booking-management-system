import Card from '../../small/card/card.tsx';
import Button from '../../small/button/button.tsx';
import { useBookingContext } from '../../../types/bookingContext.tsx';
// import { type ButtonVariant } from '../../small/button/button.tsx'
// import { useState } from 'react';

export const BlockMiniCalendar = () => {
  const { setSelectedDate, calendarDays, selectedDate, bookings,
    viewDate, setViewDate, getDaysInMonth } =
    useBookingContext();

  const monthNames = [
    'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
    'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
  ];
  const currentMonth = viewDate.getMonth();
  const currentYear = viewDate.getFullYear();

  const handlePrevMonth = () => {
    setViewDate(new Date(currentYear, currentMonth - 1, 1));
  };

  const handleNextMonth = () => {
    setViewDate(new Date(currentYear, currentMonth + 1, 1));
  };
  const days = getDaysInMonth(currentYear, currentMonth);


  const selectedDayNumber = selectedDate.match(/\d+/)?.[0];

  // const [activeButtonId, setActiveButtonId] = useState<number | null>(null);

  return (
    <Card title="Календарь" extra={selectedDate}>
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
        {calendarDays.map((day) => {
          const dayString = day ? `${day} янв` : '';
          const hasBooking =
            dayString && bookings.some((booking) => booking.date === dayString);
          if (!day) return null;
          const isSelected = day === selectedDayNumber;
          return (
            <Button
              label={day?.toString() || ''}
              onClick={() => {
                if (day && !isSelected) {
                  setSelectedDate(`${day} янв`);
                }
              }}
              size="md"
              width='auto'
              // variant={
              //   isSelected ? 'primary' : hasBooking ? 'secondary' : 'tertiary'
              // }

              shape="default"
              className={`relative ${isSelected
                ? ''
                : '!bg-base-100 !border-none !shadow-none hover:!bg-[#374151]'
                } ${hasBooking ? 'btn-active' : ''}`}
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
                    backgroundColor: 'black',
                    borderRadius: '50%',
                  }}
                ></div>
              )}
            </Button>
          );
        })}
      </div>
    </Card>
  );
};
