import { useState, useEffect } from 'react';
import { useBookingContext, type BookingItem } from '../../../types/bookingContext';
import axios from 'axios';

function BookingsList() {
  const { bookings, setBookings, } = useBookingContext();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get<BookingItem[]>(
          'http://localhost:80/api/bookings/all/',
          {
            headers: {
              Accept: 'application/json',
              Authorization: 'Bearer ' + import.meta.env.VITE_BEARER_TOKEN,
            },
          }
        );
        setBookings(response?.data);
      } catch (err) {
        setError('Error fetching data. Please try again later.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);
  // useEffect(() => {

  //   const API_URL = '/api/bookings/all';


  //   const AUTH_TOKEN = 'AzurPmBtfk6yU31ZOF9A'; 

  //   const fetchBookings = async () => {
  //     try {
  //       const response = await fetch(API_URL, {
  //         method: 'GET',
  //         headers: {
  //           'Accept': 'application/json', 
  //           'Authorization': `Bearer ${AUTH_TOKEN}` 
  //         }
  //       });

  //       if (!response.ok) {

  //         throw new Error(`HTTP error! status: ${response.status}`);
  //       }

  //       const data = await response.json();
  //       setBookings(data); 
  //     } catch (error) {
  //       if (error instanceof Error) { 
  //         setError(error.message); 
  //       } else {
  //         setError('An unknown error occurred');
  //       }
  //     } finally {
  //       setLoading(false);
  //     }
  //   };

  //   fetchBookings();
  // }, []); 

  if (loading) {
    return <p>Загрузка бронирований...</p>;
  }

  if (error) {
    return <p>Ошибка при загрузке данных: {error}</p>;
  }

  return (
    <div>
      <h1>Список бронирований</h1>
      <ul>
        {bookings.map((booking) => (
          <li key={booking.id}>
            Бронирование ID: **{booking.id}** | Ресурс: {booking.description}

          </li>
        ))}
      </ul>
    </div>
  );
}

export default BookingsList;
