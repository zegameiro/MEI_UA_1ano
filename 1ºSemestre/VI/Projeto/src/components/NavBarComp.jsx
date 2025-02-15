import {
  Navbar,
  NavbarBrand,
  NavbarContent,
  NavbarItem,
  Link,
} from "@nextui-org/react";
import { Logo } from "../assets";

const NavBarComp = () => {
  return (
    <Navbar isBordered className="bg-success-50">
      <NavbarBrand>
        <Link
          href="/"
          color="success"
          className="flex flex-row gap-2 items-center"
        >
          <img src={Logo} alt="Logo Image" width={50} />
          <p className="font-bold text-inherit">SpotiVis</p>
        </Link>
      </NavbarBrand>
    </Navbar>
  );
};

export default NavBarComp;
