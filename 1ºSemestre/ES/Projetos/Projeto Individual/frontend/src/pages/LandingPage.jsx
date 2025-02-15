import { Image, Button } from "@nextui-org/react";
import { FaTasks } from "react-icons/fa";
import { useNavigate } from "react-router-dom";

import { LogoVertical } from "../assets";
import { useUserStore } from "../stores/userStore";

const LandingPage = () => {
  const navigate = useNavigate();
  const isLoggedIn = useUserStore((state) => state.isLoggedIn) || false;

  return (
    <div className="flex flex-row items-center justify-evenly min-h-[75vh]">
      <Image src={LogoVertical} alt="TaskFlow logo" width={300} />
      <div className="max-w-sm text-center lg:text-right lg:max-w-md">
        <h1 className="text-xl font-bold lg:text-5xl">TaskFlow</h1>
        <p className="py-6 text-xl">
          Effortlessly manage your tasks with secure access, deadlines,
          priorities, and complete control over your workflow.
        </p>
        {!isLoggedIn && (
          <Button
            color="primary"
            className="text-lg"
            radius="xl"
            onClick={() => navigate("/login")}
          >
            Enter the platform <FaTasks />
          </Button>
        )}
      </div>
    </div>
  );
};

export default LandingPage;
