function examplePage2() {
  window.Telegram?.WebApp?.ready();
  // Данные пользователя telegram
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;

  //   const theme = window.Telegram?.WebApp?.themeParams;
  // Используем цвета из темы Telegram
  //   const bgColor = theme?.bg_color || "#0a0a0a";
  //   const textColor = theme?.text_color || "#ffffff";
  //   const buttonColor = theme?.button_color || "#3b82f6";
  //   const linkColor = theme?.link_color || "#06b6d4";
  //   const hintColor = theme?.hint_color || "#6b7280";
  return (
    <>
      <div>
        Hello, {user?.first_name}! <br /> Your username is @{user?.username}
      </div>
    </>
  );
}
export default examplePage2;
