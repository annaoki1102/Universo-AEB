import { motion } from 'motion/react';
import sagiCrabImage from '../../../assets/sagicrab.png';
import React from 'react';

export function Hero(): React.JSX.Element {
  return (
    <section id="home" className="relative min-h-screen flex items-center justify-center px-6 overflow-hidden">
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-b from-transparent via-[#0a0e27]/50 to-[#0a0e27]" style={{ zIndex: 1 }} />
      
      <div className="relative z-10 max-w-7xl mx-auto w-full grid md:grid-cols-2 gap-12 items-center py-20">
        {/* Text content */}
        <motion.div
          initial={{ opacity: 0, x: -50 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.8 }}
          className="text-left"
        >
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="inline-block mb-4 px-4 py-2 rounded-full bg-cyan-500/10 border border-cyan-500/30"
          >
            <span className="text-cyan-400 text-sm font-medium">Versão Alpha 1.0</span>
          </motion.div>
          
          <div className="flex items-center gap-4 mb-6">
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-cyan-300 via-blue-400 to-cyan-500 bg-clip-text text-transparent leading-tight">Universo AEB</h1>
            
          </div>
          
          <p className="text-gray-300 text-lg md:text-xl mb-8 leading-relaxed">
            Navegação intergaláctica impulsionada por inteligência artificial avançada. 
            Explore o cosmos com tecnologia de ponta e assistência espacial inteligente.
          </p>
          
          <div className="flex flex-wrap gap-4">
            <motion.a
            href="/assistentes"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white rounded-lg font-medium shadow-lg shadow-cyan-500/50 hover:shadow-cyan-500/70 transition-shadow"
            >
              Iniciar Exploração
            </motion.a>
          </div>
        </motion.div>
        
        {/* Sagi-Crab Image */}
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.3 }}
          className="relative flex items-center justify-center"
        >
          <motion.div
            animate={{
              y: [0, -20, 0],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut"
            }}
            className="relative"
          >
            {/* Glow effect */}
            <div className="absolute inset-0 blur-3xl bg-cyan-500/30 rounded-full scale-110" />
            <div className="absolute inset-0 blur-2xl bg-blue-600/20 rounded-full scale-125 animate-pulse" />
            
            {/* Image */}
            <img
              src={sagiCrabImage}
              alt="Sagi-Crab"
              className="relative w-[130%] h-auto"
            />
          </motion.div>
        </motion.div>
      </div>
      
      {/* Bottom gradient */}
      <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-[#0a0e27] to-transparent" style={{ zIndex: 2 }} />
    </section>
  );
}
