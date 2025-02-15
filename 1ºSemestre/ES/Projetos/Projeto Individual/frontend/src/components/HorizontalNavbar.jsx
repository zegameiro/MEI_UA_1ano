import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
  Button,
} from "@nextui-org/react";

import { LogoHorizontal } from "../assets";
import ProfileComponent from "./ProfileComponent";
import { useUserStore } from "../stores/userStore";

const HorizontalNavBar = () => {
  const isLoggedIn = useUserStore((state) => state.isLoggedIn) || false;

  return (
    <Navbar isBordered isBlurred>
      <NavbarContent>
        <NavbarBrand>
          <Link href={isLoggedIn ? "/home" : "/"}>
            <img src={LogoHorizontal} alt="Logo Image" width={200} />
          </Link>
        </NavbarBrand>
      </NavbarContent>

      <NavbarContent justify="end">
        <NavbarItem>
          {isLoggedIn ? (
            <ProfileComponent />
          ) : (
            <Button
              as={Link}
              color="primary"
              href="/login"
              variant="ghost"
              className="text-lg"
            >
              Login
            </Button>
          )}
        </NavbarItem>
      </NavbarContent>
    </Navbar>
  );
};

export default HorizontalNavBar;
