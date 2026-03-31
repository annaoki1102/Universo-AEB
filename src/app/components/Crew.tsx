import { motion } from 'motion/react';
import { Particles } from './Particles';
import React from 'react';

export function Crew() {
  return (
    <section className="relative min-h-[80vh] flex items-center justify-center px-2 md:px-4">
      
      <div className="relative w-full max-w-6xl h-[500px] md:h-[600px] px-12 md:px-20 rounded-3xl bg-[#0f1629]/80 border border-cyan-500/20 backdrop-blur-md overflow-hidden flex items-center justify-start">

        <Particles />

        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400/20 via-blue-500/20 to-cyan-400/20 blur-3xl opacity-70 animate-pulse"></div>

        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="relative text-left max-w-xl"
        >
          <h2 className="text-3xl md:text-4xl lg:text-5xl font-bold text-cyan-300 mb-3 leading-tight">
            O Universo já está em movimento
          </h2>

          <p className="text-gray-400 text-lg leading-relaxed">
            Cada interação abre um novo caminho. Cada escolha revela uma <br />
            nova possibilidade. A exploração não começa aqui, ela já começou.
          </p>
        </motion.div>

      </div>
    </section>
  );
}