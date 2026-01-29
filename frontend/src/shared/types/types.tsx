// types.d.ts
// {
//   "customer_id": "019c0b05-2fa7-742d-a914-b8cb00fc9236",
//   "name": "Название места",
//   "description": "Описание места",
//   "resource_type": "Квартира",
//   "location": "Новосибирск",
//   "price_per_hour": 1500
// }
interface ResourceItem {
  id: string;
  customer_id: string;
  name: string;
  description: string;
  resource_type: string;
  location: string;
  price_per_hour: number;
}
interface BookingItem {
  id: number;
  resource_id: number;
  user_id: string;
  start_time: string;
  end_time: string;
  created_at: string;
  updated_at: string;
  description: string;
  booking_type: string;
  location: string;
}
export type Tabs = 'main' | 'details';
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

export { type BookingItem, type ResourceItem, type TimeSlot, FILTERS };
export type { Filters, ActiveFilter };
