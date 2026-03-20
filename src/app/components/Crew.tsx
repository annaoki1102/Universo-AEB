import { motion } from 'motion/react';
import { Sparkles, Satellite, Wrench } from 'lucide-react';

const crewMembers = [
  {
    name: 'Cosminho',
    role: 'Guia de Iniciação Espacial',
    description: 'Especialista em orientar novos exploradores através dos fundamentos da navegação espacial e protocolos de segurança intergaláctica.',
    icon: Sparkles,
    gradient: 'from-cyan-400 to-blue-500',
  },
  {
    name: 'Luana',
    role: 'Especialista em Tecnologia e Satélites',
    description: 'Responsável pela manutenção e otimização da rede de satélites, garantindo comunicação e monitoramento contínuos em todas as missões.',
    icon: Satellite,
    gradient: 'from-blue-400 to-purple-500',
  },
  {
    name: 'Sagi-Crab',
    role: 'Assistente Inteligente em Construção',
    description: 'IA avançada em desenvolvimento contínuo, projetada para aprender e evoluir, oferecendo suporte adaptativo em exploração espacial.',
    icon: Wrench,
    gradient: 'from-cyan-500 to-teal-500',
  },
];

export function Crew() {
  return (
    <section id="crew" className="relative py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">
            Tripulação
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Conheça a equipe especializada que impulsiona o Universo Sagi-Crab
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-8">
          {crewMembers.map((member, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.15 }}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-2xl blur-xl group-hover:blur-2xl transition-all" />
              <div className="relative bg-[#0f1629]/80 backdrop-blur-sm border border-cyan-500/20 rounded-2xl p-8 hover:border-cyan-500/40 transition-all hover:transform hover:scale-[1.02] h-full flex flex-col">
                <div className={`w-20 h-20 bg-gradient-to-br ${member.gradient} rounded-2xl flex items-center justify-center mb-6 shadow-lg shadow-cyan-500/30 mx-auto`}>
                  <member.icon className="w-10 h-10 text-white" />
                </div>
                
                <h3 className="text-2xl font-semibold text-cyan-300 mb-2 text-center">{member.name}</h3>
                <p className="text-sm text-cyan-500/80 mb-4 text-center font-medium">{member.role}</p>
                <p className="text-gray-400 leading-relaxed text-center text-sm flex-grow">{member.description}</p>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}