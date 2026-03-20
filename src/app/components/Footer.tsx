export function Footer() {
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
              Navegação intergaláctica impulsionada por inteligência artificial avançada.
            </p>
          </div>
          
          <div>
            <h4 className="text-cyan-300 font-semibold mb-4">Navegação</h4>
            <ul className="space-y-2">
              <li><a href="#home" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">Início</a></li>
              <li><a href="#about" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">Sobre</a></li>
              <li><a href="#features" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">Recursos</a></li>
              <li><a href="#crew" className="text-gray-400 hover:text-cyan-400 transition-colors text-sm">Tripulação</a></li>
            </ul>
          </div>
          
          <div>
            <h4 className="text-cyan-300 font-semibold mb-4">Tecnologia</h4>
            <ul className="space-y-2">
              <li className="text-gray-400 text-sm">Inteligência Artificial</li>
              <li className="text-gray-400 text-sm">Navegação Espacial</li>
              <li className="text-gray-400 text-sm">Sistemas de Satélites</li>
              <li className="text-gray-400 text-sm">Computação Quântica</li>
            </ul>
          </div>
        </div>
        
        <div className="pt-8 border-t border-cyan-500/10 text-center text-gray-500 text-sm">
          © 2026 Universo Sagi-Crab. Todos os direitos reservados.
        </div>
      </div>
    </footer>
  );
}
