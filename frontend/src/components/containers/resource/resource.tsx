// import {selectedResource,  selectedDate,
//      setSelectedDate,setSelectedTimeSlot, selectedTimeSlot, 
//       setSelectedFilter, selectedFilter } from  '../../../views/main-page/main-page.tsx'

// import type React from 'react';
//import { timeSlots, handleBackClick, calendarDays, filters, bookings, handleResourceClick, handleConfirmBooking } from '../../../views/main-page/main-page.tsx'
import { useBookingContext } from '../bookingContext/bookingContext.tsx'
import {renderMiniCalendar} from '../calendar/miniCalendar.tsx'
import { renderCalendarScreen } from '../calendar/calendar.tsx';

export const renderResourcesScreen = () => {

    const { setSelectedFilter, selectedFilter, bookings, filters, handleResourceClick } = useBookingContext();

    return (
    <div style={{ padding: '16px' }}>
        {/* Заголовок */}
        <div style={{ marginBottom: '24px' }}>
            <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>NightBook</h1>
            <p style={{ color: '#6b7280', fontSize: '14px' }}>Ресурсы</p>
        </div>

        {/* Фильтры */}
        <div style={{ marginBottom: '24px' }}>
            <h2 style={{ fontSize: '14px', fontWeight: '600', marginBottom: '12px', color: '#9ca3af' }}>Фильтры</h2>
            <div style={{ display: 'flex', gap: '12px', overflowX: 'auto', paddingBottom: '8px' }}>
                {filters.map(filter => (
                    <button
                        key={filter}
                        onClick={() => setSelectedFilter(filter)}
                        style={{
                            padding: '8px 16px',
                            borderRadius: '20px',
                            border: 'none',
                            backgroundColor: selectedFilter === filter ? '#3b82f6' : '#1f2937',
                            color: selectedFilter === filter ? '#ffffff' : '#9ca3af',
                            fontSize: '14px',
                            fontWeight: '500',
                            whiteSpace: 'nowrap',
                            cursor: 'pointer'
                        }}
                    >
                        {filter}
                    </button>
                ))}
            </div>
        </div>

        {/* Список бронирований */}
        <div>
            <div style={{ marginBottom: '16px', color: '#9ca3af', fontSize: '14px' }}>
                Список (5 бронирований)
            </div>

            {bookings.map(booking => (
                <div
                    key={booking.id}
                    onClick={() => handleResourceClick(booking)}
                    style={{
                        backgroundColor: '#1f2937',
                        borderRadius: '16px',
                        padding: '20px',
                        marginBottom: '16px',
                        cursor: 'pointer',
                        transition: 'all 0.2s ease'
                    }}
                    onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#374151'}
                    onMouseOut={(e) => e.currentTarget.style.backgroundColor = '#1f2937'}
                >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                        <div>
                            <h3 style={{ fontSize: '18px', fontWeight: '600', marginBottom: '4px' }}>{booking.title}</h3>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '8px' }}>
                                <span style={{
                                    backgroundColor: '#374151',
                                    color: '#9ca3af',
                                    padding: '2px 8px',
                                    borderRadius: '12px',
                                    fontSize: '12px',
                                    fontWeight: '500'
                                }}>
                                    {booking.type}
                                </span>
                                <span style={{ color: '#9ca3af', fontSize: '14px' }}>•</span>
                                <span style={{ color: '#9ca3af', fontSize: '14px' }}>{booking.capacity}</span>
                            </div>
                            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                                <span style={{ color: '#9ca3af', fontSize: '14px' }}>📌 {booking.location}</span>
                                <span style={{ color: '#fbbf24' }}>★ {booking.rating}</span>
                                {booking.timeLeft && (
                                    <span style={{ color: '#6b7280', fontSize: '14px' }}>🔽 {booking.timeLeft}</span>
                                )}
                            </div>
                        </div>

                        <div style={{ textAlign: 'right' }}>
                            <div style={{ fontSize: '20px', fontWeight: '700', marginBottom: '8px' }}>
                                {booking.price.toLocaleString('ru-RU')} ₽
                            </div>
                            <div style={{ display: 'flex', gap: '8px' }}>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleResourceClick(booking);
                                    }}
                                    style={{
                                        padding: '8px 16px',
                                        backgroundColor: 'transparent',
                                        border: '1px solid #4b5563',
                                        borderRadius: '8px',
                                        color: '#ffffff',
                                        fontSize: '14px',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Открыть
                                </button>
                                <button
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        handleResourceClick(booking);
                                    }}
                                    style={{
                                        padding: '8px 16px',
                                        backgroundColor: '#3b82f6',
                                        border: 'none',
                                        borderRadius: '8px',
                                        color: '#ffffff',
                                        fontSize: '14px',
                                        fontWeight: '500',
                                        cursor: 'pointer'
                                    }}
                                >
                                    Бронь
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    </div>
    )
}



export const renderResourceDetails = () => {

    const { selectedResource, selectedDate,
        setSelectedTimeSlot, selectedTimeSlot, handleBackClick, timeSlots, handleConfirmBooking } = useBookingContext();

    if (!selectedResource) return null;

    return (
        <div style={{ padding: '16px', maxWidth: '500px', margin: '0 auto' }}>
            {/* Заголовок с кнопкой назад */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '12px', marginBottom: '24px' }}>
                <button
                    onClick={handleBackClick}
                    style={{
                        backgroundColor: 'transparent',
                        border: 'none',
                        color: '#ffffff',
                        fontSize: '24px',
                        cursor: 'pointer'
                    }}
                >
                    ←
                </button>
                <div>
                    <h1 style={{ fontSize: '24px', fontWeight: '700', marginBottom: '4px' }}>{selectedResource.title}</h1>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '8px', color: '#9ca3af' }}>
                        <span>{selectedResource.type}</span>
                        <span>•</span>
                        <span>{selectedResource.capacity}</span>
                    </div>
                </div>
                <button
                    style={{
                        marginLeft: 'auto',
                        backgroundColor: 'transparent',
                        border: 'none',
                        color: '#3b82f6',
                        fontSize: '20px',
                        cursor: 'pointer'
                    }}
                >
                    ↗
                </button>
            </div>
            {(renderMiniCalendar())}
            {/* Календарь */}
            

            {/* Слоты времени */}
            <div style={{ marginBottom: '32px' }}>
                <h2 style={{ fontSize: '16px', fontWeight: '600', marginBottom: '16px' }}>
                    Слоты на {selectedDate}
                </h2>
                <div style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(5, 1fr)',
                    gap: '12px'
                }}>
                    {timeSlots.map((slot) => (
                        <button
                            key={slot.time}
                            onClick={() => setSelectedTimeSlot(slot.time)}
                            style={{
                                padding: '12px 8px',
                                backgroundColor: selectedTimeSlot === slot.time ? '#3b82f6' : '#1f2937',
                                border: 'none',
                                borderRadius: '8px',
                                color: selectedTimeSlot === slot.time ? '#ffffff' : '#9ca3af',
                                fontSize: '14px',
                                fontWeight: '500',
                                cursor: 'pointer'
                            }}
                        >
                            {slot.time}
                        </button>
                    ))}
                </div>
            </div>

            {/* Итого */}
            <div style={{
                backgroundColor: '#1f2937',
                borderRadius: '16px',
                padding: '20px',
                marginBottom: '24px'
            }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                    <span style={{ color: '#9ca3af' }}>Итого</span>
                    <span style={{ fontSize: '24px', fontWeight: '700' }}>
                        {selectedResource.price.toLocaleString('ru-RU')} ₽
                    </span>
                </div>
                <div style={{ color: '#6b7280', fontSize: '14px' }}>
                    Слот: {selectedTimeSlot || '—'}
                </div>
            </div>

            {/* Кнопка подтверждения */}
            <button
                onClick={handleConfirmBooking}
                disabled={!selectedTimeSlot}
                style={{
                    width: '100%',
                    padding: '16px',
                    backgroundColor: selectedTimeSlot ? '#3b82f6' : '#374151',
                    border: 'none',
                    borderRadius: '12px',
                    color: '#ffffff',
                    fontSize: '16px',
                    fontWeight: '600',
                    cursor: selectedTimeSlot ? 'pointer' : 'not-allowed'
                }}
            >
                Подтвердить
            </button>
        </div>
    )
}