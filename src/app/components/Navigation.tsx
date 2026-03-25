import { useState, useEffect } from "react";
import { Link } from "react-router-dom";

export function Navigation() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled
          ? "bg-[#050b1f]/95 backdrop-blur-md border-b border-white/10"
          : "bg-[#050b1f]/95 border-b border-white/10"
      }`}
    >
      <div className="w-full px-4 md:px-6 py-3 flex items-center justify-between">
        <Link to="/#home" className="flex items-center gap-3 no-underline">
          <div className="text-2xl">🚀</div>

          <div className="leading-tight">
            <div className="text-white font-extrabold tracking-wide text-lg md:text-xl uppercase">
              Turma AEB
            </div>
            <div className="text-white/55 text-[10px] md:text-xs tracking-[0.22em] uppercase">
              Agência Espacial Brasileira · AEB Escola
            </div>
          </div>
        </Link>

        <div className="hidden md:flex items-center gap-8 text-sm">
          <Link to="/#home" className="text-white/85 hover:text-white transition-colors">
            Início
          </Link>
          <Link to="/#about" className="text-white/85 hover:text-white transition-colors">
            Sobre
          </Link>
          <Link to="/#features" className="text-white/85 hover:text-white transition-colors">
            Recursos
          </Link>
          <Link to="/#crew" className="text-white/85 hover:text-white transition-colors">
            Tripulação
          </Link>
        </div>
      </div>
    </nav>
  );
}