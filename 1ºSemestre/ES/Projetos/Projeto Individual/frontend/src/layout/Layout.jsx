import HorizontalNavBar from "../components/HorizontalNavbar";

const Layout = ({ children }) => {
  return (
    <main className="flex flex-col">
      <HorizontalNavBar />
      <section className="px-[10vw] py-[4vh] text-text">{children}</section>
    </main>
  );
};

export default Layout;
