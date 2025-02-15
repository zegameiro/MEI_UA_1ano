import { useNavigate } from "react-router-dom";
import { useUserStore } from "../stores/userStore";
import { Outlet, Link } from "react-router-dom";
import { useEffect } from "react";

const RequiredAuth = () => {
  const isLoggedIn = useUserStore((state) => state.isLoggedIn) || false;
  const navigate = useNavigate();
  console.log("isLoggedIn:", isLoggedIn);

  useEffect(() => {
    if (!isLoggedIn) {
      alert("You must login first");
      navigate("/login");
    } // else content is shown based on the Outlet component
  }, [isLoggedIn]);

  let content;

  if (isLoggedIn) content = <Outlet />;

  return content;
};

export default RequiredAuth;
