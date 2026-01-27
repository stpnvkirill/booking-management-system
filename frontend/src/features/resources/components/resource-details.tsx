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
              {selectedResource.resource_id}
            </h1>
            <div className="flex items-center gap-2 text-base-300">
              <span>{selectedResource.booking_type}</span>
              <span>•</span>
              <span>{selectedResource.location}</span>
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
        <div className="mb-8">
          <div className="grid grid-cols-4 gap-2 mb-2">
            {timeSlots.map((slot) => (
              <div className="">
                <Button
                  label={slot.time}
                  onClick={() => setSelectedTimeSlot(slot.time)}
                  size="md"
                  variant={
                    selectedTimeSlot === slot.time ? 'primary' : 'secondary'
                  }
                  shape="default"
                />
              </div>
            ))}
          </div>
        </div>

        {/* Итого */}
        <div className="rounded-2xl p-5 mb-6 text-neutral">
          <div className="flex justify-between mb-2">
            <span className="text-neutral">Итого</span>
            <span className="font-bold text-2xl text-neutral">
              {/* {(selectedResource.price ?? 0).toLocaleString('ru-RU')} ₽ */}{' '}
              ЦЕНА
            </span>
          </div>
          <div className="text-accent text-sm">
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
    </div>
  );
};
