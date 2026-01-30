import BlockMiniCalendar from '@/shared/components/calendar/mini-calendar';
import Button from '@/shared/components/button/button';
import { useState } from 'react';
// import { firstBigLetter } from "@/shared/types/functions"
import type {
  ResourceItem,
  ResourceTabs,
  TimeSlot,
} from '@/shared/types/types';
// import Header from '@/shared/components/header/header';
interface ResourceDetailsProps {
  data: ResourceItem | undefined;
  selectedDate: string;
  handleResourceClick: (data: ResourceItem | undefined) => void;
  handleBackClick: () => void;
  setResourceActiveTab: React.Dispatch<React.SetStateAction<ResourceTabs>>;
  activeResourceTab: ResourceTabs | undefined;
}
export default function ResourceDetails({ data }: ResourceDetailsProps) {
  const [selectedDate, setSelectedDate] = useState<string>('1 янв');

  const [selectedTimeSlot, setSelectedTimeSlot] = useState<
    string | undefined
  >();
  const handleConfirmBooking = () => {};
  const timeSlots: TimeSlot[] = [];

  // if (!data) return null;
  return (
    <>
      {/* Календарь */}
      <BlockMiniCalendar
        selectedDate={selectedDate}
        setSelectedDate={setSelectedDate}
        data={data}
      />

      {/* Слоты времени */}
      <div className="mb-8">
        <div className="ml-4">{selectedDate}</div>
        <div className="grid grid-cols-4 gap-2 mb-2">
          {timeSlots.map((slot) => (
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
          ))}
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
        <div className="text-accent text-sm">
          Слот: {selectedTimeSlot || '—'}
        </div>
      </div>
      {/* Кнопка подтверждения */}
      <Button
        label={'Подтвердить'}
        onClick={handleConfirmBooking}
        disabled={!selectedTimeSlot}
        size="xl"
        width="full"
        variant="primary"
        shape="default"
      />
    </>
  );
}
