import { useLocation } from "react-router-dom";

export function Footer() {
  const location = useLocation();

  const handleFooterNavigation = (sectionId: string) => {
    if (location.pathname !== "/") {
      window.location.href = `/#${sectionId}`;
      return;
    }

    const element = document.getElementById(sectionId);

    if (sectionId === "home") {
      window.scrollTo({
        top: 0,
        behavior: "smooth",
      });
      return;
    }

    if (element) {
      element.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  };

  return (
    <footer className="relative py-12 px-6 border-t border-cyan-500/10">
      <div className="max-w-6xl mx-auto">
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/50">
                <span className="text-white font-bold text-sm">SC</span>
              </div>
              <span className="text-cyan-300 font-semibold text-lg">Sagi-Crab</span>
            </div>
            <p className="text-gray-400 text-sm">
              Navegação intergaláctica impulsionada por inteligência artificial.
            </p>
          </div>

          <div>
            <h4 className="text-cyan-300 font-semibold mb-4">Navegação</h4>
            <ul className="space-y-2">
              <li>
                <button
                  onClick={() => handleFooterNavigation("home")}
                  className="text-gray-400 hover:text-cyan-400 transition-colors text-sm bg-transparent border-none cursor-pointer p-0"
                >
                  Início
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleFooterNavigation("about")}
                  className="text-gray-400 hover:text-cyan-400 transition-colors text-sm bg-transparent border-none cursor-pointer p-0"
                >
                  Sobre
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleFooterNavigation("features")}
                  className="text-gray-400 hover:text-cyan-400 transition-colors text-sm bg-transparent border-none cursor-pointer p-0"
                >
                  Recursos
                </button>
              </li>
              <li>
                <button
                  onClick={() => handleFooterNavigation("crew")}
                  className="text-gray-400 hover:text-cyan-400 transition-colors text-sm bg-transparent border-none cursor-pointer p-0"
                >
                  Tripulação
                </button>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="text-cyan-300 font-semibold mb-4">AEB Escola</h4>
            <ul className="space-y-2">
              <li className="text-gray-400 text-sm">Inteligência Artificial</li>
              <li className="text-gray-400 text-sm">Educação Espacial</li>
              <li className="text-gray-400 text-sm">Aprendizagem Interativa</li>
              <li className="text-gray-400 text-sm">Conteúdos Educacionais</li>
            </ul>
          </div>
        </div>

        <div className="pt-8 border-t border-cyan-500/10 text-center text-gray-500 text-sm">
          © 2026 Universo AEB. Todos os direitos reservados.
        </div>
      </div>
    </footer>
  );
}