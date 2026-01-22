import Button from "../../small/button/button";

export const renderProfileScreen = () => {
  window.Telegram?.WebApp?.ready();
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  return (
    <div className="p-4">
      {/* Заголовок */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Профиль</h1>
        <p className="text-sm" style={{ color: "#6b7280", fontSize: "14px" }}>
          Личный кабинет
        </p>
      </div>
      {/* Настройки */}
      <div className="mb-8">
        <h2 className="text-base font-semibold mb-4">Настройки</h2>
        <div className="rounded-2xl p-5 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center font-semibold">
              {user?.username || "404"}
            </div>
            <div>
              <div className="text-base font-semibold mb-1">
                {user?.username || "anonymous"}
              </div>
              <div className="flex items-center gap-2 text-sm">
                <span className="w-2 h-2 rounded-full" />
                Уведомления включены
              </div>
            </div>
          </div>
        </div>
      </div>
      {/* Активные бронирования */}
      <div className="mb-8">
        <div className="flex gap-3 mb-4">
          <Button
            onClick={() => {}}
            label="Активные"
            variant="primary"
            width="responsive"
            size="md"
            shape="rounded"
          ></Button>
          <Button
            onClick={() => {}}
            label="История"
            variant="secondary"
            width="responsive"
            size="md"
            shape="rounded"
          ></Button>
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
        <div className="flex gap-3 justify-center flex-row ">
          <div className="w-full">
            <Button
              onClick={() => {}}
              label="Открыть"
              variant="primary"
              size="md"
              width="full"
            ></Button>
          </div>
          <div className="w-full">
            <Button
              onClick={() => {}}
              label="Отменить"
              variant="info"
              size="md"
              width="full"
            ></Button>
          </div>
        </div>
      </div>
      {/* Кнопка выхода */}
      <div className="m-1">
        <Button
          label={"Выйти"}
          variant="error"
          size="lg"
          width="full"
          onClick={() => {}}
        ></Button>
      </div>
    </div>
  );
};
