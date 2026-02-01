import BlockMiniCalendar from '@/shared/components/calendar/mini-calendar';
import Button from '@/shared/components/button/button';
import { useState } from 'react';
import type {
  DateString,
  ResourceItem,
  ResourceTabs,
} from '@/shared/types/types';
import { GetDD_MM_YYYY } from '@/shared/types/functions';
import dayjs, { Dayjs } from 'dayjs';
import utc from 'dayjs/plugin/utc';
import timezone from 'dayjs/plugin/timezone';
dayjs().format()
dayjs.extend(utc);
dayjs.extend(timezone);

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

  const handleConfirmBooking = () => {
    alert(`Бронирование "${data?.name}" на время ${selectedTimeSlotStart}-${selectedTimeSlotEnd}. Подтверждено!`)
  };

  const generateTimeSlots = (
    start: string,
    end: string,
    step: number = 30,
    selectedSlot?: string,
    tz: string = 'Asia/Novosibirsk',
  ) => {
    const Start = dayjs.tz(start, tz)
    const End = dayjs.tz(end, tz)
    const slots: string[] = [];
    let current: Dayjs = Start;
    if (selectedSlot) {
      current = dayjs.tz(`${dayjs(start).format('YYYY-MM-DD')} ${selectedSlot}`, tz).add(step, 'minute');
    } else {
      current = dayjs.tz(start, tz);
    }
    while (current.isBefore(End) || current.isSame(End, "minute")) {
      slots.push(current.format("HH:mm"));
      current = current.add(step, "minute")
    }
    return slots;
  }
  const TimeSlots = generateTimeSlots(data!.available_start, data!.available_end, 30)

  const [selectedTimeSlotStart, setTimeSlotStart] = useState<string>()
  const [selectedTimeSlotEnd, setTimeSlotEnd] = useState<string>()
  const [TimeSlotsLeft, setTimeSlotStartsLeft] = useState<string[]>()

  const getTimeSlotsLeft = (slot: string) => {
    const GetTimeSlotsLeft = generateTimeSlots(data!.available_start, data!.available_end, 30, slot)
    console.log(`${dayjs(data!.available_start).format("YYYY-MM-DD")}T${slot}:00Z`)
    setTimeSlotStartsLeft(GetTimeSlotsLeft)
    console.log(GetTimeSlotsLeft)
  }

  // console.log(generateTimeSlots(`${dayjs().format("YYYY-MM-DD")}T${selectedTimeSlotStart}:00Z`, data!.available_end, 30))
  return (
    <div className="h-max max-h-[calc(100vh-185px)] overflow-y-scroll">
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
        {/* <div className="ml-4">
          {selectedDate.format('YYYY-MM-DD').toString()}
        </div> */}
        {
          !selectedTimeSlotStart ?
            <div className="grid grid-cols-4 gap-2 mb-2 mt-6">
              {TimeSlots.map((slot) => {
                const isSelected = slot === selectedTimeSlotStart;
                return (
                  <div>
                    <Button
                      label={`${slot}`}
                      onClick={() => {
                        setTimeSlotStart(slot);
                        getTimeSlotsLeft(slot)
                      }}
                      size="sm"
                      variant={
                        isSelected ? "primary" : "tertiary"
                      }
                      shape={isSelected ? "rounded" : "default"}
                    />
                  </div>
                )
              })}
            </div> :
            !selectedTimeSlotEnd ?
              <div className="grid grid-cols-4 gap-2 mb-2 mt-6">
                {TimeSlotsLeft!.map((slot) => {
                  const isSelected = slot === selectedTimeSlotEnd;
                  return (
                    <div>
                      <Button
                        label={`${slot}`}
                        onClick={() => {
                          setTimeSlotEnd(slot);
                          console.log(selectedTimeSlotEnd);
                        }}
                        size="sm"
                        variant={
                          isSelected ? "primary" : "tertiary"
                        }
                        shape={isSelected ? "rounded" : "outline"}
                      />
                    </div>
                  )
                })}
              </div>
              : ""}
        {
          selectedTimeSlotStart ?
            <Button
              variant="primary"
              shape="text"
              width="full"
              size="xs"
              label={`Выбрать другое время?(Сейчас ${selectedTimeSlotStart || ""}-${selectedTimeSlotEnd || ""})`}
              onClick={() => { setTimeSlotStart(undefined); setTimeSlotEnd(undefined) }}
            /> : ""
        }
      </div>
      {/* Итого */}
      <div className="rounded-2xl p-5 mb-6 text-neutral">
        <div className="flex justify-between mb-2">
          <span className="text-neutral">Итого</span>
          <span className="font-bold text-2xl text-neutral">
            {(data?.price_per_hour ?? 0).toLocaleString('ru-RU')} ₽ / Час
          </span>
        </div>
        <div className="text-accent text-sm">Слот: {selectedTimeSlotStart! ? `${selectedTimeSlotStart || ""}-${selectedTimeSlotEnd || ""}` : "—"}</div>
      </div>
      {/* Кнопка подтверждения */}
      <Button
        label={'Подтвердить'}
        onClick={handleConfirmBooking}
        disabled={!selectedTimeSlotEnd}
        size="xl"
        width="full"
        variant="primary"
        shape="default"
      />
    </div >
  );
}
