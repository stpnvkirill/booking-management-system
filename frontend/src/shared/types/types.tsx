// types.d.ts
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
  | "Студия";
type FiltersArray = readonly Filters[];
const FILTERS: FiltersArray = [
  'Все',
  'Квартира',
  "Студия",
  'Офис',
  'Дом',
  'Переговорная',
  'Коттедж',
] as const;

export { type BookingItem, type TimeSlot, FILTERS };
export type { Filters, ActiveFilter };
