import { useState, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";

export function Navigation() {
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  const handleSectionNavigation = (sectionId: string) => {
    if (location.pathname === "/assistentes") {
      window.location.href = `/#${sectionId}`;
      return;
    }

    if (sectionId === "home") {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
      window.history.replaceState(null, "", "/#home");
      return;
    }

    const element = document.getElementById(sectionId);

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
      window.history.replaceState(null, "", `/#${sectionId}`);
    }
  };

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[#050b1f]/95 backdrop-blur-md border-b border-white/10"
          : "bg-[#050b1f]/95 border-b border-white/10"
      }`}
    >
      <div className="w-full px-6 md:px-8 py-3 flex items-center justify-between">
        <Link to="/#home" className="flex items-center gap-3 no-underline">
          <div className="leading-tight">
            <div className="text-white font-extrabold tracking-wide text-lg md:text-xl uppercase">
              Turma AEB
            </div>
            <div className="text-white/65 text-[10px] md:text-xs tracking-[0.22em] uppercase">
              Agência Espacial Brasileira · AEB Escola
            </div>
          </div>
        </Link>

        <div className="hidden md:flex items-center gap-8 text-sm">
          <button
            onClick={() => handleSectionNavigation("home")}
            className="text-white/85 hover:text-white transition-colors bg-transparent border-none cursor-pointer"
          >
            Início
          </button>

          <button
            onClick={() => handleSectionNavigation("about")}
            className="text-white/85 hover:text-white transition-colors bg-transparent border-none cursor-pointer"
          >
            Sobre
          </button>

          <button
            onClick={() => handleSectionNavigation("features")}
            className="text-white/85 hover:text-white transition-colors bg-transparent border-none cursor-pointer"
          >
            Recursos
          </button>

          <button
            onClick={() => handleSectionNavigation("crew")}
            className="text-white/85 hover:text-white transition-colors bg-transparent border-none cursor-pointer"
          >
            Tripulação
          </button>
        </div>
      </div>
    </nav>
  );
}