import type { PropsWithChildren } from 'react';
import Button from '../../small/button/button';
import type { BookingItem } from '../../../types/bookingContext';
// import { useBookingContext } from "../bookingContext/bookingContext.tsx";
export interface ActiveBookingProps {
  // bookings?: BookingItem;
  // selectedDate?: string;
  bookings?: string; //потом будет подругому

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: BookingItem; // Позже замени на BookingItem
  onCancel: () => void;
}
export const ActiveBookingCard = ({
  data,
  onCancel,
  // bookings,
}: PropsWithChildren<ActiveBookingProps>): React.ReactElement => {
  // console.log(bookings);
  return (
    <div className="rounded-2xl p-5 bg-base-200 hover:bg-base-100 duration-200">
      <div className="mb-3">
        <div className="text-lg font-semibold mb-1 text-base-content">
          {data.description}
        </div>
        <div className="text-sm text-base-content/60">
          {data.date} • {data.time}
        </div>
      </div>
      <div className="flex gap-3 justify-center flex-row ">
        {/* <div className="w-full">
          <Button
            onClick={() => {}}
            label="Открыть"
            variant="primary"
            size="md"
            width="full"
          ></Button>
        </div> */}
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
};
/*  */
