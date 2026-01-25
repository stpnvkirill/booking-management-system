import type { PropsWithChildren } from 'react';
import Button from '../../small/button/button';
// import { useBookingContext } from "../bookingContext/bookingContext.tsx";
export interface ActiveBookingProps {
  // bookings?: BookingItem;
  // selectedDate?: string;
  bookings?: string; //потом будет подругому

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  data: any; // Позже замени на BookingItem
  onCancel: () => void;
}
export const ActiveBookingCard = ({
  data,
  onCancel,
  // bookings,
}: PropsWithChildren<ActiveBookingProps>): React.ReactElement => {
  // console.log(bookings);
  return (
    //     <div className="p-4 bg-secondary rounded-2xl mb-4">
    //   <div className="flex justify-between items-start mb-2">
    //     <div>
    //       <h3 className="font-bold text-lg">{data.title}</h3>
    //       <p className="text-sm text-gray-400">{data.type}</p>
    //     </div>
    //     <div className="text-right">
    //       <div className="text-accent font-bold">{data.price} ₽</div>
    //       <div className="text-xs text-gray-500">{data.date}</div>
    //     </div>
    //   </div>

    //   <div className="flex items-center gap-2 mb-4 text-sm text-gray-300">
    //     <span>🕒 {data.time}</span>
    //     <span>•</span>
    //     <span>📍 {data.location}</span>
    //   </div>

    //   <Button
    //     label="Отменить"
    //     variant="error"
    //     shape="rounded"
    //     size="sm"
    //     width="full"
    //     onClick={onCancel}
    //   />
    // </div>

    <div className="mb-4 rounded-2xl p-5 bg-base-200 hover:bg-base-100 duration-200">
      <div className="mb-3">
        <div className="text-lg font-semibold mb-1 text-base-content">
          {data.title}
        </div>
        <div className="text-sm text-base-content/60">
          {data.date} • {data.time}
        </div>
      </div>
      <div className="flex gap-3 justify-center flex-row ">
        <div className="w-full">
          <Button
            onClick={() => {}}
            label="Открыть"
            variant="primary"
            size="md"
            width="full"
          ></Button>
        </div>
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
