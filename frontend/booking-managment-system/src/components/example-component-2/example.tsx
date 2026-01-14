import React from "react";
import "../../styles/App.css";
interface WelcomeMessageProps {
  name: string;
  count: number;
  isLoggedIn: boolean;
}
const WelcomeMessage2 = ({
  name,
  count,
  isLoggedIn,
}: WelcomeMessageProps): React.ReactElement => {
  return (
    <div>
      {isLoggedIn ? (
        <h1>
          Welcome back, {name}! You have {count} new messages.
        </h1>
      ) : (
        <h1>Welcome to the site! Please log in.</h1>
      )}
    </div>
  );
};

export default WelcomeMessage2;
