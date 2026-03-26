import { motion } from 'motion/react';

const features = [
  {
    image: "/images/navegacao.png",
    title: 'Navegação Inteligente',
    description: 'Sistema avançado de navegação que orienta usuários na exploração de conteúdos e trilhas do conhecimento espacial.',
  },
  {
    image: "/images/ia.png",
    title: 'Assistência com IA',
    description: 'Personagens inteligentes que auxiliam no aprendizado, respondem dúvidas e guiam a jornada educacional.',
  },
  {
    image: "/images/satelite.png",
    title: 'Conectividade Espacial',
    description: 'Integração de conteúdos, recursos e experiências digitais em uma plataforma interativa e acessível.',
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
            Navegação
          </h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Tecnologias de ponta que impulsionam a próxima geração de exploração espacial
          </p>
        </motion.div>

        <div className="grid md:grid-cols-3 gap-6">
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
              
              <div className="relative bg-[#0f1629]/60 backdrop-blur-sm border border-cyan-500/20 rounded-xl p-6 hover:border-cyan-500/40 transition-colors">
                <div className="w-full text-center">
                  <div className="flex justify-center mb-6">
                    <img
                      src={feature.image}
                      alt={feature.title}
                      className="w-32 h-32 object-contain drop-shadow-[0_0_25px_rgba(56,189,248,0.5)]"
                    />
                  </div>

                  <h3 className="text-xl font-semibold text-cyan-300 mb-2">
                    {feature.title}
                  </h3>

                  <p className="text-gray-400">
                    {feature.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
} 