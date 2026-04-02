import { motion } from 'motion/react';
import { Rocket, Brain, Satellite } from 'lucide-react';

export function About() {
  return (
    <section id="about" className="relative py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent pb-2">Exploração Espacial Inteligente</h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            O Universo Sagi-Crab combina tecnologia avançada de IA com sistemas de navegação intergaláctica 
            para criar a mais completa plataforma de exploração espacial.
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
            <div className="relative bg-[#0f1629]/80 backdrop-blur-sm border border-cyan-500/20 rounded-2xl p-8 hover:border-cyan-500/40 transition-colors">
              <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/50">
                <Rocket className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-cyan-300 mb-4">Navegação Avançada</h3>
              <p className="text-gray-400 leading-relaxed">
                Sistemas de navegação intergaláctica de última geração com precisão absoluta 
                para exploração em qualquer região do cosmos.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
            <div className="relative bg-[#0f1629]/80 backdrop-blur-sm border border-cyan-500/20 rounded-2xl p-8 hover:border-cyan-500/40 transition-colors h-full flex flex-col">
              <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/50">
                <Brain className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-cyan-300 mb-4">IA Adaptativa</h3>
              <p className="text-gray-400 leading-relaxed flex-grow">
                Inteligência artificial que aprende e evolui constantemente, 
                oferecendo assistência personalizada em cada missão espacial.
              </p>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.3 }}
            className="relative group"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
            <div className="relative bg-[#0f1629]/80 backdrop-blur-sm border border-cyan-500/20 rounded-2xl p-8 hover:border-cyan-500/40 transition-colors">
              <div className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-xl flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/50">
                <Satellite className="w-8 h-8 text-white" />
              </div>
              <h3 className="text-2xl font-semibold text-cyan-300 mb-4">Tecnologia de Satélites</h3>
              <p className="text-gray-400 leading-relaxed">
                Rede avançada de satélites para comunicação e monitoramento em tempo real 
                de todas as operações espaciais.
              </p>
            </div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}