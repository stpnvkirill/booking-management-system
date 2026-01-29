/* eslint-disable react-refresh/only-export-components */
export function firstBigLetter(string: string | undefined): string {
  if (!string) return ''; // Обработка пустой строки
  return string.charAt(0).toUpperCase() + string.slice(1);
};
export function getDaysInMonth(year: number, month: number) {
  const date = new Date(year, month, 1);
  const days = [];

  const firstDayOfWeek = date.getDay();

  const offset = firstDayOfWeek === 0 ? 6 : firstDayOfWeek - 1;

  for (let i = 0; i < offset; i++) {
    days.push(null);
  }

  while (date.getMonth() === month) {
    days.push(date.getDate());
    date.setDate(date.getDate() + 1);
  }
  return days;
};


// export default { getDaysInMonth, firstBigLetter };
