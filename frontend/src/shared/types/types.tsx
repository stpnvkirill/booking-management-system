// types.d.ts
// {
//   "customer_id": "019c0b05-2fa7-742d-a914-b8cb00fc9236",
//   "name": "Название места",
//   "description": "Описание места",
//   "resource_type": "Квартира",
//   "location": "Новосибирск",
//   "price_per_hour": 1500
// }
interface Booking_Resource {
  id: number;
  start_time: string;
  end_time: string;
  resource_name: string;
  location: string;
  price_per_hour: number;
  resource_type: string;
  description: string;
}
interface ResourceItem {
  id: number;
  customer_id: string;
  name: string;
  description: string;
  resource_type: string;
  location: string;
  price_per_hour: number;
  available_date: string;
  available_start: string;
  available_end: string;
}
interface BookingItem {
  id: number;
  user_id: string;
  resource_id: number;
  resource_name: string;
  start_time: string;
  end_time: string;
  created_at: string;
}
interface TimeSlot {
  time: string;
  available: boolean;
}
declare global {
  interface Window {
    ready: (name: string) => void;
  }
}

type ActiveFilter = (typeof FILTERS)[number];
type Filters =
  | 'Все'
  | 'Квартира'
  | 'Офис'
  | 'Коттедж'
  | 'Дом'
  | 'Переговорная'
  | 'Студия';
type FiltersArray = readonly Filters[];
const FILTERS: FiltersArray = [
  'Все',
  'Квартира',
  'Студия',
  'Офис',
  'Дом',
  'Переговорная',
  'Коттедж',
] as const;
export type DateString = `${number}-${number}-${number}`;
export type Tabs = 'main' | 'details';
export type ResourceTabs = 'main' | 'details';
export { type Booking_Resource, type BookingItem, type ResourceItem, type TimeSlot, FILTERS };
export type { Filters, ActiveFilter };
