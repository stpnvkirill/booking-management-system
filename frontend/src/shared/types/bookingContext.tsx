// import { createContext, useContext, useState, type ReactNode } from 'react';
// import {
//   type FilterType,
//   type TimeSlot,
// } from '../views/main-page/main-page.tsx';
// interface BookingContextType {
//   activeTab: 'Ресурсы' | 'Календарь' | 'Профиль';
//   setActiveTab: (tab: 'Ресурсы' | 'Календарь' | 'Профиль') => void;
//   selectedFilter: Filters;
//   setSelectedFilter: (filter: Filters) => void;
//   selectedDate: string;
//   setSelectedDate: (date: string) => void;
//   selectedTimeSlot: string | null;
//   setSelectedTimeSlot: (timeSlot: string | null) => void;

//   selectedResource: BookingItem | null;
//   setSelectedResource: (resource: BookingItem | null) => void;

//   filters: Filters[];
//   bookings: BookingItem[];
//   setBookings: React.Dispatch<React.SetStateAction<BookingItem[]>>;
//   timeSlots: TimeSlot[];
//   calendarDays: string[];

//   handleResourceClick: (resource: BookingItem) => void;
//   handleCancelBooking: (id: string) => void;
//   handleBackClick: () => void;
//   handleConfirmBooking: () => void;
//   isAuthenticated: boolean;
//   setIsAuthenticated: (val: boolean) => void;
//   login: string;
//   pass: string;
//   isLoading: boolean;
//   setLogin: React.Dispatch<React.SetStateAction<string>>;
//   setPass: React.Dispatch<React.SetStateAction<string>>;
//   setIsLoading: (value: React.SetStateAction<boolean>) => void;
//   error: boolean;
//   setError: React.Dispatch<React.SetStateAction<boolean>>;
//   // currentMonth: number;
//   // setCurrentMonth: React.Dispatch<React.SetStateAction<number>>
//   getDaysInMonth: (year: number, month: number) => (number | null)[];
//   viewDate: Date;
//   setViewDate: React.Dispatch<React.SetStateAction<Date>>;
//   handleTimeClick: (time: string) => void

//   bookingRange: {
//     start: string | null;
//     end: string | null;
//   }
//   setBookingRange: React.Dispatch<React.SetStateAction<{
//     start: string | null;
//     end: string | null;
//   }>>

// }
// export interface BookingItem {
//   price?: number;
//   id?: string;
//   capacity?: string;
//   location: string;
//   rating?: string | number;
//   timeLeft?: string;
//   time?: string;
//   date?: string;
//   active?: boolean;

//   created_at: string;
//   upadated_at: string;
//   resource_id: number;
//   user_id: string;
//   description: string;
//   booking_type: string;
//   start_time: string;
//   end_time: string;
// }

// // контекст
// const BookingContext = createContext<BookingContextType | undefined>(undefined);
// //провайдер
// export const BookingProvider = ({ children }: { children: ReactNode }) => {
//   const [activeTab, setActiveTab] = useState<
//     'Ресурсы' | 'Календарь' | 'Профиль'
//   >('Ресурсы');
//   const [selectedFilter, setSelectedFilter] = useState<Filters>('Все');
//   const [selectedDate, setSelectedDate] = useState<string>('1 янв');
//   const [selectedTimeSlot, setSelectedTimeSlot] = useState<string | null>(null);
//   const [selectedResource, setSelectedResource] = useState<BookingItem | null>(
//     null
//   );
//   const [isAuthenticated, setIsAuthenticated] = useState(false);
//   // const [currentMonth, setCurrentMonth] = useState(0);
//   const [viewDate, setViewDate] = useState(new Date(2026, 0, 1));

//   const [login, setLogin] = useState('');
//   const [pass, setPass] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [error, setError] = useState(false);

//   // useEffect(() => {
//   //   const API_URL = 'http://localhost:80/api/bookings/all'; // Твой URL из BookingsList2

//   //   const fetchBookings = async () => {
//   //     setIsLoading(true); // Используем стейт из провайдера
//   //     setError(false); // Сбрасываем ошибку
//   //     try {
//   //       const response = await axios.get(API_URL, {
//   //         headers: {
//   //           'Accept': 'application/json',
//   //           'Authorization': `Bearer ${AUTH_TOKEN}`
//   //         },
//   //       });

//   //       // САМЫЙ ВАЖНЫЙ ЭТАП: Маппинг полей из БД в твой интерфейс
//   //       const mappedData: BookingItem2[] = response.data.map((dbItem: any) => {

//   //         // Здесь берем поля из `dbItem` (как на твоем скрине БД)
//   //         // и присваиваем их полям твоего `BookingItem` интерфейса (как в твоем коде)
//   //         return {
//   //           id: dbItem.id.toString(), // id (serial4)
//   //           resource_id: dbItem.resource_id, // resource_id (int4)
//   //           user_id: dbItem.user_id, // user_id (uuid)
//   //           description: dbItem.description, // description (text)
//   //           location: dbItem.location, // location (varchar)
//   //           start_time: dbItem.start_time, // start_time (timestamptz)
//   //           end_time: dbItem.end_time, // end_time (timestamptz)
//   //           booking_type: dbItem.booking_type, // booking_type

//   //           // Дополнительные поля UI, которые ты можешь вычислить или задать по умолчанию
//   //           title: dbItem.description || 'Бронирование', // Используем description как title
//   //           active: new Date(dbItem.end_time) > new Date(), // Активно, если время окончания еще не прошло
//   //           // date и time можно вычислить из start_time/end_time при необходимости
//   //         };
//   //       });

//   //       setBookings(mappedData);

//   //     } catch (err) {
//   //       console.error(err);
//   //       setError(true);
//   //     } finally {
//   //       setIsLoading(false);
//   //     }
//   //   };

//   //   fetchBookings();
//   // }, []);

//   // const filters: Filters[] = [
//   //   'Все',
//   //   'Площадка',
//   //   'Работа',
//   //   'Здоровье',
//   //   'Авто',
//   //   'Жильё',
//   // ];

//   const [bookings, setBookings] = useState<BookingItem[]>([
//     {
//       id: '0',
//       capacity: '30–50 гостей',
//       location: 'Центр',
//       rating: 4.8,
//       timeLeft: '4ч',
//       price: 2900,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//     {
//       id: '1',

//       capacity: '30–50 гостей',
//       location: 'Центр',
//       rating: 4.8,
//       timeLeft: '4ч',
//       price: 3000,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//     {
//       id: '2',

//       capacity: 'Дневной доступ',
//       location: 'Центр',
//       rating: 4.7,
//       timeLeft: '8ч',
//       price: 1200,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//     {
//       id: '3',

//       capacity: '80–120 гостей',
//       location: 'Набережная',
//       rating: 4.9,
//       timeLeft: '6ч',
//       price: 5400,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//     {
//       id: '4',

//       capacity: '1 ночь',
//       location: 'Набережная',
//       rating: 4.9,
//       timeLeft: '2ч',
//       price: 5600,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//     {
//       id: '5',

//       capacity: '1 ночь',
//       location: 'Набережная',
//       rating: 4.9,
//       timeLeft: '2ч',
//       price: 5600,
//       date: '',
//       time: '',
//       active: false,

//       start_time: '',
//       end_time: '',
//       created_at: '',
//       upadated_at: '',
//       resource_id: 0,
//       user_id: '',
//       description: '',
//       booking_type: '',
//     },
//   ]);
//   const timeSlots: TimeSlot[] = [
//     { time: '12:00', available: true },
//     { time: '12:30', available: true },
//     { time: '13:00', available: true },
//     { time: '13:30', available: true },
//     { time: '14:30', available: true },
//     { time: '15:00', available: true },
//     { time: '15:30', available: true },
//     { time: '16:00', available: true },
//     { time: '16:30', available: true },
//     { time: '17:00', available: true },
//     { time: '17:30', available: true },
//     { time: '18:00', available: true },
//     { time: '18:30', available: true },
//     { time: '19:00', available: true },
//     { time: '19:30', available: true },
//     { time: '20:00', available: true },
//     { time: '20:30', available: true },
//     { time: '21:00', available: true },
//     { time: '21:30', available: true },
//     { time: '22:00', available: true },
//   ];

//   const [bookingRange, setBookingRange] = useState<{ start: string | null, end: string | null }>({
//     start: null,
//     end: null
//   });

//   const handleTimeClick = (time: string) => {
//     if (!bookingRange.start || (bookingRange.start && bookingRange.end)) {

//       setBookingRange({ start: time, end: null });
//     } else {

//       if (time > bookingRange.start) {
//         setBookingRange(prev => ({ ...prev, end: time }));
//       } else {

//         setBookingRange({ start: time, end: null });
//       }
//     }
//   };

//   const calendarDays = Array.from({ length: 31 }, (_, i) => String(i + 1));

//   const getDaysInMonth = (year: number, month: number) => {
//     const date = new Date(year, month, 1);
//     const days = [];

//     const firstDayOfWeek = date.getDay();

//     const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

//     for (let i = 0; i < offset; i++) {
//       days.push(null);
//     }

//     while (date.getMonth() === month) {
//       days.push(date.getDate());
//       date.setDate(date.getDate() + 1);
//     }
//     return days;
//   };

//   const handleResourceClick = (resource: BookingItem) => {
//     setSelectedResource(resource);
//   };

//   const handleBackClick = () => {
//     setSelectedResource(null);
//   };

//   /// чтоб вернуть обратно кнопку брони раскоменти и переименуй(обязательно)
//   // закоменченый handleConfirmBooking ниже и вызови его в самой кнопке
//   // const handleConfirmBooking = () => {
//   //   if (selectedTimeSlot && selectedResource) {
//   //     setBookings((prevBookings) =>
//   //       prevBookings.map((item) =>
//   //         item.id === selectedResource.id
//   //           ? {
//   //             ...item,
//   //             active: true,
//   //             date: selectedDate,
//   //             time: selectedTimeSlot,
//   //           }
//   //           : item
//   //       )
//   //     );

//   //     alert(`Бронирование подтверждено: ${selectedResource.description}`);

//   //     setSelectedResource(null);
//   //     setSelectedTimeSlot(null);
//   //   }
//   // };

//   const handleConfirmBooking = () => {
//     if (!bookingRange.start || !bookingRange.end || !selectedResource) return;

//     setBookings((prevBookings) =>
//       prevBookings.map((item) =>
//         item.id === selectedResource.id
//           ? {
//             ...item,
//             active: true,
//             date: selectedDate,

//             time: `${bookingRange.start} — ${bookingRange.end}`,
//           }
//           : item
//       )
//     );

//     // alert(`Бронирование подтверждено: ${selectedResource.description}`);

//     setBookingRange({ start: null, end: null });
//     handleBackClick();
//   };

//   const handleCancelBooking = (id: string) => {
//     setBookings((prev) =>
//       prev.map((b) =>
//         b.id === id ? { ...b, active: false, date: '', time: '' } : b
//       )
//     );
//   };

//   // const handleConfirmBooking = () => {
//   //   alert('Забронировано успешно!');
//   //   if (selectedTimeSlot && selectedResource) {
//   //     alert(
//   //       `Бронирование подтверждено: ${selectedResource.title} на ${selectedTimeSlot}`
//   //     );
//   //     console.log(selectedResource)
//   //     setSelectedResource(null);
//   //     setSelectedTimeSlot(null);
//   //   }
//   // };

//   const value: BookingContextType = {
//     activeTab,
//     setActiveTab,
//     selectedFilter,
//     setSelectedFilter,
//     selectedDate,
//     setSelectedDate,
//     selectedTimeSlot,
//     setSelectedTimeSlot,
//     selectedResource,
//     setSelectedResource,

//     // filters,
//     bookings,
//     setBookings,
//     timeSlots,
//     calendarDays,

//     handleResourceClick,
//     handleBackClick,
//     handleConfirmBooking,
//     handleCancelBooking,
//     isAuthenticated,
//     setIsAuthenticated,
//     login,
//     setLogin,
//     pass,
//     setPass,
//     isLoading,
//     setIsLoading,
//     error,
//     setError,
//     // currentMonth,
//     // setCurrentMonth,
//     getDaysInMonth,
//     viewDate,
//     setViewDate,
//     handleTimeClick,
//     bookingRange,
//     setBookingRange
//   };

//   return (
//     <BookingContext.Provider value={value}>{children}</BookingContext.Provider>
//   );
// };
// // eslint-disable-next-line react-refresh/only-export-components
// export const useBookingContext = () => {
//   const context = useContext(BookingContext);
//   if (context === undefined) {
//     throw new Error('useBookingContext must be used within a BookingProvider');
//   }
//   return context;
// };
