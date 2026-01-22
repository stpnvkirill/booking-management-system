// import {selectedResource,  selectedDate,
//      setSelectedDate,setSelectedTimeSlot, selectedTimeSlot,
//       setSelectedFilter, selectedFilter } from  '../../../views/main-page/main-page.tsx'

// import type React from 'react';
//import { timeSlots, handleBackClick, calendarDays, filters, bookings, handleResourceClick, handleConfirmBooking } from '../../../views/main-page/main-page.tsx'
import { useBookingContext } from "../bookingContext/bookingContext.tsx";

// import { MiniCalendar } from '../calendar/miniCalendar.tsx'
// import { Calendar } from '../calendar/calendar.tsx';
import Button from "../../small/button/button.tsx";
import { BlockMiniCalendar } from "../calendar/blockMiniCalendar.tsx";

export const ResourcesScreen = () => {
  const {
    setSelectedFilter,
    selectedFilter,
    bookings,
    filters,
    handleResourceClick,
  } = useBookingContext();
  return (
    <div style={{ padding: "16px" }}>
      {/* Заголовок */}
      <div style={{ marginBottom: "24px" }}>
        <h1
          style={{ fontSize: "28px", fontWeight: "700", marginBottom: "8px" }}
        >
          NightBook
        </h1>
        <p style={{ color: "#6b7280", fontSize: "14px" }}>Ресурсы</p>
      </div>

      {/* Фильтры */}
      <div style={{ marginBottom: "24px" }}>
        <h2
          style={{
            fontSize: "14px",
            fontWeight: "600",
            marginBottom: "12px",
            color: "#9ca3af",
          }}
        >
          Фильтры
        </h2>
        <div
          style={{
            display: "flex",
            gap: "12px",
            overflowX: "auto",
            paddingBottom: "8px",
          }}
        >
          {filters.map((filter) => (
            // <button
            //   key={filter}
            //   onClick={() => setSelectedFilter(filter)}
            //   style={{
            //     padding: "8px 16px",
            //     borderRadius: "20px",
            //     border: "none",
            //     backgroundColor:
            //       selectedFilter === filter ? "#3b82f6" : "#1f2937",
            //     color: selectedFilter === filter ? "#ffffff" : "#9ca3af",
            //     fontSize: "14px",
            //     fontWeight: "500",
            //     whiteSpace: "nowrap",
            //     cursor: "pointer",
            //   }}
            // >
            //   {filter}
            // </button>

            <Button
              key={filter}
              label={`${filter}`}
              onClick={() => setSelectedFilter(filter)}
              isCircle
              size="xs"
              width="responsive"
              disabled={selectedFilter === filter}
            />
          ))}
        </div>
      </div>

      {/* Список бронирований */}
      <div>
        <div
          style={{ marginBottom: "16px", color: "#9ca3af", fontSize: "14px" }}
        >
          Список (5 бронирований)
        </div>

        {bookings.map((booking) => (
          <div
            key={booking.id}
            onClick={() => handleResourceClick(booking)}
            style={{
              backgroundColor: "#1f2937",
              borderRadius: "16px",
              padding: "20px",
              marginBottom: "16px",
              cursor: "pointer",
              transition: "all 0.2s ease",
            }}
            onMouseOver={(e) =>
              (e.currentTarget.style.backgroundColor = "#374151")
            }
            onMouseOut={(e) =>
              (e.currentTarget.style.backgroundColor = "#1f2937")
            }
          >
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "flex-start",
                marginBottom: "12px",
              }}
            >
              <div>
                <h3
                  style={{
                    fontSize: "18px",
                    fontWeight: "600",
                    marginBottom: "4px",
                  }}
                >
                  {booking.title}
                </h3>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "8px",
                    marginBottom: "8px",
                  }}
                >
                  <span
                    style={{
                      backgroundColor: "#374151",
                      color: "#9ca3af",
                      padding: "2px 8px",
                      borderRadius: "12px",
                      fontSize: "12px",
                      fontWeight: "500",
                    }}
                  >
                    {booking.type}
                  </span>
                  <span style={{ color: "#9ca3af", fontSize: "14px" }}>•</span>
                  <span style={{ color: "#9ca3af", fontSize: "14px" }}>
                    {booking.capacity}
                  </span>
                </div>
                <div
                  style={{ display: "flex", alignItems: "center", gap: "8px" }}
                >
                  <span style={{ color: "#9ca3af", fontSize: "14px" }}>
                    📌 {booking.location}
                  </span>
                  <span style={{ color: "#fbbf24" }}>★ {booking.rating}</span>
                  {booking.timeLeft && (
                    <span style={{ color: "#6b7280", fontSize: "14px" }}>
                      🔽 {booking.timeLeft}
                    </span>
                  )}
                </div>
              </div>

              <div style={{ textAlign: "right" }}>
                <div
                  style={{
                    fontSize: "20px",
                    fontWeight: "700",
                    marginBottom: "8px",
                  }}
                >
                  {booking.price.toLocaleString("ru-RU")} ₽
                </div>
                <div className="flex flex-col gap-2">
                  <Button
                    label="Открыть"
                    onClick={() => {
                      handleResourceClick(booking);
                    }}
                    size="sm"
                    variant="primary"
                    width="responsive"
                  />
                  <Button
                    label="Бронь"
                    onClick={() => {
                      handleResourceClick(booking);
                    }}
                    variant="info"
                    width="responsive"
                    size="sm"
                  />
                </div>
              </div>
            </div>
          </div>
        ))}
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
    <div style={{ padding: "16px", maxWidth: "500px", margin: "0 auto" }}>
      {/* Заголовок с кнопкой назад */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "12px",
          marginBottom: "24px",
        }}
      >
        <button
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
        </button>
        <div>
          <h1
            style={{
              fontSize: "24px",
              fontWeight: "700",
              marginBottom: "4px",
            }}
          >
            {selectedResource.title}
          </h1>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              color: "#9ca3af",
            }}
          >
            <span>{selectedResource.type}</span>
            <span>•</span>
            <span>{selectedResource.capacity}</span>
          </div>
        </div>
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
        </button>
      </div>
      {BlockMiniCalendar()}
      {/* Календарь */}

      {/* Слоты времени */}
      <div style={{ marginBottom: "32px" }}>
        <h2
          style={{
            fontSize: "16px",
            fontWeight: "600",
            marginBottom: "30px",
          }}
        >
          {/* Слоты на {selectedDate} */}
        </h2>
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "repeat(5, 1fr)",
            gap: "12px",
          }}
        >
          {timeSlots.map((slot) => (
            <Button
              label={slot.time}
              onClick={() => setSelectedTimeSlot(slot.time)}
              size="md"
              variant={selectedTimeSlot === slot.time ? "primary" : "secondary"}
              isCircle={false}
            />
          ))}
        </div>
      </div>

      {/* Итого */}
      <div
        style={{
          backgroundColor: "#1f2937",
          borderRadius: "16px",
          padding: "20px",
          marginBottom: "24px",
        }}
      >
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            marginBottom: "8px",
          }}
        >
          <span style={{ color: "#9ca3af" }}>Итого</span>
          <span style={{ fontSize: "24px", fontWeight: "700" }}>
            {selectedResource.price.toLocaleString("ru-RU")} ₽
          </span>
        </div>
        <div style={{ color: "#6b7280", fontSize: "14px" }}>
          Слот: {selectedTimeSlot || "—"}
        </div>
      </div>
      {/* Кнопка подтверждения */}
      <Button
        label={"Подтвердить"}
        onClick={handleConfirmBooking}
        disabled={!selectedTimeSlot}
        size="xl"
        width="full"
        variant="primary"
        isCircle={true}
      />
    </div>
  );
};
