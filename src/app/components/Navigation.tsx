import { useState, useEffect } from 'react';

export function Navigation() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-[#0a0e27]/90 backdrop-blur-md shadow-lg shadow-cyan-500/10' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-cyan-400 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/50">
            <span className="text-white font-bold text-sm">SC</span>
          </div>
          <span className="text-cyan-300 font-semibold text-lg tracking-wide">Sagi-Crab</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8">
          <a href="#home" className="text-gray-300 hover:text-cyan-400 transition-colors">
            Início
          </a>
          <a href="#about" className="text-gray-300 hover:text-cyan-400 transition-colors">
            Sobre
          </a>
          <a href="#features" className="text-gray-300 hover:text-cyan-400 transition-colors">
            Recursos
          </a>
          <a href="#crew" className="text-gray-300 hover:text-cyan-400 transition-colors">
            Tripulação
          </a>
        </div>
      </div>
    </nav>
  );
}
