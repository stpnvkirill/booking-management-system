import Button from '@/shared/components/button/button';
import type { BookingItem } from '@/shared/types/types';
import dayjs from 'dayjs';
// import { useBookingContext } from "../bookingContext/bookingContext.tsx";
export interface ActiveBookingProps {
  bookings?: string; //потом будет подругому
  data: BookingItem | undefined; // Позже замени на BookingItem
  onCancel: () => void;
}
export default function ActiveBookingCard({
  data,
  onCancel,
}: ActiveBookingProps) {
  return (
    <div className="rounded-2xl p-5 bg-base-200 hover:bg-base-100 duration-200">
      <div className="mb-3">
        <div className="text-lg font-semibold mb-1 text-base-content">
          {data?.resource_name}
        </div>
        <div className="text-sm text-base-content/60">
          {dayjs(data?.start_time).format("DD.MM.YYYY")} • {dayjs(data?.start_time).format("hh:mm")}-{dayjs(data?.end_time).format("hh:mm")}
        </div>
      </div>
      <div className="flex gap-3 justify-center flex-row ">
        <div className="w-full">
          <Button
            onClick={onCancel}
            label="Отменить"
            variant="info"
            size="md"
            width="full"
          ></Button>
        </div>
      </div>
    </div>
  );
}
