  export const renderProfileScreen = () => (
    <div style={{ padding: '16px' }}>
      {/* Заголовок */}
      <div style={{ marginBottom: '32px' }}>
        <h1 style={{ fontSize: '28px', fontWeight: '700', marginBottom: '8px' }}>Профиль</h1>
        <p style={{ color: '#6b7280', fontSize: '14px' }}>Личный кабинет</p>
      </div>

      {/* Настройки */}
<div className="mb-8">
  <h2 className="text-base font-semibold mb-4">Настройки</h2>

  <div className="rounded-2xl p-5 flex items-center justify-between">
    <div className="flex items-center gap-3">
      <div className="w-10 h-10 rounded-full flex items-center justify-center font-semibold">
        Asta
      </div>

      <div>
        <div className="text-base font-semibold mb-1">Asta</div>

        <div className="flex items-center gap-2 text-sm">
          <span className="w-2 h-2 rounded-full" />
          уведомления включены
        </div>
      </div>
    </div>
  </div>
</div>

      {/* Активные бронирования */}
<div className="mb-8">
  <div className="flex mb-4">
    <button className="px-4 py-2 mr-3 rounded-full text-sm font-medium bg-primary text-primary-content border-none">
      Активные
    </button>
    <button className="px-4 py-2 rounded-full text-sm font-medium bg-base-100 text-base-content border border-base-300">
      История
    </button>
  </div>
</div>

        {/* Активное бронирование */}
<div className="mb-4 rounded-2xl p-5 bg-base-200">
  <div className="mb-3">
    <div className="text-lg font-semibold mb-1 text-base-content">
      Loft Noir
    </div>
    <div className="text-sm text-base-content/60">
      15 янв • 19:00–23:00
    </div>
  </div>

  <div className="flex gap-3">
    <button className="flex-1 px-3 py-3 rounded-lg text-sm font-medium bg-base-100 text-base-content border border-base-300 cursor-pointer">
      Открыть
    </button>
    <button className="flex-1 px-3 py-3 rounded-lg text-sm font-medium bg-error text-error-content border-none cursor-pointer">
      Отменить
    </button>
  </div>
</div>

      {/* Кнопка выхода */}
<button className="w-full px-4 py-4 rounded-xl text-lg font-semibold border border-base-300 bg-base-100 text-error cursor-pointer">
  Выйти
</button>
</div>
  );