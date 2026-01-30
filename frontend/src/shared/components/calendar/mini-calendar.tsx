import dayjs, { Dayjs } from 'dayjs';
import ru from 'dayjs/locale/ru';
import isToday from 'dayjs/plugin/isToday';
import type { BookingItem, ResourceItem } from '@/shared/types/types';
import Button from '../button/button';
import Card from './components/card';

dayjs.locale(ru);
dayjs.extend(isToday);
interface CalendarDay {
  date: Dayjs | null;
  isInCurrentMonth: boolean;
}
interface BlockMiniCalendarProps {
  data: ResourceItem | BookingItem | undefined;
  selectedDate: dayjs.Dayjs;
  setSelectedDate: React.Dispatch<React.SetStateAction<dayjs.Dayjs>>;
  currentMonth: dayjs.Dayjs;
  setCurrentMonth: React.Dispatch<React.SetStateAction<dayjs.Dayjs>>;
}
export default function BlockMiniCalendar({
  selectedDate,
  setSelectedDate,
  currentMonth,
  setCurrentMonth,
}: BlockMiniCalendarProps) {
  const generateCalendarDays = (date: Dayjs): CalendarDay[] => {
    const startOfMonth = date.startOf('month');
    const endOfMonth = date.endOf('month');
    const daysInMonth = date.daysInMonth();
    const firstDayOfWeek = startOfMonth.day();
    const startPadding = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;
    const calendarDays: CalendarDay[] = [];
    for (let i = startPadding; i > 0; i--) {
      calendarDays.push({
        date: startOfMonth.subtract(i, 'day'),
        isInCurrentMonth: false,
      });
    }
    for (let i = 0; i < daysInMonth; i++) {
      calendarDays.push({
        date: startOfMonth.add(i, 'day'),
        isInCurrentMonth: true,
      });
    }
    const remainingDays = 42 - calendarDays.length;
    for (let i = 1; i <= remainingDays; i++) {
      calendarDays.push({
        date: endOfMonth.add(i, 'day'),
        isInCurrentMonth: false,
      });
    }
    return calendarDays;
  };
  const days = generateCalendarDays(currentMonth);
  const weekdays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС'];
  const handlePrevMonth = () => {
    setCurrentMonth(currentMonth.subtract(1, 'month'));
  };
  const handleNextMonth = () => {
    setCurrentMonth(currentMonth.add(1, 'month'));
  };
  const handleDayClick = (date: Dayjs | null, isInCurrentMonth: boolean) => {
    if (date && isInCurrentMonth) {
      setSelectedDate(date);
    }
  };
  const isSelected = (date: Dayjs | null): boolean => {
    return date ? (selectedDate?.isSame(date, 'day') ?? false) : false;
  };
  return (
    <Card>
      {/* Кнопки листания */}
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
          {currentMonth.format('MMMM YYYY').charAt(0).toUpperCase() +
            currentMonth.format('MMMM YYYY').slice(1)}
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
        {weekdays.map((day) => (
          <div
            key={day}
            className="text-center text-xs text-base-content/50 uppercase font-bold"
          >
            {day}
          </div>
        ))}
      </div>
      {/* Сетка чисел */}
      <div className="grid grid-cols-7 gap-2 mb-2">
        {days.map((day, index) => {
          if (!day?.isInCurrentMonth) return <div key={`empty-${index}`} />;
          return (
            <Button
              key={index}
              label={day.date!.format('D').toString()}
              onClick={() => {
                handleDayClick(day.date, day.isInCurrentMonth);
              }}
              size="md"
              width="auto"
              shape="default"
              className={`relative ${isSelected(day.date) ? '' : 'bg-base-100! border-none! shadow-none! hover:bg-[#374151]!'} `}
            />
          );
        })}
      </div>
    </Card>
  );
}
