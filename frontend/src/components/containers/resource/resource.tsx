// import {selectedResource,  selectedDate,
//      setSelectedDate,setSelectedTimeSlot, selectedTimeSlot,
//       setSelectedFilter, selectedFilter } from  '../../../views/main-page/main-page.tsx'

// import type React from 'react';
// import { timeSlots, handleBackClick, calendarDays, filters, bookings, handleResourceClick, handleConfirmBooking } from '../../../views/main-page/main-page.tsx'
import { useBookingContext } from '../../../types/bookingContext.tsx';
// import {  } from "../../../views/main-page/main-page.tsx"
// import { MiniCalendar } from '../calendar/miniCalendar.tsx'
import { Calendar } from '../calendar/calendar.tsx';
import Button from '../../small/button/button.tsx';
import { BlockMiniCalendar } from '../calendar/blockMiniCalendar.tsx';
import { BookingCard } from '../booking-card/booking-card.tsx';

import { motion, AnimatePresence } from 'framer-motion';

export const ResourcesScreen = () => {
  const { setSelectedFilter, selectedFilter, bookings, filters } =
    useBookingContext();

  const filteredBookings = bookings.filter((booking) =>
    selectedFilter === 'Все' ? true : booking.type === selectedFilter
  );

  return (
    <div style={{ padding: '16px' }}>
      {/* Заголовок */}
      <div style={{ marginBottom: '24px' }}>
        <h1
          style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}
        >
          NightBook
        </h1>
        <p style={{ color: '#6b7280', fontSize: '14px' }}>Ресурсы</p>
      </div>

      {/* Фильтры */}
      <div style={{ marginBottom: '24px' }}>
        <h2
          style={{
            fontSize: '14px',
            fontWeight: '600',
            marginBottom: '12px',
            color: '#9ca3af',
          }}
        >
          Фильтры
        </h2>
        <div className="flex gap-3 overflow-x-auto pb-2">
          {filters.map((filter) => (
            <Button
              key={filter}
              label={`${filter}`}
              onClick={() => setSelectedFilter(filter)}
              shape="rounded"
              size="xs"
              width="responsive"
              disabled={selectedFilter === filter}
            />
          ))}
        </div>
      </div>
      {/* Список бронирований */}
      <div>
        <div className="mb-4 text-sm text-secondary">
          Список ({filteredBookings.length} ресурсов)
        </div>

        <div className="flex flex-col gap-4">
          <AnimatePresence mode="popLayout">
            {filteredBookings.map((booking) => (
              <motion.div
                key={booking.id}
                layout
                initial={{ opacity: 0, y: 0 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.95 }}
                transition={{ duration: 0.2 }}
              >
                <BookingCard data={booking} />
              </motion.div>
            ))}
          </AnimatePresence>
        </div>

        {/* 
                {filteredBookings.map((booking) => (
                    <BookingCard key={booking!.id} data={booking!} />
                ))} */}
      </div>
    </div>
  );
};
export const ResourceDetails = () => {
  const {
    selectedResource,
    // selectedDate,
    setSelectedTimeSlot,
    selectedTimeSlot,
    handleBackClick,
    timeSlots,
    handleConfirmBooking,
  } = useBookingContext();

  if (!selectedResource) return null;

  return (
    <div style={{ padding: '16px', maxWidth: '500px', margin: '0 auto' }}>
      {/* Заголовок с кнопкой назад */}
      <div
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          marginBottom: '24px',
        }}
      >
        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={handleBackClick}
          label="←"
        />

        {/* <button
          onClick={handleBackClick}
          style={{
            backgroundColor: "transparent",
            border: "none",
            color: "#ffffff",
            fontSize: "24px",
            cursor: "pointer",
          }}
        >
          ←
        </button> */}
        <div>
          <h1
            style={{
              fontSize: '24px',
              fontWeight: '700',
              marginBottom: '4px',
            }}
          >
            {selectedResource.title}
          </h1>
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '8px',
              color: '#9ca3af',
            }}
          >
            <span>{selectedResource.type}</span>
            <span>•</span>
            <span>{selectedResource.capacity}</span>
          </div>
        </div>

        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={() => { }}
          label="↗"
          className="ml-auto"
        />

        {/* 
        <button
          style={{
            marginLeft: "auto",
            backgroundColor: "transparent",
            border: "none",
            color: "#3b82f6",
            fontSize: "20px",
            cursor: "pointer",
          }}
        >
          ↗
        </button> */}
      </div>
      {BlockMiniCalendar()}
      {/* Календарь */}

      {/* Слоты времени */}
      <div style={{ marginBottom: '32px' }}>
        <h2
          style={{
            fontSize: '16px',
            fontWeight: '600',
            marginBottom: '30px',
          }}
        >
          {/* Слоты на {selectedDate} */}
        </h2>
        <div className='flex flex-row gap-3 flex-wrap justify-around'>
          {timeSlots.map((slot) => (
            <div className="">
              <Button
                label={slot.time}
                onClick={() => setSelectedTimeSlot(slot.time)}
                size="md"
                variant={selectedTimeSlot === slot.time ? 'primary' : 'secondary'}
                shape="default"
              /></div>
          ))}
        </div>
      </div>

      {/* Итого */}
      <div
        style={{
          backgroundColor: '#1f2937',
          borderRadius: '16px',
          padding: '20px',
          marginBottom: '24px',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            marginBottom: '8px',
          }}
        >
          <span style={{ color: '#9ca3af' }}>Итого</span>
          <span style={{ fontSize: '24px', fontWeight: '700' }}>
            {(selectedResource.price ?? 0).toLocaleString('ru-RU')} ₽
          </span>
        </div>
        <div style={{ color: '#6b7280', fontSize: '14px' }}>
          Слот: {selectedTimeSlot || '—'}
        </div>
      </div>
      {/* Кнопка подтверждения */}
      <Button
        label={'Подтвердить'}
        onClick={handleConfirmBooking}
        disabled={!selectedTimeSlot}
        size="xl"
        width="full"
        variant="primary"
        shape="default"
      />
    </div>
  );
};
