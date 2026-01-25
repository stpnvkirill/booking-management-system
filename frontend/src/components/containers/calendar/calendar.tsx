// import { selectedDate, setSelectedDate, setSelectedResource, setActiveTab } from '../../../App.tsx'
import { useBookingContext } from '../../../types/bookingContext.tsx';
import Button from '../../small/button/button.tsx';
import { BookingCardCalendar } from '../booking-card/booking-card-calendar.tsx';
import { motion, AnimatePresence } from 'framer-motion';

export const Calendar = () => {
    const {
        selectedDate,
        setSelectedDate,
        bookings,
        viewDate, setViewDate, getDaysInMonth
    } = useBookingContext();

    const monthNames = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ];
    const currentMonth = viewDate.getMonth();
    const currentYear = viewDate.getFullYear();

    const handlePrevMonth = () => {
        setViewDate(new Date(currentYear, currentMonth - 1, 1));
    };

    const handleNextMonth = () => {
        setViewDate(new Date(currentYear, currentMonth + 1, 1));
    };
    const days = getDaysInMonth(currentYear, currentMonth);

    const getSelectedDayNumber = () => {
        const match = selectedDate.match(/\d+/);
        return match ? match[0] : null;
    };

    const selectedDayNumber = getSelectedDayNumber();
    // console.log(bookings);
    return (
        <div style={{ padding: '16px' }}>
            {/* Заголовок */}
            <div style={{ marginBottom: '24px' }}>
                <h1
                    style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}
                >
                    Календарь
                </h1>
                <p style={{ color: '#6b7280', fontSize: '14px' }}>
                    Расписание бронирований
                </p>
            </div>
            {/* Текущий месяц */}
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
                        alignItems: 'center',
                        marginBottom: '20px',
                    }}
                >
                    <Button
                        variant="primary"
                        size="lg"
                        width="responsive"
                        shape="text"
                        onClick={handlePrevMonth}
                        label="←"
                    />
                    <h2 style={{ fontSize: '18px', fontWeight: '600' }}>{monthNames[currentMonth]} {currentYear}</h2>
                    <Button
                        variant="primary"
                        size="lg"
                        width="responsive"
                        shape="text"
                        onClick={handleNextMonth}
                        label="→"
                    />
                </div>
                {/* Дни недели */}
                <div
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(7, 1fr)',
                        gap: '2px',
                        marginBottom: '16px',
                        textAlign: 'center',
                    }}
                >
                    {['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].map((day) => (
                        <div key={day} style={{ color: '#6b7280', fontSize: '14px' }}>
                            {day}
                        </div>
                    ))}
                </div>
                {/* Числа месяца с бронированиями */}
                <div
                    style={{
                        display: 'grid',
                        gridTemplateColumns: 'repeat(7, 1fr)',
                        gap: '8px',
                        textAlign: 'center',
                    }}
                >
                    {/* {calendarDays.map((day, index) => {
                        const dayString = day ? `${day} янв` : '';
                        const hasBooking =
                            dayString &&
                            bookings.some((booking) => booking.date === dayString);
                        if (!day) return null;
                        const isSelected = day === selectedDayNumber; */}

                    {days.map((day, index) => {
                        if (!day) return <div key={`empty-${index}`} />; // Пустая ячейка для отступа

                        const dayString = `${day} ${monthNames[currentMonth].slice(0, 3).toLowerCase()}`;
                        const isSelected = day.toString() === selectedDayNumber;
                        const hasBooking = bookings.some(b => b.date === dayString);

                        return (
                            <Button
                                key={index}
                                // disabled={isSelected}
                                label={day.toString()}
                                size="md"
                                width="auto"
                                onClick={() => {
                                    if (day && !isSelected) {
                                        setSelectedDate(dayString);
                                    }
                                }}
                                shape="default"
                                className={`relative ${isSelected
                                    ? ''
                                    : '!bg-[#1f2937] !border-none !shadow-none hover:!bg-[#374151]'
                                    } ${hasBooking ? 'btn-active' : ''}`}
                            >
                                {hasBooking && (
                                    <div
                                        style={{
                                            position: 'absolute',
                                            bottom: '4px',
                                            left: '50%',
                                            transform: 'translateX(-50%)',
                                            width: '4px',
                                            height: '4px',
                                            backgroundColor: '#00000',
                                            borderRadius: '50%',
                                        }}
                                    ></div>
                                )}
                            </Button>
                        );
                    })}
                </div>
            </div>
            {/* Предстоящие бронирования на выбранную дату */}

            <AnimatePresence mode="wait">
                <motion.div
                    key={selectedDate}
                    initial={{ opacity: 0, y: 0 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 0 }}
                    transition={{ duration: 0.2 }}
                >
                    <BookingCardCalendar
                        bookings={bookings}
                        selectedDate={selectedDate}
                    />
                </motion.div>
            </AnimatePresence>

            {/* <BookingCardCalendar
        key={selectedDate}
        bookings={bookings}
        selectedDate={selectedDate}
      ></BookingCardCalendar> */}
        </div>
    );
};
