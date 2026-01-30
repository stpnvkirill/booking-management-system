import { AUTH_CREDENTIALS } from '@/shared/types/constants';
import { useState } from 'react';
export default function ProfileSettings() {
  const user = window.Telegram?.WebApp?.initDataUnsafe?.user;
  const [isChecked, setIsChecked] = useState(true);
  const handleChange = () => {
    setIsChecked((prev) => !prev);
  };
  return (
    <div className="mb-8 bg-base-200 rounded-2xl p-5 flex items-center justify-between">
      <div className="flex items-center gap-3">
        <div className="w-16 h-16 bg-accent rounded-full flex items-center justify-center font-semibold">
          {user?.photo_url ? (
            <img
              className="rounded-full"
              src={user?.photo_url}
              alt={user?.photo_url || '404'}
            />
          ) : user?.first_name && user?.last_name ? (
            `${user?.first_name?.charAt(0) || ''} ${user?.last_name?.charAt(0) || ''}`
          ) : (
            `404`
          )}
        </div>
        <div>
          <div className="text-base font-semibold mb-1">
            {user?.username || AUTH_CREDENTIALS.login}
          </div>
          <div className="flex items-center text-sm">
            <input
              type="checkbox"
              className="checkbox checkbox-primary mr-2"
              onChange={handleChange}
              checked={isChecked}
            />
            <span className="text-base">
              {isChecked ? 'Уведомления включены' : 'Уведомления выключены'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
