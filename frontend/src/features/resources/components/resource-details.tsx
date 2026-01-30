import BlockMiniCalendar from '@/shared/components/calendar/mini-calendar';
import Button from '@/shared/components/button/button';
import { useState } from 'react';
import type {
  DateString,
  ResourceItem,
  ResourceTabs,
} from '@/shared/types/types';
import { GetDD_MM_YYYY } from '@/shared/types/functions';
import dayjs from 'dayjs';

interface ResourceDetailsProps {
  data: ResourceItem | undefined;
  selectedDate: string;
  setSelectedDate: React.Dispatch<React.SetStateAction<DateString>>;
  handleResourceClick: (data: ResourceItem | undefined) => void;
  handleBackClick: () => void;
  setResourceActiveTab: React.Dispatch<React.SetStateAction<ResourceTabs>>;
  activeResourceTab: ResourceTabs | undefined;
}
export default function ResourceDetails({ data }: ResourceDetailsProps) {
  const available_date_str: string = GetDD_MM_YYYY(data!.available_date);
  console.log(available_date_str);

  const [currentMonth, setCurrentMonth] = useState(() => {
    return data?.available_date
      ? dayjs(data.available_date).startOf('month')
      : dayjs().startOf('month');
  });
  const [selectedDate, setSelectedDate] = useState(() => {
    return data?.available_date
      ? dayjs(data.available_date).startOf('day')
      : dayjs().startOf('day');
  });

  const handleConfirmBooking = () => {};

  console.log(data);
  return (
    <>
      {/* Календарь */}
      <BlockMiniCalendar
        data={data}
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        currentMonth={currentMonth}
        setCurrentMonth={setCurrentMonth}
      />
      {/* Слоты времени */}
      <div className="mb-8">
        <div className="ml-4">
          {selectedDate.format('YYYY-MM-DD').toString()}
        </div>
        <div className="grid grid-cols-4 gap-2 mb-2 mt-6">
          <Button
            label="11:00"
            onClick={() => {}}
            size="md"
            variant="secondary"
            shape="default"
          />
          <Button
            label="12:00"
            onClick={() => {}}
            size="md"
            variant="secondary"
            shape="default"
          />
          {/* {timeSlots.map((slot) => (
            <div className="">
              <Button
                label={slot.time}
                onClick={() => setSelectedTimeSlot(slot.time)}
                size="md"
                variant={
                  selectedTimeSlot === slot.time ? 'primary' : 'secondary'
                }
                shape="default"
              />
            </div>
          ))} */}
        </div>
      </div>
      {/* Итого */}
      <div className="rounded-2xl p-5 mb-6 text-neutral">
        <div className="flex justify-between mb-2">
          <span className="text-neutral">Итого</span>
          <span className="font-bold text-2xl text-neutral">
            {(data?.price_per_hour ?? 0).toLocaleString('ru-RU')} ₽ / Час
          </span>
        </div>
        <div className="text-accent text-sm">Слот: —</div>
      </div>
      {/* Кнопка подтверждения */}
      <Button
        label={'Подтвердить'}
        onClick={handleConfirmBooking}
        disabled={!true}
        size="xl"
        width="full"
        variant="primary"
        shape="default"
      />
    </>
  );
}
