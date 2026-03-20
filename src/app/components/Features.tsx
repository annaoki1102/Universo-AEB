import { motion } from 'motion/react';
import { Zap, Shield, Globe, Cpu } from 'lucide-react';

const features = [
  {
    icon: Zap,
    title: 'Velocidade Superluminal',
    description: 'Processamento em tempo real com latência próxima de zero',
  },
  {
    icon: Shield,
    title: 'Segurança Quântica',
    description: 'Criptografia de nível quântico para proteção total de dados',
  },
  {
    icon: Globe,
    title: 'Cobertura Global',
    description: 'Conectividade em qualquer ponto do universo conhecido',
  },
  {
    icon: Cpu,
    title: 'Processamento Neural',
    description: 'Redes neurais avançadas para análise e tomada de decisão',
  },
];

export function Features() {
  return (
    <section id="features" className="relative py-24 px-6">
      <div className="max-w-6xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-6 bg-gradient-to-r from-cyan-300 to-blue-400 bg-clip-text text-transparent">
            Recursos Tecnológicos
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Tecnologias de ponta que impulsionam a próxima geração de exploração espacial
          </p>
        </motion.div>

        <div className="grid md:grid-cols-2 gap-6">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, x: index % 2 === 0 ? -30 : 30 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              className="relative group"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-cyan-500/10 to-blue-600/10 rounded-xl blur-lg group-hover:blur-xl transition-all" />
              <div className="relative bg-[#0f1629]/60 backdrop-blur-sm border border-cyan-500/20 rounded-xl p-6 hover:border-cyan-500/40 transition-colors flex items-start gap-4">
                <div className="w-12 h-12 bg-gradient-to-br from-cyan-500/20 to-blue-600/20 rounded-lg flex items-center justify-center flex-shrink-0 border border-cyan-500/30">
                  <feature.icon className="w-6 h-6 text-cyan-400" />
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-cyan-300 mb-2">{feature.title}</h3>
                  <p className="text-gray-400">{feature.description}</p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
