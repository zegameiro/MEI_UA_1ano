import {
  User,
  Dropdown,
  DropdownItem,
  DropdownMenu,
  DropdownTrigger,
} from "@nextui-org/react";
import { googleLogout } from "@react-oauth/google";
import { useNavigate } from "react-router-dom";
import { useCookies } from "react-cookie";

import { FiLogOut } from "react-icons/fi";

import { useUserStore } from "../stores/userStore";

const ProfileComponent = () => {
  const [_cookies, _setCookie, removeCookie] = useCookies();

  const user_name = useUserStore((state) => state.user_name) || false;
  const picture_url = useUserStore((state) => state.picture_url) || false;
  const logoutStore = useUserStore((state) => state.logout) || false;

  const navigate = useNavigate();

  const logout = () => {
    googleLogout();
    removeCookie("credential");
    logoutStore();
    navigate("/");
  };

  return (
    <Dropdown backdrop="blur">
      <DropdownTrigger>
        <div className="flex flex-row items-center gap-2 cursor-pointer">
          <img
            src={picture_url}
            alt="profile"
            className="w-10 h-10 rounded-full"
            fetch-priority="low"
            loading="lazy"
            decoding="async"
            referrerPolicy="no-referrer"
          />
          <span className="text-lg">{user_name}</span>
        </div>
      </DropdownTrigger>
      <DropdownMenu aria-label="Static Actions">
        <DropdownItem
          key="delete"
          color="danger"
          textValue="Logout"
          onClick={() => logout()}
        >
          <span className="flex flex-row items-center gap-2 text-danger hover:text-white">
            <FiLogOut /> Logout
          </span>
        </DropdownItem>
      </DropdownMenu>
    </Dropdown>
  );
};

export default ProfileComponent;
