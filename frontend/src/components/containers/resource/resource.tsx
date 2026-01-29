import { useBookingContext } from '../../../types/bookingContext.tsx';
import Button from '../../small/button/button.tsx';
import { BlockMiniCalendar } from '../calendar/blockMiniCalendar.tsx';
import { BookingCard } from '../booking-card/booking-card.tsx';
import { motion, AnimatePresence } from 'framer-motion';

export const ResourcesScreen = () => {
  const { setSelectedFilter, selectedFilter, bookings, filters } =
    useBookingContext();

  const filteredBookings = bookings.filter((booking) =>
    selectedFilter === 'Все' ? true : booking.description === selectedFilter
  );

  return (
    <div className="pb-20 h-screen bg-neutral-content text-neutral font-sans">
      <div className="p-4">
        {/* Заголовок */}
        <div className="mb-6">
          <h1 className="text-3xl text-neutral font-bold mb-2">NightBook</h1>
          <p className="text-base-300 text-sm">Ресурсы</p>
        </div>
        {/* Фильтры */}
        <div className="mb-6">
          <h2 className="text-sm text-accent-content font-semibold mb-3">
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

        <div className="mb-4 text-sm text-secondary">
          Список ({filteredBookings.length} ресурсов)
        </div>
        {/* <div> */}
        <div className="flex flex-col gap-4 max-h-[calc(100vh-290px)] overflow-y-scroll">
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
    bookingRange,
    setBookingRange,
    handleTimeClick,
    handleConfirmBooking,
  } = useBookingContext();

  const endSlots = timeSlots.filter(slot => {
    if (!bookingRange.start) return false;
    return slot.time > bookingRange.start;
  });

  const step = !bookingRange.start
    ? 'SELECT_START'
    : (!bookingRange.end ? 'SELECT_END' : 'COMPLETED');

  const resetBookingRange = () => {
    setBookingRange({ start: null, end: null });
  };

  if (!selectedResource) return null;
  return (
    ///////////от сюда
    <div className="pb-20 bg-neutral-content text-neutral font-sans">
      <div className="p-4 max-w-125 mt-0 mb-0  ml-auto mr-auto">
        {/* Заголовок с кнопкой назад */}
        <div className="flex items-center gap-3 mb-6">
          <Button
            variant="primary"
            size="lg"
            width="responsive"
            shape="text"
            onClick={handleBackClick}
            label="←"
          />
          <div>
            <h1 className="text-2xl font-bold mb-1">
              {selectedResource.description}
            </h1>
            <div className="flex items-center gap-2 text-base-300">
              <span>{selectedResource.booking_type}</span>
              <span>•</span>
              <span>{selectedResource.capacity}</span>
            </div>
          </div>
          {/* 
        // А нужна ли тут эта кнопка вообще
        <Button
          variant="primary"
          size="lg"
          width="responsive"
          shape="text"
          onClick={() => { }}
          label="↗"
          className="ml-auto"
        /> */}
        </div>
        <BlockMiniCalendar />
        {/* Календарь */}




        {/* Слоты времени */}
        {/* <div className="mb-8 min-h-[200px]"> */}
        {/* <div className="grid grid-cols-4 gap-2 mb-2"> */}
        {step === 'SELECT_START' && (
          <div>
            <h3 className="text-sm font-semibold mb-3">Выберите время начала:</h3>
            <div className="grid grid-cols-4 gap-2">
              {timeSlots.map((slot) => (
                <Button
                  key={slot.time}
                  label={slot.time}
                  onClick={() => setBookingRange({ start: slot.time, end: null })}
                  variant="secondary"
                />
              ))}

            </div>
          </div>
        )}

        {step === 'SELECT_END' && (
          <motion.div initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}>
            <div className="flex justify-between items-center mb-3">
              <h3 className="text-sm font-semibold">Выберите время окончания:</h3>
              <button
                onClick={() => setBookingRange({ start: null, end: null })}
                className="text-xs text-primary underline"
              >
                Изменить старт ({bookingRange.start})
              </button>
            </div>
            <div className="grid grid-cols-4 gap-2">
              {timeSlots
                .filter(slot => slot.time > bookingRange.start!)
                .map((slot) => (
                  <Button
                    key={slot.time}
                    label={slot.time}
                    onClick={() => setBookingRange({ ...bookingRange, end: slot.time })}
                    variant="primary"
                    shape="outline"
                  />
                ))}
            </div>
          </motion.div>
        )}


        {step === 'COMPLETED' && (
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="rounded-2xl p-5 mb-6 text-neutral bg-base-200"
          >
            <div className="flex justify-between mb-2">
              <span className="text-neutral">Итого</span>
              <span className="font-bold text-2xl text-neutral">
                {(selectedResource.price ?? 0).toLocaleString('ru-RU')} ₽
              </span>
            </div>

            <div className="text-accent text-sm font-medium">
              Выбрано: **{bookingRange.start} — {bookingRange.end}**
            </div>
          </motion.div>
        )}




        <AnimatePresence>
          {step === 'COMPLETED' && (
            <motion.div initial={{ y: 20, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              className="grid grid-cols-12 gap-4 w-full mt-6" >



              <Button
                label="Подтвердить бронь"
                onClick={handleConfirmBooking}
                size="xl"
                width="full"
                variant="primary"
                shape="rounded"
                className="col-span-6"
              />

              <Button
                label="Сбросить"
                onClick={resetBookingRange}
                disabled={false}
                size="xl"
                width="full"
                variant="info"
                shape="rounded"
                className="col-span-6"
              />


            </motion.div>
          )}
        </AnimatePresence>

        {/* </div> */}
      </div>
    </div>

  );
};
