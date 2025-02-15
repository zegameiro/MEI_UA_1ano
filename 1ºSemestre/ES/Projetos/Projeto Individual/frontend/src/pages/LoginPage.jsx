import { useState } from "react";
import { Divider, Link } from "@nextui-org/react";
import { GoogleLogin } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import { jwtDecode } from "jwt-decode";

import { MdError } from "react-icons/md";
import { FaCircleCheck } from "react-icons/fa6";

import { LogoVertical } from "../assets";
import { useUserStore } from "../stores/userStore";

const LoginPage = () => {
  const navigate = useNavigate();
  const [loginState, setLoginState] = useState(); // 0 - login successfull; 1 - login failure
  const loginStore = useUserStore((state) => state.login) || false;
  const isLoggedIn = useUserStore((state) => state.isLoggedIn) || false;

  const successLogin = (response) => {
    const credentials = jwtDecode(response.credential);

    setLoginState(0);
    loginStore(credentials.name, credentials.picture, response.credential);

    setTimeout(() => {
      navigate("/home");
    });
  };

  const errorMessage = (error) => {
    console.log(error);
    setLoginState(1);
  };

  return (
    <main className="flex flex-col bg-gradient-to-tr from-primary to-background">
      <div className="flex flex-col px-[10%] py-[5%] justify-center min-h-screen">
        <div className="flex flex-col lg:flex-row border-2 p-4 rounded-xl shadow-lg justify-evenly bg-background">
          <div className="flex flex-row justify-center items-center space-x-10">
            <Link href="/" className="cursor-pointer">
              <img src={LogoVertical} alt="TaskFlow Logo" />
            </Link>
            <p className="text-nowrap text-2xl font-semibold">
              Structure your <span className="text-primary">Tasks</span>,<br />{" "}
              Master your <span className="text-[#7d47a4]">Workflow</span>
            </p>
          </div>

          <Divider
            orientation="vertical"
            className="hidden lg:flex my-4 h-[10vw]"
          />
          <Divider
            orientation="horizontal"
            className="flex lg:hidden my-4 w-full"
          />

          <div className="flex flex-col justify-center items-center space-y-2">
            <span className="text-center">
              <h1 className="text-2xl font-bold">Login with</h1>
            </span>
            {loginState == 1 ? ( // Error message either from Google OAuth2 or from the API
              <span className="flex flex-row gap-1 items-center text-error font-semibold">
                <MdError className="text-lg" />
                <p>Error login in</p>
              </span>
            ) : loginState == 2 ? ( // Success message
              <span className="flex flex-row gap-1 items-center text-success font-semibold">
                <FaCircleCheck /> Logged in with success
              </span>
            ) : (
              // Google Login element (default case)
              !isLoggedIn && (
                <GoogleLogin onSuccess={successLogin} onError={errorMessage} />
              )
            )}
          </div>
        </div>
      </div>
    </main>
  );
};

export default LoginPage;
