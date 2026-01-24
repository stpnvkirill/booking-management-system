// import { useBookingContext } from '../bookingContext/bookingContext.tsx';

// export const MiniCalendar = () => {
//   const { setSelectedDate, calendarDays, selectedDate, bookings } =
//     useBookingContext();

//   const getSelectedDayNumber = () => {
//     const match = selectedDate.match(/\d+/);
//     return match ? match[0] : null;
//   };

//   const selectedDayNumber = getSelectedDayNumber();

//   return (
//     <div style={{ marginBottom: '32px' }}>
//       <div
//         style={{
//           display: 'flex',
//           justifyContent: 'space-between',
//           alignItems: 'center',
//           marginBottom: '16px',
//         }}
//       >
//         <h2 style={{ fontSize: '16px', fontWeight: '600' }}>Календарь</h2>
//         <span style={{ color: '#3b82f6', fontWeight: '500' }}>
//           {selectedDate}
//         </span>
//       </div>
//       {/* Дни недели */}
//       <div
//         style={{
//           display: 'grid',
//           gridTemplateColumns: 'repeat(7, 1fr)',
//           gap: '8px',
//           marginBottom: '16px',
//           textAlign: 'center',
//         }}
//       >
//         {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
//           <div key={day} style={{ color: '#6b7280', fontSize: '14px' }}>
//             {day}
//           </div>
//         ))}
//       </div>

//       {/* Числа */}
//       <div
//         style={{
//           display: 'grid',
//           gridTemplateColumns: 'repeat(7, 1fr)',
//           gap: '8px',
//           textAlign: 'center',
//         }}
//       >
//         {calendarDays.map((day, index) => {
//           const dayString = day ? `${day} янв` : '';
//           const hasBooking =
//             dayString &&
//             bookings.some(
//               (booking) =>
//                 booking.date === dayString || booking.date?.includes(day || '')
//             );

//           if (!day) return null;

//           const isSelected = day === selectedDayNumber;

//           return (
//             <div
//               key={index}
//               style={{
//                 padding: '12px 8px',
//                 borderRadius: '8px',
//                 backgroundColor: isSelected
//                   ? '#3b82f6'
//                   : hasBooking
//                     ? '#374151'
//                     : 'transparent',
//                 color: isSelected ? '#ffffff' : day ? '#ffffff' : 'transparent',
//                 fontWeight: isSelected ? '600' : '400',
//                 cursor: day ? 'pointer' : 'default',
//                 position: 'relative',
//               }}
//               onClick={() => {
//                 if (day) {
//                   setSelectedDate(`${day} янв`);
//                 }
//               }}
//             >
//               {day}
//               {hasBooking && (
//                 <div
//                   style={{
//                     position: 'absolute',
//                     bottom: '4px',
//                     left: '50%',
//                     transform: 'translateX(-50%)',
//                     width: '4px',
//                     height: '4px',
//                     backgroundColor: '#10b981',
//                     borderRadius: '50%',
//                   }}
//                 ></div>
//               )}
//             </div>
//           );
//         })}
//       </div>
//     </div>
//   );
// };
