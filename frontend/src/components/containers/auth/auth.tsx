import { useState } from "react";
import Button from "../../small/button/button";
import Input from "../../small/input/input";
import { useBookingContext } from "../bookingContext/bookingContext";
import { AUTH_CREDENTIALS } from "./authConfig";
import { motion, AnimatePresence } from 'framer-motion';
//анимка загрузки
const Spinner = () => (
    <div className="flex justify-center items-center p-4">
        <span className="loading loading-infinity loading-xl text-primary"></span>
    </div>
);
const formVariants = {
    hidden: { opacity: 0, x: 50, transition: { duration: 0.3 } },
    visible: { opacity: 1, x: 0, transition: { duration: 0.3 } },
    exit: { opacity: 0, x: -50, transition: { duration: 0.3 } }
};

export const AuthContainer = () => {

    const [isLogin, setIsLogin] = useState(true);
    const [confirmPass, setConfirmPass] = useState('');

    const {
        setIsAuthenticated, login, pass, setLogin,
        setPass, isLoading, setIsLoading, error, setError
    } = useBookingContext();


    const handleLogin = () => {
        console.log("LOGIN:", login);
        console.log("PASS:", pass);
        console.log("CONFIRM:", confirmPass);
        setError(false);

        if (isLogin) {
            // ВХОД
            if (login === AUTH_CREDENTIALS.login && pass === AUTH_CREDENTIALS.password) {
                setIsLoading(true);
                setTimeout(() => {
                    setIsAuthenticated(true);
                    setIsLoading(false);
                }, 1500);
            } else {
                setError(true);
            }
        } else {
            // РЕГИСТРАЦИЯ

            if (!pass || !confirmPass || pass !== confirmPass || pass.length < 1) {
                setError(true);
                console.log("Ошибка валидации:", { pass, confirmPass });
                return;
            }

            setIsLoading(true);
            setTimeout(() => {
                AUTH_CREDENTIALS.login = login;
                AUTH_CREDENTIALS.password = pass;
                setIsAuthenticated(true);
                setIsLoading(false);
            }, 1500);
        }
    };



    return (
        <div className="fixed inset-0 flex items-center justify-center bg-black/60 z-50 p-6 backdrop-blur-sm">
            <div className="w-full max-w-sm bg-base-200 p-6 rounded-2xl shadow-xl">
                <h3 className="text-xl font-bold mb-6 text-accent-content">
                    {isLogin ? "Авторизация" : "Регистрация"}
                </h3>

                {error && (
                    <div className="alert alert-error mb-4 py-2 text-sm shadow-lg">
                        <span>{isLogin ? "Неверный логин или пароль" : "Пароли не совпадают"}</span>
                    </div>
                )}

                {isLoading ? (
                    <Spinner />
                ) : (
                    <AnimatePresence mode="wait">
                        <motion.div
                            key={isLogin ? "loginForm" : "registerForm"}
                            variants={formVariants}
                            initial="hidden"
                            animate="visible"
                            exit="exit"
                            className="flex flex-col gap-4"
                        >
                            <Input
                                label="Логин"
                                variant={error ? "error" : "default"}
                                className="bg-base-100"
                                value={login}
                                onChange={(e) => {
                                    setLogin(e.target.value);
                                    if (error) setError(false);
                                }}
                            />
                            <Input
                                label="Пароль"
                                type="password"
                                variant={error ? "error" : "default"}
                                className="bg-base-100"
                                value={pass}
                                onChange={(e) => {
                                    setPass(e.target.value);
                                    if (error) setError(false);
                                }}
                            />
                            {!isLogin && (
                                <Input
                                    label="Повторите пароль"
                                    type="password"
                                    variant={error ? "error" : "default"}
                                    className="bg-base-100"
                                    value={confirmPass}
                                    onChange={(e) => setConfirmPass(e.target.value)}
                                />
                            )}

                            <div className="mt-2">
                                <Button
                                    label={isLogin ? "Войти" : "Зарегистрироваться"}
                                    variant="primary"
                                    width="full"
                                    size="lg"
                                    onClick={handleLogin}
                                    shape="rounded"
                                />
                            </div>
                            <Button
                                variant="secondary"
                                size="sm"
                                width="responsive"
                                label={isLogin ? "Нет аккаунта? Создать" : "Уже есть аккаунт? Войти"}
                                onClick={() => {
                                    setIsLogin(!isLogin);
                                    setError(false);
                                    setPass('');
                                    setConfirmPass('');
                                }}
                                shape="text"
                            >

                            </Button>
                        </motion.div>
                    </AnimatePresence>
                )}
            </div>

        </div>

    );

};
