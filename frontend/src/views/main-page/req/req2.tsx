import  { useState, useEffect } from 'react';
import axios from 'axios'; // Импортируем Axios
import { useBookingContext } from '../../../types/bookingContext';

function BookingsList2() {
  const { setBookings } = useBookingContext();
  // Устанавливаем начальные значения и типы
  const [loading, setLoading] = useState(true); 
  const [error, setError] = useState<string | null>(null); 

  useEffect(() => {
    const API_URL = 'http://localhost:80/api/bookings/all';
    // Этот токен может больше не понадобиться, если куки будут работать
    const AUTH_TOKEN = import.meta.env.VITE_BEARER_TOKEN

    const fetchBookings = async () => {
      try {
        const response = await axios.get(API_URL, {
          headers: {
            'Accept': 'application/json',
            'Authorization': `Bearer ${AUTH_TOKEN}`
          },
          // !!! ГЛАВНОЕ ИЗМЕНЕНИЕ !!!
          // Это заставляет браузер отправлять куки вместе с запросом
            // withCredentials: true 
        });

        // Axios автоматически парсит JSON, данные лежат в response.data
        setBookings(response.data); 

      } catch (err) {
        // Улучшенная обработка ошибок Axios
        if (axios.isAxiosError(err)) {
            setError(err.message);
        } else if (err instanceof Error) { 
            setError(err.message); 
        } else {
            setError('An unknown error occurred');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchBookings();
  }, []); 

  if (loading) {
    return <p>Загрузка бронирований...</p>;
  }

  if (error) {
    return <p>Ошибка при загрузке данных: **{error}**</p>;
  }

//   return (
//     <div>
//       <h1>Список бронирований</h1>
//       <ul>
//         {bookings.map((booking) => (
//           <li key={booking.id}>
//             Бронирование ID: **{booking.id}** | description: {booking.description} | loacation: {booking.location} 
//             | end_time: {booking.end_time} | start_time: {booking.end_time} 
//              | updated: {booking.upadated_at}  | created: {booking.created_at}
//               | type: {booking.booking_type}  | user_id: {booking.user_id}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
}

export default BookingsList2;