import { createContext, useContext, useState, type ReactNode } from 'react';
import {
  type FilterType,
  type TimeSlot,
} from '../views/main-page/main-page.tsx';
export type Booking = {
  id: string;
  resourceId?: string;
  customerId?: string;
  startAt?: string;
  endAt?: string;
  [key: string]: unknown;
};

export type GetAllBookingsResponse = Booking[];

interface BookingContextType {
  activeTab: 'Ресурсы' | 'Календарь' | 'Профиль';
  setActiveTab: (tab: 'Ресурсы' | 'Календарь' | 'Профиль') => void;
  selectedFilter: FilterType;
  setSelectedFilter: (filter: FilterType) => void;
  selectedDate: string;
  setSelectedDate: (date: string) => void;
  selectedTimeSlot: string | null;
  setSelectedTimeSlot: (timeSlot: string | null) => void;

  selectedResource: BookingItem | null;
  setSelectedResource: (resource: BookingItem | null) => void;

  filters: FilterType[];
  bookings: BookingItem[];
  setBookings: React.Dispatch<React.SetStateAction<BookingItem[]>>;
  timeSlots: TimeSlot[];
  calendarDays: string[];

  handleResourceClick: (resource: BookingItem) => void;
  handleCancelBooking: (id: string) => void;
  handleBackClick: () => void;
  handleConfirmBooking: () => void;
  isAuthenticated: boolean;
  setIsAuthenticated: (val: boolean) => void;
  login: string;
  pass: string;
  isLoading: boolean;
  setLogin: React.Dispatch<React.SetStateAction<string>>;
  setPass: React.Dispatch<React.SetStateAction<string>>;
  setIsLoading: (value: React.SetStateAction<boolean>) => void;
  error: boolean;
  setError: React.Dispatch<React.SetStateAction<boolean>>;
  // currentMonth: number;
  // setCurrentMonth: React.Dispatch<React.SetStateAction<number>>
  getDaysInMonth: (year: number, month: number) => (number | null)[];
  viewDate: Date;
  setViewDate: React.Dispatch<React.SetStateAction<Date>>;
}
export interface BookingItem {
  price?: number;
  id?: string;
  title?: string;
  type?: string;
  capacity?: string;
  location?: string;
  rating?: string | number;
  timeLeft?: string;
  time?: string;
  date?: string;
  active?: boolean;
}
// контекст
const BookingContext = createContext<BookingContextType | undefined>(undefined);
//провайдер
export const BookingProvider = ({ children }: { children: ReactNode }) => {
  const [activeTab, setActiveTab] = useState<
    'Ресурсы' | 'Календарь' | 'Профиль'
  >('Ресурсы');
  const [selectedFilter, setSelectedFilter] = useState<FilterType>('Все');
  const [selectedDate, setSelectedDate] = useState<string>('1 янв');
  const [selectedTimeSlot, setSelectedTimeSlot] = useState<string | null>(null);
  const [selectedResource, setSelectedResource] = useState<BookingItem | null>(
    null
  );
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // const [currentMonth, setCurrentMonth] = useState(0);
  const [viewDate, setViewDate] = useState(new Date(2026, 0, 1));

  const [login, setLogin] = useState('');
  const [pass, setPass] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(false);

  const filters: FilterType[] = [
    'Все',
    'Площадка',
    'Работа',
    'Здоровье',
    'Авто',
    'Жильё',
  ];
  const [bookings, setBookings] = useState<BookingItem[]>([
    {
      id: '0',
      title: 'Loft Noir',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 2900,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '1',
      title: 'Loft Noir2',
      type: 'Площадка',
      capacity: '30–50 гостей',
      location: 'Центр',
      rating: 4.8,
      timeLeft: '4ч',
      price: 3000,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '2',
      title: 'Cowork Pulse',
      type: 'Работа',
      capacity: 'Дневной доступ',
      location: 'Центр',
      rating: 4.7,
      timeLeft: '8ч',
      price: 1200,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '3',
      title: 'Hall Obsidian',
      type: 'Площадка',
      capacity: '80–120 гостей',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '6ч',
      price: 5400,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '4',
      title: 'Noir Suites',
      type: 'Жильё',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '',
      time: '',
      active: false,
    },
    {
      id: '5',
      title: 'Noir 222 Suites',
      type: 'Работа',
      capacity: '1 ночь',
      location: 'Набережная',
      rating: 4.9,
      timeLeft: '2ч',
      price: 5600,
      date: '',
      time: '',
      active: false,
    },
  ]);
  const timeSlots: TimeSlot[] = [
    { time: '18:00', available: true },
    { time: '18:30', available: true },
    { time: '19:00', available: true },
    { time: '19:30', available: true },
    { time: '20:00', available: true },
    { time: '20:30', available: true },
    { time: '21:00', available: true },
    { time: '21:30', available: true },
  ];
  const calendarDays = Array.from({ length: 31 }, (_, i) => String(i + 1));

  const getDaysInMonth = (year: number, month: number) => {
    const date = new Date(year, month, 1);
    const days = [];

    const firstDayOfWeek = date.getDay();

    const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

    for (let i = 0; i < offset; i++) {
      days.push(null);
    }

    while (date.getMonth() === month) {
      days.push(date.getDate());
      date.setDate(date.getDate() + 1);
    }
    return days;
  };

  const handleResourceClick = (resource: BookingItem) => {
    setSelectedResource(resource);
  };

  const handleBackClick = () => {
    setSelectedResource(null);
  };

  /// чтоб вернуть обратно кнопку брони раскоменти и переименуй(обязательно)
  // закоменченый handleConfirmBooking ниже и вызови его в самой кнопке
  const handleConfirmBooking = () => {
    if (selectedTimeSlot && selectedResource) {
      setBookings((prevBookings) =>
        prevBookings.map((item) =>
          item.id === selectedResource.id
            ? {
                ...item,
                active: true,
                date: selectedDate,
                time: selectedTimeSlot,
              }
            : item
        )
      );

      alert(`Бронирование подтверждено: ${selectedResource.title}`);

      setSelectedResource(null);
      setSelectedTimeSlot(null);
    }
  };

  const handleCancelBooking = (id: string) => {
    setBookings((prev) =>
      prev.map((b) =>
        b.id === id ? { ...b, active: false, date: '', time: '' } : b
      )
    );
  };

  // const handleConfirmBooking = () => {
  //   alert('Забронировано успешно!');
  //   if (selectedTimeSlot && selectedResource) {
  //     alert(
  //       `Бронирование подтверждено: ${selectedResource.title} на ${selectedTimeSlot}`
  //     );
  //     console.log(selectedResource)
  //     setSelectedResource(null);
  //     setSelectedTimeSlot(null);
  //   }
  // };

  const value: BookingContextType = {
    activeTab,
    setActiveTab,
    selectedFilter,
    setSelectedFilter,
    selectedDate,
    setSelectedDate,
    selectedTimeSlot,
    setSelectedTimeSlot,
    selectedResource,
    setSelectedResource,

    filters,
    bookings,
    setBookings,
    timeSlots,
    calendarDays,

    handleResourceClick,
    handleBackClick,
    handleConfirmBooking,
    handleCancelBooking,
    isAuthenticated,
    setIsAuthenticated,
    login,
    setLogin,
    pass,
    setPass,
    isLoading,
    setIsLoading,
    error,
    setError,
    // currentMonth,
    // setCurrentMonth,
    getDaysInMonth,
    viewDate,
    setViewDate,
  };

  return (
    <BookingContext.Provider value={value}>{children}</BookingContext.Provider>
  );
};
// eslint-disable-next-line react-refresh/only-export-components
export const useBookingContext = () => {
  const context = useContext(BookingContext);
  if (context === undefined) {
    throw new Error('useBookingContext must be used within a BookingProvider');
  }
  return context;
};
